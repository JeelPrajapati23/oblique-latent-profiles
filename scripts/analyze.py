"""Week 3 analysis for one task: cost table, win/tie/loss, and the 10 queries where the main system
(E4) helped most / hurt most versus the best E1 baseline, with query and document profiles.

    python scripts/analyze.py --task math     ->  reports/analysis_math.md
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from obliq.data import ROOT, load_task
from obliq.evaluate import evaluate_run, per_query
from obliq.fusion import dev_split, rrf
from obliq.profiles import PROFILES, VLLMBackend, load_profiles, strip_math_query, variant_name
from obliq.rerank import RERANK
from obliq.retrievers import CACHE, TOKENIZERS
from obliq.runs import load_run, run_path

LLM = "Qwen/Qwen2.5-7B-Instruct-AWQ"
BASELINE = {"math": "qwen3-0.6b_text_none", "writing": "bm25_text_split"}  # best E1 run on dev (run_profiles.py)
MAIN = "E4_RRF_all_4_k_60"
COMPONENTS = {"math": ["bm25_text_word", "qwen3-0.6b_text_none", "bm25_profile_word", "qwen3-0.6b_profile_query"],
              "writing": ["bm25_text_split", "qwen3-0.6b_text_none", "bm25_profile_word", "qwen3-0.6b_profile_query"]}


def short(text, n=300):
    text = " ".join(text.split())
    return text[:n] + ("..." if len(text) > n else "")


def cost_section(task):
    lines = ["## Cost", "", "| Step | Items | Wall time | GPU-minutes | GPU-seconds per item |", "|---|---|---|---|---|"]
    for vdir in sorted((PROFILES / task.name).glob("*__*")):
        cost = vdir / "cost.jsonl"
        if not cost.exists():
            continue
        for r in map(json.loads, open(cost)):
            if r["limit"]:
                continue  # timing pilot; its items are part of the full run's total below
            label = f"Profile {r['setting']} ({'+'.join(r['kinds'])}) on {r['gpus']}x {r['gpu']}"
            lines.append(f"| {label} | {r['generated']} | {r['seconds'] / 60:.1f} min | "
                         f"{r['seconds'] * r['gpus'] / 60:.1f} | {r['seconds'] * r['gpus'] / r['generated']:.2f} |")
    rc = RERANK / task.name / "cost.jsonl"
    if rc.exists():
        for r in map(json.loads, open(rc)):
            lines.append(f"| E5 re-rank top {r['top']} ({r['queries']} queries) | {r['generated']} windows | "
                         f"{r['seconds'] / 60:.1f} min | {r['seconds'] * r['gpus'] / 60:.1f} | "
                         f"{r['seconds'] * r['gpus'] / r['queries']:.2f} per query |")
    lines += ["", "GPU-seconds per item is batched throughput on Kaggle T4s (includes vLLM start-up), not "
              "single-request latency. Profiling is a one-off, offline cost per corpus.", ""]
    return lines


def latency_section(task, prof_docs, prof_queries):
    """Online cost per query on the laptop, excluding the LLM call that profiles the query."""
    from rank_bm25 import BM25Okapi
    import faiss
    qids = sorted(task.queries)
    tok = TOKENIZERS["word"]
    t = {}
    for label, docs, queries in [("BM25 text", task.corpus, task.queries), ("BM25 profile", prof_docs, prof_queries)]:
        ids = list(docs)
        bm = BM25Okapi([tok(docs[d]) for d in ids])
        t0 = time.perf_counter()
        for q in qids:
            bm.get_scores(tok(queries[q]))
        t[label] = (time.perf_counter() - t0) / len(qids)
    for label, name in [("Dense text (FAISS search)", f"{task.name}_corpus_qwen3-0.6b_L2048"),
                        ("Dense profile (FAISS search)", None)]:
        if name is None:
            name = next(p.stem for p in (CACHE / "emb").glob(f"{task.name}_docprof_{task.name}-*_L512.npy"))
        emb = np.load(CACHE / "emb" / f"{name}.npy")
        index = faiss.IndexFlatIP(emb.shape[1])
        index.add(emb)
        qs = emb[:len(qids)]  # stand-in query vectors; search cost doesn't depend on their values
        t0 = time.perf_counter()
        for i in range(len(qids)):
            index.search(qs[i:i + 1], 1000)
        t[label] = (time.perf_counter() - t0) / len(qids)
    runs = [load_run(task.name, n) for n in COMPONENTS[task.name]]
    t0 = time.perf_counter()
    rrf(runs)
    t["RRF of 4 lists"] = (time.perf_counter() - t0) / len(qids)
    lines = ["## Online latency per query (laptop CPU, after the query is profiled)", "",
             "| Step | ms per query |", "|---|---|"]
    lines += [f"| {k} | {v * 1000:.1f} |" for k, v in t.items()]
    lines += [f"| **Total** | **{sum(t.values()) * 1000:.1f}** |", "",
              "Not included: encoding the query and its profile with Qwen3-0.6B (one forward pass each) and "
              "the LLM call that writes the query profile (~100 output tokens; a few seconds on one T4).", ""]
    return lines


def examples_section(task, base, main, prof_docs, prof_queries, n=10):
    pb, pm = per_query(base, task), per_query(main, task)
    label = "pool" if "pool" in pm else "gold"  # Math headline metric is pooled, as in the paper
    other = "gold" if label == "pool" else None
    qids = sorted(pm[label])
    delta = {q: pm[label][q] - pb[label][q] for q in qids}
    tie_key = (lambda q: pm[other][q] - pb[other][q]) if other else (lambda q: 0)
    wins, losses = sum(d > 1e-9 for d in delta.values()), sum(d < -1e-9 for d in delta.values())
    rel = task.qrels_pool if label == "pool" else task.qrels
    lines = ["## Where profiles help and hurt", "",
             f"Per-query nDCG@10 ({label}) of `{MAIN}` vs `{BASELINE[task.name]}`, all {len(qids)} queries: "
             f"**{wins} better, {losses} worse, {len(qids) - wins - losses} tied** "
             f"(ties are mostly queries where both systems score 0).", ""]

    def rank_of(run, q, d):
        order = list(dict(sorted(run[q].items(), key=lambda x: -x[1])))
        return order.index(d) + 1 if d in order else None

    for title, sel in [("Helped most", sorted(qids, key=lambda q: (-delta[q], -tie_key(q)))[:n]),
                       ("Hurt most", sorted(qids, key=lambda q: (delta[q], tie_key(q)))[:n])]:
        lines += [f"### {title}", ""]
        for q in sel:
            qtext = strip_math_query(task.queries[q]) if task.name == "math" else task.queries[q]
            rels = set(rel.get(q, {}))
            lines += [f"**{q}**: nDCG@10 {pb[label][q]:.3f} -> {pm[label][q]:.3f} ({delta[q]:+.3f})", "",
                      f"> {short(qtext)}", "", f"Query profile: {short(prof_queries[q], 600)}", ""]
            if not rels:
                continue
            if title == "Helped most":  # the relevant doc E4 lifted highest, and where the baseline had it
                d = min(rels, key=lambda d: rank_of(main, q, d) or 10**6)
                lines += [f"Relevant doc `{d}`: rank {rank_of(base, q, d)} (baseline) -> {rank_of(main, q, d)} (E4)", "",
                          f"> {short(task.corpus[d])}", "", f"Doc profile: {short(prof_docs[d], 600)}", ""]
            else:  # the relevant doc the baseline ranked highest, and E4's non-relevant top hit
                d = min(rels, key=lambda d: rank_of(base, q, d) or 10**6)
                top = max(main[q], key=main[q].get)
                lines += [f"Relevant doc `{d}`: rank {rank_of(base, q, d)} (baseline) -> {rank_of(main, q, d)} (E4)", "",
                          f"E4's top hit `{top}` ({'relevant' if top in rels else 'not relevant'}):", "",
                          f"> {short(task.corpus[top])}", "", f"Its profile: {short(prof_docs[top], 600)}", ""]
    return lines


def results_section(task, dev, test):
    rows = [("E1 " + BASELINE[task.name], BASELINE[task.name]), ("E4 RRF all 4 (main)", MAIN)]
    e5 = f"E5_rerank_top50_{MAIN}"
    if run_path(task.name, e5).exists():
        rows.append(("E5 = E4 + LLM re-rank top 50", e5))
    from scipy.stats import ttest_rel
    base = load_run(task.name, BASELINE[task.name])
    lines = ["## Headline numbers (masked; gold/pooled for Math)", "",
             "| system | nDCG@10 all | nDCG@10 test | R@50 all | R@100 all | p vs E1 (test) |", "|---|---|---|---|---|---|"]
    for label, name in rows:
        run = load_run(task.name, name)
        a, t = evaluate_run(run, task), evaluate_run(run, task, qids=test)
        ps = []
        if name != BASELINE[task.name]:
            pr, pb = per_query(run, task, qids=test), per_query(base, task, qids=test)
            for k in pr:
                qs = sorted(pr[k])
                ps.append(f"{ttest_rel([pr[k][q] for q in qs], [pb[k][q] for q in qs]).pvalue:.3g}")
        f = lambda r, m: "/".join(f"{r[k][m]:.3f}" for k in ("gold", "pool") if k in r)
        lines.append(f"| {label} | {f(a, 'ndcg@10')} | {f(t, 'ndcg@10')} | {f(a, 'recall@50')} | "
                     f"{f(a, 'recall@100')} | {'/'.join(ps) or '-'} |")
    if run_path(task.name, e5).exists():  # E5 only reorders E4's top 50, so test it against E4 directly
        pa, pb = per_query(load_run(task.name, e5), task), per_query(load_run(task.name, MAIN), task)
        cells = []
        for k in pa:
            qs = sorted(pa[k])
            x, y = [pa[k][q] for q in qs], [pb[k][q] for q in qs]
            cells.append(f"{k}: {sum(a > b + 1e-9 for a, b in zip(x, y))} better / "
                         f"{sum(a < b - 1e-9 for a, b in zip(x, y))} worse, p = {ttest_rel(x, y).pvalue:.3g}")
        lines += ["", f"E5 vs E4, all queries, nDCG@10: {'; '.join(cells)}. Recall@50/100 are equal by "
                  "construction (only the top 50 is reordered)."]
    lines += ["", "Paper reference (nDCG@10, Math pooled): Gemini-2-Embedding .147, GPT-5.2 rewriter + Gemini .185, "
              "GPT-5.2 multi-hop agent .207, oracle GPT-5.2 re-ranker with gold injected .329.", ""]
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default="math", choices=["math", "writing"])
    args = ap.parse_args()
    task = load_task(args.task)
    dev, test = dev_split(args.task, task.qrels)
    v = variant_name(args.task, LLM, VLLMBackend.decoding)
    prof_docs, prof_queries = load_profiles(args.task, v, "doc"), load_profiles(args.task, v, "query")
    base, main_run = load_run(args.task, BASELINE[args.task]), load_run(args.task, MAIN)
    lines = [f"# Week 3 analysis: {args.task}", "", "All runs masked with `per_query_excluded_ids.json`.", ""]
    lines += results_section(task, dev, test)
    lines += cost_section(task)
    lines += latency_section(task, prof_docs, prof_queries)
    lines += examples_section(task, base, main_run, prof_docs, prof_queries)
    out = ROOT / "reports" / f"analysis_{args.task}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:60]))
    print(f"\nreport: {out}")


if __name__ == "__main__":
    main()
