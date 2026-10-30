"""E3 (profile-only retrieval) and E4 (RRF over text + profile indexes).

Indexes: BM25-text and dense-text reuse the E1 run files; BM25-profile and dense-profile are built
here from the cached LLM profiles. Every choice (BM25 tokenizer, dense query prompt, fusion weights)
is made on the fixed 20% dev split (splits/<task>.json) and reported on the other 80% and on all
queries. Paired t-tests on test queries compare each system with the best E1 baseline.

    python scripts/run_profiles.py --tasks writing math
"""
import argparse
import itertools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from scipy.stats import ttest_rel

from obliq.data import ROOT, load_task
from obliq.evaluate import METRICS, evaluate_run, per_query
from obliq.fusion import dev_split, rrf
from obliq.profiles import VLLMBackend, load_profiles, variant_name
from obliq.retrievers import bm25_search, dense_search, encode
from obliq.runs import load_run, mask, run_path, save_run

K = 1000
QWEN = "Qwen/Qwen3-Embedding-0.6B"
LLM = "Qwen/Qwen2.5-7B-Instruct-AWQ"
SETTINGS = {"writing": ["writing"], "math": ["math", "math_soln"]}
# Paper's best single-stage retriever (Gemini-2-Embedding, nDCG@10): the number to beat.
TARGET = {"writing": ".164", "math": ".147 (pooled)"}
GRID = [0, 0.5, 1, 2]


def pick(cands: dict, task, dev):
    """Name of the candidate run with the best dev nDCG@10 (gold qrels)."""
    return max(cands, key=lambda n: evaluate_run(cands[n], task, ["ndcg@10"], dev)["gold"]["ndcg@10"])


def profile_runs(task, setting, k_fetch):
    """BM25 and dense runs over profiles. math_soln shares Math's query profiles (same prompt)."""
    dv = variant_name(setting, LLM, VLLMBackend.decoding)
    qv = variant_name(task.name, LLM, VLLMBackend.decoding)
    docs, queries = load_profiles(task.name, dv, "doc"), load_profiles(task.name, qv, "query")
    assert set(docs) == set(task.corpus) and set(queries) == set(task.queries), "profiles incomplete"
    tag = "" if setting == task.name else "soln_"
    runs = {}
    for tok in ["word", "lower"]:
        name = f"{tag}bm25_profile_{tok}"
        if not run_path(task.name, name).exists():
            save_run(mask(bm25_search(docs, queries, k_fetch, tok), task.excluded, K), task.name, name)
        runs[name] = load_run(task.name, name)
    d_ids, d_emb = encode(docs, f"{task.name}_docprof_{dv.split('__')[0]}_qwen3-0.6b_L512", QWEN,
                          max_len=512, batch_size=32)
    for qp in ["none", "query"]:
        name = f"{tag}qwen3-0.6b_profile_{qp}"
        if not run_path(task.name, name).exists():
            q_ids, q_emb = encode(queries, f"{task.name}_qprof_{qv.split('__')[0]}_qwen3-0.6b_{qp}_L512", QWEN,
                                  prompt_name=None if qp == "none" else qp, max_len=512, batch_size=32)
            save_run(mask(dense_search(d_ids, d_emb, q_ids, q_emb, k_fetch), task.excluded, K), task.name, name)
        runs[name] = load_run(task.name, name)
    return runs


def tune_weights(comp: list, task, dev):
    """Grid-search one RRF weight per component on dev queries only."""
    dev_runs = [{q: r[q] for q in dev if q in r} for r in comp]
    best, best_w = -1, None
    for w in itertools.product(GRID, repeat=len(comp)):
        if not any(w):
            continue
        s = evaluate_run(rrf(dev_runs, weights=list(w)), task, ["ndcg@10"], dev)["gold"]["ndcg@10"]
        if s > best + 1e-9:
            best, best_w = s, list(w)
    return best_w


def fmt(res, m):
    return "/".join(f"{res[k][m]:.3f}" for k in ("gold", "pool") if k in res)


def report(task, rows, dev, test, baseline):
    """Markdown table: all-query metrics, dev/test nDCG@10, and paired t-test vs baseline on test."""
    pq_base = per_query(rows[baseline], task, qids=test)
    labels = "gold/pool" if task.qrels_pool else "gold"
    out = [f"| system | " + " | ".join(METRICS) + f" | dev nDCG@10 | test nDCG@10 | p vs {baseline} (test) |",
           "|---" * (len(METRICS) + 4) + "|"]
    for name, run in rows.items():
        a, d, t = (evaluate_run(run, task, qids=s) for s in (None, dev, test))
        pq = per_query(run, task, qids=test)
        ps = []
        for k in pq:
            qs = sorted(pq[k])
            x, y = [pq[k][q] for q in qs], [pq_base[k][q] for q in qs]
            ps.append("-" if name == baseline else f"{ttest_rel(x, y).pvalue:.3g}{'+' if sum(x) > sum(y) else '-'}")
        out.append(f"| {name} | " + " | ".join(fmt(a, m) for m in METRICS)
                   + f" | {fmt(d, 'ndcg@10')} | {fmt(t, 'ndcg@10')} | {'/'.join(ps)} |")
    return out, labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", nargs="+", default=["writing", "math"])
    args = ap.parse_args()
    for name in args.tasks:
        task = load_task(name)
        k_fetch = K + max((len(v) for v in task.excluded.values()), default=0)
        dev, test = dev_split(name, task.qrels)
        print(f"\n== {name}: dev {len(dev)} / test {len(test)} queries")

        text = {n: load_run(name, n) for n in
                ["bm25_text_split", "bm25_text_lower", "bm25_text_word", "qwen3-0.6b_text_none", "qwen3-0.6b_text_query"]}
        bt = pick({n: r for n, r in text.items() if n.startswith("bm25")}, task, dev)
        dt = pick({n: r for n, r in text.items() if n.startswith("qwen")}, task, dev)
        baseline = pick({bt: text[bt], dt: text[dt]}, task, dev)  # best E1 single retriever on dev
        rows = {f"E1 {bt}": text[bt], f"E1 {dt}": text[dt]}
        notes = [f"- Text components picked on dev: `{bt}`, `{dt}`; significance baseline: `{baseline}`."]

        for setting in SETTINGS[name]:
            pr = profile_runs(task, setting, k_fetch)
            bp = pick({n: r for n, r in pr.items() if "bm25" in n}, task, dev)
            dp = pick({n: r for n, r in pr.items() if "qwen" in n}, task, dev)
            tag = "" if setting == name else " [soln variant]"
            comp = [text[bt], text[dt], pr[bp], pr[dp]]
            w = tune_weights(comp, task, dev)
            runs = {
                f"E3 {bp}{tag}": pr[bp],
                f"E3 {dp}{tag}": pr[dp],
                f"E3 RRF profile (BM25-p + dense-p){tag}": rrf([pr[bp], pr[dp]]),
                f"E4 RRF all 4 (k=60){tag}": rrf(comp),
                f"E4 weighted RRF all 4 w={w}{tag}": rrf(comp, weights=w),
            }
            if setting == name:  # control: is the E4 gain from profiles, or just from fusing two text runs?
                rows["RRF text only (BM25-t + dense-t)"] = rrf([text[bt], text[dt]])
            for n, r in runs.items():
                save_run(r, name, re.sub(r"[^\w.-]+", "_", n.split(" w=")[0]).strip("_"))
            rows.update(runs)
            notes.append(f"- {setting}: profile components picked on dev: `{bp}`, `{dp}`; "
                         f"weights (BM25-t, dense-t, BM25-p, dense-p) tuned on dev: {w}.")

        baseline_key = f"E1 {baseline}"
        table, labels = report(task, rows, dev, test, baseline_key)
        lines = [f"# E3/E4 results: {name}", "",
                 f"All numbers masked. Cells are {labels}. Paper's best single-stage retriever "
                 f"(Gemini-2-Embedding) nDCG@10 = {TARGET[name]}.", "",
                 f"Dev = fixed 20% split ({len(dev)} queries, `splits/{name}.json`), test = other {len(test)}. "
                 f"p = paired t-test on test nDCG@10 vs `{baseline_key}`; +/- = better/worse on average. "
                 "Claim a win only at p < 0.05.", "", *notes, "", *table]
        if name == "math":
            lines += ["", "The `[soln variant]` rows profile documents together with their solutions. The "
                      "paper's retrievers never saw solutions, so these rows are not the headline number."]
        out = ROOT / "reports" / f"e3_e4_{name}.md"
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(lines))
        print(f"\nreport: {out}")


if __name__ == "__main__":
    main()
