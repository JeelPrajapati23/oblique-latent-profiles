"""Week 4: final results tables (Markdown + LaTeX) and figures for the report.

Every number is recomputed here from the saved (masked) run files, so the tables can't drift from
the runs. Outputs:
    reports/results.md              all tables
    reports/tables.tex              the same tables, booktabs LaTeX
    reports/figures/*.png           figures

    python scripts/make_results.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
import numpy as np
from scipy.stats import ttest_rel

from obliq.data import ROOT, load_task
from obliq.evaluate import METRICS, evaluate_run, per_query
from obliq.fusion import dev_split, rrf
from obliq.runs import load_run

FIG = ROOT / "reports" / "figures"
OURS, PAPER, ACCENT2 = "#2a78d6", "#a3a29b", "#eb6834"  # categorical slot 1, neutral, slot 2
INK, MUTED = "#222222", "#555555"

# (label, run file, kind) per task; kind: base = E1 baseline, ours, var = labelled variant, not headline
SYSTEMS = {
    "math": [
        ("BM25 text", "bm25_text_word", "base"),
        ("Qwen3-0.6B text", "qwen3-0.6b_text_none", "base"),
        ("E2 LLM query rewrite + Qwen3", "E2_rewrite_qwen3-0.6b_none", "ours"),
        ("E3 profiles only (RRF of 2)", "E3_RRF_profile_BM25-p_dense-p", "ours"),
        ("E4 text + profiles, RRF of 4 (main)", "E4_RRF_all_4_k_60", "ours"),
        ("E4, dev-tuned weights", "E4_weighted_RRF_all_4", "ours"),
        ("E5 = E4 + 7B listwise re-rank", "E5_rerank_top50_E4_RRF_all_4_k_60", "ours"),
        ("E4 with solution-aware doc profiles", "E4_RRF_all_4_k_60_soln_variant", "var"),
    ],
    "writing": [
        ("BM25 text", "bm25_text_split", "base"),
        ("Qwen3-0.6B text", "qwen3-0.6b_text_none", "base"),
        ("E2 LLM query rewrite + Qwen3", "E2_rewrite_qwen3-0.6b_query", "ours"),
        ("E3 profiles only (RRF of 2)", "E3_RRF_profile_BM25-p_dense-p", "ours"),
        ("E4 text + profiles, RRF of 4 (main)", "E4_RRF_all_4_k_60", "ours"),
        ("E4, dev-tuned weights", "E4_weighted_RRF_all_4", "ours"),
        ("E4, profiles without Voice/Tone", "F_E4_with_B_B_bm25_profile_no_voice_tone_replacing_BM25-p_dense-p", "ours"),
        ("Char 3-5-gram TF-IDF", "D_tfidf_char_35", "var"),
        ("Style-Embedding (Wegmann)", "D_style_emb", "var"),
        ("BM25 + char n-gram + Style-Emb, RRF", "F_BM25-t_D_D_tfidf_char_35_D_style_emb", "var"),
    ],
}
BEST_E1 = {"math": "qwen3-0.6b_text_none", "writing": "bm25_text_split"}  # picked on dev in run_profiles.py
MAIN = "E4_RRF_all_4_k_60"
# Paper (Tchuindjo et al. 2026), nDCG@10; Math pooled, Writing gold.
PAPER_SYS = {"math": [("Gemini-2-Embedding", .147), ("GPT-5.2 rewriter + Gemini", .185),
                      ("GPT-5.2 multi-hop agent", .207), ("Oracle GPT-5.2 re-ranker", .329)],
             "writing": [("Gemini-2-Embedding", .164), ("GPT-5.2 rewriter + Gemini", .018),
                         ("GPT-5.2 multi-hop agent", .061), ("Oracle GPT-5.2 re-ranker", .515)]}
# E1 reproduction: our run, paper Table 3 cells (nDCG@10, nDCG@50, R@10, R@50, R@100; Math gold/pooled).
# None = cell not recorded in CLAUDE.md; check the paper PDF.
E1 = {
    "math": [("BM25", "bm25_text_lower", [(.022, .029), (.034, .025), (.020, .029), (.060, .029), (.088, .029)]),
             ("Qwen3-Embedding-0.6B", "qwen3-0.6b_text_query",
              [(None, .143), (.149, .176), (.070, .088), (.219, .247), (.309, .336)])],
    "writing": [("BM25", "bm25_text_word", [(.077,), (.114,), (.062,), (.154,), (.208,)]),
                ("Qwen3-Embedding-0.6B", "qwen3-0.6b_text_none", [(.046,), (.060,), (.040,), (.075,), (.103,)])],
}
JOBS = {"math": "profiles (main)", "math_soln": "profiles with solutions (variant)",
        "math_topic": "profiles, topic allowed (A1)", "math_short": "profiles, ~40 words (A3)",
        "math_rewrite": "E2 query rewrites", "writing": "profiles (main)", "writing_rewrite": "E2 query rewrites"}
ABLATIONS = [("Main: 7B, no topic words, 60-100 words", "math-ee895b"),
             ("A1: topic words allowed", "math_topic-1af30a"),
             ("A2: 3B profiler", "math-ee895b_3B"),
             ("A3: ~40-word profiles", "math_short-07ea6b")]


def cell(res, m):
    return "/".join(f"{res[k][m]:.3f}" for k in ("gold", "pool") if k in res)


def pval(run, base, task, test):
    """Paired t-test on test nDCG@10 per qrels type; '+'/'-' = better/worse on average."""
    a, b = per_query(run, task, qids=test), per_query(base, task, qids=test)
    out = []
    for k in a:
        qs = sorted(a[k])
        x, y = [a[k][q] for q in qs], [b[k][q] for q in qs]
        if x == y:
            return "–"
        out.append(f"{ttest_rel(x, y).pvalue:.2g}{'+' if sum(x) > sum(y) else '−'}")
    return "/".join(out)


def md_table(header, rows):
    return ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(r) + " |" for r in rows]


def tex_table(header, rows, caption, label):
    esc = lambda s: (s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("~", r"$\sim$")
                     .replace("−", "$-$").replace("**", "").replace("`", ""))
    return [r"\begin{table}[t]", r"\centering\small", f"\\caption{{{esc(caption)}}}", f"\\label{{{label}}}",
            r"\begin{tabular}{l" + "r" * (len(header) - 1) + "}", r"\toprule",
            " & ".join(esc(h) for h in header) + r" \\", r"\midrule",
            *[" & ".join(esc(c) for c in r) + r" \\" for r in rows], r"\bottomrule", r"\end{tabular}",
            r"\end{table}", ""]


def style(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#bbbbbb")
    ax.spines["bottom"].set_color("#bbbbbb")
    ax.tick_params(colors=MUTED, labelsize=8.5)
    ax.xaxis.grid(True, color="#e6e6e6", linewidth=0.8)
    ax.set_axisbelow(True)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    md, tex, scores = ["# Results tables", "",
                       "Generated by `scripts/make_results.py` from the masked run files. Math cells are "
                       "gold/pooled, Writing gold only. p = paired t-test on the fixed 80% test split "
                       "(nDCG@10) vs the best E1 baseline picked on dev; +/− = better/worse on average; "
                       "claim a win only at p < 0.05.", ""], [], {}
    tasks = {n: load_task(n) for n in ("math", "writing")}
    splits = {n: dev_split(n, t.qrels) for n, t in tasks.items()}

    # ---- Table 1: E1 reproduction
    rows = []
    for name, task in tasks.items():
        for label, run_name, paper in E1[name]:
            res = evaluate_run(load_run(name, run_name), task)
            rows.append([f"{name.title()} {label}", f"`{run_name}`"] + [
                f"{cell(res, m)} ({'/'.join('–' if v is None else f'{v:.3f}' for v in p)})"
                for m, p in zip(METRICS, paper)])
    h = ["task / system", "our run", *METRICS]
    cap = "E1 reproduction: ours (paper Table 3 in brackets). Math gold/pooled, Writing gold."
    md += ["## Table 1. " + cap, "", *md_table(h, rows), ""]
    tex += tex_table(h[:1] + h[2:], [[r[0]] + r[2:] for r in rows], cap, "tab:e1")

    # ---- Table 2/3: main results per task
    for i, (name, task) in enumerate(tasks.items(), 2):
        dev, test = splits[name]
        base = load_run(name, BEST_E1[name])
        rows, scores[name] = [], {}
        for label, run_name, kind in SYSTEMS[name]:
            run = load_run(name, run_name)
            a, t = evaluate_run(run, task), evaluate_run(run, task, ["ndcg@10"], test)
            scores[name][label] = (a, kind)
            mark = {"base": " (E1)", "var": " †", "ours": ""}[kind]
            bold = "**" if run_name == MAIN else ""
            rows.append([f"{bold}{label}{mark}{bold}", *(cell(a, m) for m in METRICS), cell(t, "ndcg@10"),
                         "–" if run_name == BEST_E1[name] else pval(run, base, task, test)])
        q = "gold/pooled" if task.qrels_pool else "gold"
        cap = (f"{name.title()} ({len(task.queries)} queries; {q}). Paper nDCG@10: "
               + ", ".join(f"{s} {v:.3f}" for s, v in PAPER_SYS[name]) + ".")
        h = ["system", *METRICS, "test nDCG@10", f"p vs {BEST_E1[name]}"]
        notes = {"math": "E1 rows and E4's text components use the dev-picked settings (BM25 `word` "
                         "tokenizer, Qwen3 without a query prompt), so they differ from Table 1, which matches the "
                         "paper's setup. † Docs profiled together with their solutions, which the paper's retrievers never saw; "
                         "not the headline number.",
                 "writing": "E1 rows use the dev-picked settings (BM25 `split` tokenizer), so BM25 differs "
                            "from Table 1. † Non-LLM style baselines (step D), not part of the profile method."}[name]
        md += [f"## Table {i}. " + cap, "", *md_table(h, rows), "", notes, ""]
        tex += tex_table(h, rows, cap + " " + notes, f"tab:{name}")

    # ---- Table 4: ablations (Math)
    task = tasks["math"]
    dev, test = splits["math"]
    text = [load_run("math", "bm25_text_word"), load_run("math", "qwen3-0.6b_text_none")]
    abl, rows = {}, []
    for label, tag in ABLATIONS:
        e3 = rrf([load_run("math", f"A_{tag}_bm25_profile_word"), load_run("math", f"A_{tag}_qwen3-0.6b_profile_query")])
        abl[label] = (e3, rrf(text + [load_run("math", f"A_{tag}_bm25_profile_word"),
                                      load_run("math", f"A_{tag}_qwen3-0.6b_profile_query")]))
    m3, m4 = abl[ABLATIONS[0][0]]
    abl_scores = {}
    for label, (e3, e4) in abl.items():
        r3, r4 = evaluate_run(e3, task, ["ndcg@10"]), evaluate_run(e4, task, ["ndcg@10"])
        abl_scores[label] = (r3, r4)
        first = label == ABLATIONS[0][0]
        rows.append([label, cell(r3, "ndcg@10"), "–" if first else pval(e3, m3, task, test),
                     cell(r4, "ndcg@10"), "–" if first else pval(e4, m4, task, test)])
    h = ["profiles", "E3 nDCG@10", "p vs main E3", "E4 nDCG@10", "p vs main E4"]
    cap = "Ablations on Math (gold/pooled nDCG@10, all queries; p on test). Retrieval components fixed."
    md += ["## Table 4. " + cap, "", *md_table(h, rows), ""]
    tex += tex_table(h, rows, cap, "tab:ablations")

    # ---- Table 5: cost
    rows = []
    for f in sorted((ROOT / "profiles").glob("*/*/cost.jsonl")) + sorted((ROOT / "rerank").glob("*/cost.jsonl")):
        recs = [r for r in map(json.loads, f.read_text().splitlines()) if r.get("limit", 0) == 0]
        if not recs:
            continue
        gm = sum(r["seconds"] * r.get("gpus", 1) / 60 for r in recs)
        n = sum(r.get("generated", r.get("windows", 0)) for r in recs)
        if f.parent.parent.name == "rerank":
            job = f"E5 listwise re-rank, {f.parent.name.title()} top 50"
        else:
            setting, model = f.parent.name.split("__")
            setting = setting.rsplit("-", 1)[0]
            size = model.split("-")[1]
            what = "profiles, main prompt (A2)" if size == "3B" else JOBS.get(setting, setting)
            job = f"{f.parent.parent.name.title()}: {what}, {size}"
        rows.append([job, str(n or "–"), f"{gm:.0f}"])
    h = ["LLM job (Kaggle 2× T4)", "items", "GPU-minutes"]
    cap = "One-off LLM cost. Online cost of E4 is ~100 ms/query on a laptop CPU plus one LLM call for the query profile."
    md += ["## Table 5. " + cap, "", *md_table(h, rows), ""]
    tex += tex_table(h, rows, cap, "tab:cost")

    (ROOT / "reports" / "results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (ROOT / "reports" / "tables.tex").write_text("\n".join(tex), encoding="utf-8")
    print("\n".join(md))

    # ---- Figure 1: headline nDCG@10 vs the paper (oracle left out: it sees the gold doc)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, name in zip(axes, ("math", "writing")):
        k = "pool" if name == "math" else "gold"
        items = [(s, v, "paper") for s, v in PAPER_SYS[name][:3]]
        items += [(lab, a[k]["ndcg@10"], kind) for lab, (a, kind) in scores[name].items()
                  if "dev-tuned" not in lab and "Voice/Tone" not in lab and not lab.startswith(("Char", "Style"))]
        items = items[::-1]
        y = np.arange(len(items))
        colors = [PAPER if kd == "paper" else OURS for _, _, kd in items]
        ax.barh(y, [v for _, v, _ in items], color=colors, height=0.62, edgecolor="white", linewidth=1.5)
        for yi, (lab, v, kd) in zip(y, items):
            ax.text(v + 0.003, yi, f"{v:.3f}", va="center", fontsize=8, color=INK,
                    fontweight="bold" if "(main)" in lab else "normal")
        ax.set_yticks(y, [f"{lab} (paper)" if kd == "paper" else lab for lab, _, kd in items], fontsize=8.5)
        for t, (lab, _, _) in zip(ax.get_yticklabels(), items):
            if "(main)" in lab:
                t.set_fontweight("bold")
        ax.set_xlim(0, max(v for _, v, _ in items) * 1.18)
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.set_xlabel(f"nDCG@10 ({'pooled' if k == 'pool' else 'gold'} qrels)", fontsize=9, color=MUTED)
        ax.set_title(f"{name.title()}", fontsize=11, color=INK, loc="left")
        style(ax)
    fig.legend(handles=[Patch(color=OURS, label="ours (open models)"), Patch(color=PAPER, label="paper (GPT-5.2 / Gemini)")],
               loc="upper right", frameon=False, fontsize=8.5, ncol=2)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(FIG / "fig1_main_results.png", dpi=200, facecolor="white")

    # ---- Figure 2: ablations, E3 and E4 (pooled)
    fig, ax = plt.subplots(figsize=(7, 3.4))
    labs = [l for l, _ in ABLATIONS][::-1]
    y = np.arange(len(labs))
    for off, idx, col, name in ((0.19, 0, ACCENT2, "E3: profiles only"), (-0.19, 1, OURS, "E4: text + profiles")):
        vals = [abl_scores[l][idx]["pool"]["ndcg@10"] for l in labs]
        ax.barh(y + off, vals, height=0.36, color=col, label=name, edgecolor="white", linewidth=1.5)
        for yi, v in zip(y, vals):
            ax.text(v + 0.002, yi + off, f"{v:.3f}", va="center", fontsize=8, color=INK)
    ax.axvline(.147, color=MUTED, linestyle="--", linewidth=1)
    ax.text(.1475, -0.75, "paper Gemini .147", fontsize=8, color=MUTED, va="bottom")
    ax.set_yticks(y, labs, fontsize=8.5)
    ax.set_xlim(0, 0.215)
    ax.set_ylim(-0.8, len(labs) - 0.45)
    ax.set_xlabel("Math nDCG@10 (pooled qrels)", fontsize=9, color=MUTED)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2)
    style(ax)
    fig.tight_layout()
    fig.savefig(FIG / "fig2_ablations_math.png", dpi=200, facecolor="white")

    # ---- Figure 3: per-query Math, Qwen3 text vs E4 (pooled)
    a = per_query(load_run("math", MAIN), task)["pool"]
    b = per_query(load_run("math", "qwen3-0.6b_text_none"), task)["pool"]
    qs = sorted(a)
    x, yv = np.array([b[q] for q in qs]), np.array([a[q] for q in qs])
    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    ax.plot([0, 1], [0, 1], color="#bbbbbb", linewidth=1)
    ax.scatter(x, yv, s=26, color=OURS, alpha=0.6, edgecolor="white", linewidth=0.6)
    better, worse = int((yv > x + 1e-9).sum()), int((yv < x - 1e-9).sum())
    ax.text(0.03, 0.95, f"E4 better: {better}", fontsize=8.5, color=INK, transform=ax.transAxes)
    ax.text(0.97, 0.05, f"E4 worse: {worse}", fontsize=8.5, color=INK, ha="right", transform=ax.transAxes)
    ax.text(0.97, 0.12, f"tied: {len(qs) - better - worse} (mostly both 0)", fontsize=8.5, color=MUTED, ha="right",
            transform=ax.transAxes)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel("Qwen3-0.6B text, nDCG@10 (pooled)", fontsize=9, color=MUTED)
    ax.set_ylabel("E4 text + profiles, nDCG@10 (pooled)", fontsize=9, color=MUTED)
    ax.set_title("Math, per query", fontsize=11, color=INK, loc="left")
    style(ax)
    ax.yaxis.grid(True, color="#e6e6e6", linewidth=0.8)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_per_query_math.png", dpi=200, facecolor="white")
    print("figures:", *sorted(p.name for p in FIG.glob("*.png")))


if __name__ == "__main__":
    main()
