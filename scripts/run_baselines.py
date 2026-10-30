"""E1: reproduce the paper's BM25 and Qwen3-Embedding-0.6B rows on raw text.

    python scripts/run_baselines.py --tasks math writing --systems bm25 dense
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from obliq.data import load_task
from obliq.evaluate import evaluate_run, format_row, header
from obliq.retrievers import bm25_search, dense_search, encode
from obliq.runs import mask, save_run

K = 1000
QWEN = "Qwen/Qwen3-Embedding-0.6B"

# Paper Table 3 (nDCG@10, nDCG@50, R@10, R@50, R@100). Math is gold/pooled; Writing single gold.
PAPER = {
    "math": {"bm25": ".022/.029  .034/.025  .020/.029  .060/.029  .088/.029",
             "qwen3-0.6b": ".116/.143  .149/.176  .070/.088  .219/.247  .309/.336"},
    "writing": {"bm25": ".077  .114  .062  .154  .208",
                "qwen3-0.6b": ".046  .060  .040  .075  .103"},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", nargs="+", default=["math", "writing"])
    ap.add_argument("--systems", nargs="+", default=["bm25", "dense"])
    ap.add_argument("--bm25-tok", nargs="+", default=["lower"])
    ap.add_argument("--qprompt", nargs="+", default=["query"], help="'query' or 'none'")
    ap.add_argument("--max-len", type=int, default=2048)
    args = ap.parse_args()

    for name in args.tasks:
        task = load_task(name)
        # Over-fetch so masking never leaves fewer than K results.
        k_fetch = K + max((len(v) for v in task.excluded.values()), default=0)
        print(f"\n== {name}: {len(task.corpus)} docs, {len(task.queries)} queries")
        rows = []
        if "bm25" in args.systems:
            for tok in args.bm25_tok:
                run = mask(bm25_search(task.corpus, task.queries, k_fetch, tok), task.excluded, K)
                sysname = f"bm25_text_{tok}"
                save_run(run, name, sysname)
                rows.append((sysname, evaluate_run(run, task)))
        if "dense" in args.systems:
            d_ids, d_emb = encode(task.corpus, f"{name}_corpus_qwen3-0.6b_L{args.max_len}", QWEN,
                                  max_len=args.max_len)
            for qp in args.qprompt:
                q_ids, q_emb = encode(task.queries, f"{name}_queries_qwen3-0.6b_{qp}_L{args.max_len}",
                                      QWEN, prompt_name=None if qp == "none" else qp,
                                      max_len=args.max_len)
                run = mask(dense_search(d_ids, d_emb, q_ids, q_emb, k_fetch), task.excluded, K)
                sysname = f"qwen3-0.6b_text_{qp}"
                save_run(run, name, sysname)
                rows.append((sysname, evaluate_run(run, task)))

        print(header())
        for sysname, res in rows:
            print(format_row(sysname, res))
        for sysname, ref in PAPER[name].items():
            print(f"{'paper:' + sysname:<28}" + "  ".join(f"{c:>11}" for c in ref.split()))


if __name__ == "__main__":
    main()
