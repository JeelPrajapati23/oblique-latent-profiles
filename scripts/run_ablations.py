"""Ablations A1-A3 on Math: does each profiling choice matter for E3/E4?

Each variant is plugged into exactly the main system's components (BM25-profile `word`, Qwen3
dense-profile with the `query` prompt, equal-weight RRF with BM25-text `word` + Qwen3-text `none`);
nothing is re-tuned, so the only difference is the profiles. p = paired t-test on test nDCG@10 vs
the main E4. Variants whose profiles are missing are skipped (run kaggle/ablation.ipynb first).

    python scripts/run_ablations.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
from scipy.stats import ttest_rel

from obliq.data import ROOT, load_task
from obliq.evaluate import per_query
from obliq.fusion import dev_split, rrf
from obliq.profiles import PROFILES, VLLMBackend, load_profiles, variant_name
from obliq.retrievers import bm25_search, dense_search, encode
from obliq.runs import load_run, mask, run_path, save_run
from run_profiles import K, LLM, QWEN, report

VARIANTS = {  # label -> (setting, model)
    "main (7B, no topic, 60-100 words)": ("math", LLM),
    "A1 topic words allowed": ("math_topic", LLM),
    "A2 3B profiler": ("math", "Qwen/Qwen2.5-3B-Instruct-AWQ"),
    "A3 ~40-word profiles": ("math_short", LLM),
}
# The topic words the main prompt bans by example; share of profiles using any = topic leak rate.
TOPIC = re.compile(r"\b(triangle|polynomial|matri(x|ces)|primes?|graphs?|integrals?|sequences?)\b", re.I)


def runs_for(task, tag, docs, queries, k_fetch, vname):
    bname, dname = f"A_{tag}_bm25_profile_word", f"A_{tag}_qwen3-0.6b_profile_query"
    if not run_path(task.name, bname).exists():
        save_run(mask(bm25_search(docs, queries, k_fetch, "word"), task.excluded, K), task.name, bname)
    if not run_path(task.name, dname).exists():
        d_ids, d_emb = encode(docs, f"math_docprof_{vname}_qwen3-0.6b_L512", QWEN, max_len=512, batch_size=32)
        q_ids, q_emb = encode(queries, f"math_qprof_{vname}_qwen3-0.6b_query_L512", QWEN, prompt_name="query",
                              max_len=512, batch_size=32)
        save_run(mask(dense_search(d_ids, d_emb, q_ids, q_emb, k_fetch), task.excluded, K), task.name, dname)
    return load_run(task.name, bname), load_run(task.name, dname)


def gpu_minutes(vdir: Path):
    cost = vdir / "cost.jsonl"
    if not cost.exists():
        return None
    return sum(r["seconds"] * r["gpus"] / 60 for r in map(json.loads, cost.read_text().splitlines()) if r["limit"] == 0)


def main():
    task = load_task("math")
    k_fetch = K + max((len(v) for v in task.excluded.values()), default=0)
    dev, test = dev_split("math", task.qrels)
    text = [load_run("math", "bm25_text_word"), load_run("math", "qwen3-0.6b_text_none")]
    rows, stats = {}, []
    for label, (setting, model) in VARIANTS.items():
        vname = variant_name(setting, model, VLLMBackend.decoding)
        docs, queries = load_profiles("math", vname, "doc"), load_profiles("math", vname, "query")
        if set(docs) != set(task.corpus) or set(queries) != set(task.queries):
            print(f"skip {label}: {vname} has {len(docs)}/{len(task.corpus)} docs, "
                  f"{len(queries)}/{len(task.queries)} queries")
            continue
        tag = vname.split("__")[0] + ("" if model == LLM else "_" + model.split("/")[-1].split("-")[1])
        bp, dp = runs_for(task, tag, docs, queries, k_fetch, tag)
        rows[f"{label}: E3 RRF profile"] = rrf([bp, dp])
        rows[f"{label}: E4 RRF all 4"] = e4 = rrf(text + [bp, dp])
        save_run(e4, "math", f"A_{tag}_E4_RRF_all_4")
        words = np.mean([len(p.split()) for p in docs.values()])
        leak = np.mean([bool(TOPIC.search(p)) for p in docs.values()])
        gm = gpu_minutes(PROFILES / "math" / vname)
        stats.append(f"| {label} | `{vname}` | {words:.0f} | {leak:.0%} | {f'{gm:.0f}' if gm else '-'} |")

    base = "main (7B, no topic, 60-100 words): E4 RRF all 4"
    table, labels = report(task, rows, dev, test, base)
    lines = ["# Ablations A1-A3 (Math)", "",
             f"All numbers masked, cells {labels}. Components fixed to the main system's (no re-tuning). "
             f"Dev = {len(dev)} / test = {len(test)} queries; p = paired t-test on test nDCG@10 vs `{base}`.", "",
             "| variant | cache | mean words / doc profile | doc profiles with a banned topic word | GPU-min |",
             "|---|---|---|---|---|", *stats, "", *table]
    # profile-only effect: each variant's E3 vs the main E3 (E4 dilutes it with the two text runs)
    e3 = {k.split(":")[0]: r for k, r in rows.items() if k.endswith("E3 RRF profile")}
    main_label = next(iter(VARIANTS))
    if main_label in e3:
        base = per_query(e3[main_label], task, qids=test)
        lines += ["", "E3 (profiles only) vs main E3, test queries:", "",
                  "| variant | gold: mean vs main (p) | pool: mean vs main (p) |", "|---|---|---|"]
        for label, run in e3.items():
            if label == main_label:
                continue
            pq = per_query(run, task, qids=test)
            cells = []
            for k in pq:
                qs = sorted(pq[k])
                x, y = [pq[k][q] for q in qs], [base[k][q] for q in qs]
                cells.append(f"{np.mean(x):.3f} vs {np.mean(y):.3f} (p = {ttest_rel(x, y).pvalue:.3g})")
            lines.append(f"| {label} | " + " | ".join(cells) + " |")
    out = ROOT / "reports" / "ablations_math.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
