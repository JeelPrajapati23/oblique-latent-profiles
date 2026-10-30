"""E2: query-side rewriting with the same open LLM (Qwen2.5-7B), then Qwen3-0.6B dense retrieval over
the raw corpus, mirroring the paper's GPT-5.2 rewriter + Gemini pipeline. Answers RQ4: does
document-side profiling (E4) beat query-side rewriting with the same LLM?

Rewrites come from the Kaggle notebook (build_kaggle_notebook.py --rewrite) and are cached like
profiles under profiles/<task>/<task>_rewrite-*/queries.jsonl.

    python scripts/run_rewrite.py --tasks math writing   ->  reports/e2_<task>.md
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from scipy.stats import ttest_rel

from obliq.data import ROOT, load_task
from obliq.evaluate import METRICS, evaluate_run, per_query
from obliq.fusion import dev_split
from obliq.profiles import VLLMBackend, load_profiles, variant_name
from obliq.retrievers import dense_search, encode
from obliq.runs import load_run, mask, run_path, save_run

K = 1000
QWEN = "Qwen/Qwen3-Embedding-0.6B"
LLM = "Qwen/Qwen2.5-7B-Instruct-AWQ"
BASELINE = {"math": "qwen3-0.6b_text_none", "writing": "bm25_text_split"}  # best E1 run on dev
PAPER = {"math": "Gemini .147 -> GPT-5.2 rewriter + Gemini .185 (pooled)",
         "writing": "Gemini .164 -> GPT-5.2 rewriter + Gemini .018"}
_PREFIX = re.compile(r"^\s*(\*\*)?(rewritten query|query|rewrite)(\*\*)?\s*:\s*", re.I)


def parse_rewrite(text: str) -> tuple[str, bool]:
    """Pull the rewritten query out of the LLM answer. Writing answers are JSON
    ({"rewritten_query": ..., "rationale": ...}); Math answers are plain text, sometimes prefixed.
    Returns (query, parsed_ok); falls back to the whole answer."""
    m = re.search(r'"rewritten_query"\s*:\s*"((?:[^"\\]|\\.)*)"', text, re.S)
    if m:
        try:
            return json.loads(f'"{m.group(1)}"'), True
        except json.JSONDecodeError:
            return m.group(1), True
    m = re.search(r'"rewritten_query"\s*:\s*"(.*)', text, re.S)
    if m:  # answer hit the token cap inside the string: keep the partial rewrite, drop the JSON wrapper
        return m.group(1).replace('\\"', '"'), False
    return _PREFIX.sub("", text.strip().strip('"')).strip(), True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", nargs="+", default=["math", "writing"])
    args = ap.parse_args()
    for name in args.tasks:
        task = load_task(name)
        dev, test = dev_split(name, task.qrels)
        k_fetch = K + max((len(v) for v in task.excluded.values()), default=0)
        v = variant_name(f"{name}_rewrite", LLM, VLLMBackend.decoding)
        raw = load_profiles(name, v, "query")
        assert set(raw) == set(task.queries), f"rewrites incomplete in {v}: {len(raw)}/{len(task.queries)}"
        parsed = {q: parse_rewrite(t) for q, t in raw.items()}
        rewrites = {q: p[0] for q, p in parsed.items()}
        bad = sum(not p[1] for p in parsed.values())

        d_ids, d_emb = encode(task.corpus, f"{name}_corpus_qwen3-0.6b_L2048", QWEN, max_len=2048)
        cands = {}
        for qp in ["none", "query"]:
            sysname = f"E2_rewrite_qwen3-0.6b_{qp}"
            if not run_path(name, sysname).exists():
                q_ids, q_emb = encode(rewrites, f"{name}_rewrite_{v.split('__')[0]}_qwen3-0.6b_{qp}_L512", QWEN,
                                      prompt_name=None if qp == "none" else qp, max_len=512)
                save_run(mask(dense_search(d_ids, d_emb, q_ids, q_emb, k_fetch), task.excluded, K), name, sysname)
            cands[sysname] = load_run(name, sysname)
        e2 = max(cands, key=lambda n: evaluate_run(cands[n], task, ["ndcg@10"], dev)["gold"]["ndcg@10"])

        rows = {f"E1 {BASELINE[name]} (best baseline)": load_run(name, BASELINE[name])}
        if BASELINE[name] != "qwen3-0.6b_text_none":  # same retriever as E2, original query
            rows["E1 qwen3-0.6b_text_none (E2's retriever, original query)"] = load_run(name, "qwen3-0.6b_text_none")
        rows[f"E2 {e2}"] = cands[e2]
        rows["E4 RRF all 4 (main)"] = load_run(name, "E4_RRF_all_4_k_60")
        base_key = next(iter(rows))
        pb = per_query(rows[base_key], task, qids=test)
        pe2 = per_query(cands[e2], task, qids=test)

        def ptest(pa, pref):
            cells = []
            for k in pa:
                qs = sorted(pa[k])
                x, y = [pa[k][q] for q in qs], [pref[k][q] for q in qs]
                cells.append(f"{ttest_rel(x, y).pvalue:.3g}{'+' if sum(x) > sum(y) else '-'}")
            return "/".join(cells)

        f = lambda r, m: "/".join(f"{r[k][m]:.3f}" for k in ("gold", "pool") if k in r)
        table = [f"| system | " + " | ".join(METRICS) + " | test nDCG@10 | p vs best E1 (test) | p vs E2 (test) |",
                 "|---" * (len(METRICS) + 4) + "|"]
        for label, run in rows.items():
            a, t = evaluate_run(run, task), evaluate_run(run, task, qids=test)
            pr = per_query(run, task, qids=test)
            table.append(f"| {label} | " + " | ".join(f(a, m) for m in METRICS) + f" | {f(t, 'ndcg@10')} | "
                         f"{'-' if label == base_key else ptest(pr, pb)} | "
                         f"{'-' if label.startswith('E2') else ptest(pr, pe2)} |")
        ex = sorted(task.queries)[:3]
        lines = [f"# E2 query rewriting: {name}", "",
                 f"Rewriter: `{LLM}` (same LLM and decoding as the profiles), prompt `prompts/rewrite_{name}.txt`"
                 + (" (the paper's authorship rewriter prompt, verbatim)." if name == "writing" else
                    " (the paper gives no Math rewriter prompt; this follows its Twitter rewriter template)."),
                 f"Retriever: Qwen3-Embedding-0.6B over raw text; query prompt chosen on dev: `{e2}`.",
                 f"Answers cut off by the 220-token cap before the JSON closed (partial rewrite used): {bad}/{len(raw)}.",
                 f"Paper, same comparison: {PAPER[name]}.", "",
                 f"All numbers masked; cells are {'gold/pool' if task.qrels_pool else 'gold'}. Test = the fixed 80% "
                 "split. p = paired t-test on test nDCG@10; +/- = better/worse on average.", "", *table, "",
                 "## Example rewrites", ""]
        for q in ex:
            lines += [f"**{q}**: {' '.join(rewrites[q].split())[:500]}", ""]
        out = ROOT / "reports" / f"e2_{name}.md"
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(lines))


if __name__ == "__main__":
    main()
