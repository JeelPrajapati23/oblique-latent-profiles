"""E5: re-rank the top 50 of a first-stage run with Qwen2.5-7B (listwise, sliding window 20 / step 10).

Three modes:
    # laptop: write the small top-50 input file that the Kaggle notebook ships
    python scripts/rerank.py --task math --export
    # Kaggle (vLLM): fill the window cache rerank/<task>/windows.jsonl
    python scripts/rerank.py --task math --llm
    # laptop, after unzipping the Kaggle output: rebuild the full run from the cache and evaluate
    python scripts/rerank.py --task math
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from obliq.data import load_task
from obliq.rerank import RERANK, Cache, rerank
from obliq.runs import load_run, mask, save_run

MODEL = "Qwen/Qwen2.5-7B-Instruct-AWQ"
DECODING = "greedy-maxtok256"  # no frequency penalty: the answer repeats "[", "]" and ">" by design
FIRST_STAGE = "E4_RRF_all_4_k_60"  # main system (equal-weight RRF over the four indexes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=["math", "writing"])
    ap.add_argument("--run", default=FIRST_STAGE)
    ap.add_argument("--top", type=int, default=50)
    ap.add_argument("--export", action="store_true", help="write the top-n input file for Kaggle")
    ap.add_argument("--llm", action="store_true", help="generate missing windows with vLLM")
    args = ap.parse_args()
    task = load_task(args.task)
    inp = RERANK / args.task / f"input_{args.run}_top{args.top}.json"

    if args.export:
        run = load_run(args.task, args.run)
        top = {q: dict(sorted(d.items(), key=lambda x: -x[1])[:args.top]) for q, d in run.items()}
        inp.parent.mkdir(parents=True, exist_ok=True)
        inp.write_text(json.dumps(top))
        print(f"wrote {inp} ({len(top)} queries)")
        return

    cache = Cache(RERANK / args.task / "windows.jsonl")
    generate = None
    if args.llm:
        from vllm import SamplingParams
        from obliq.profiles import VLLMBackend
        backend = VLLMBackend(MODEL, max_model_len=8192)
        backend.params = SamplingParams(temperature=0.0, max_tokens=256)
        generate = backend.generate
        run = json.loads(inp.read_text())  # Kaggle has only the top-n file
    else:
        run = load_run(args.task, args.run)

    t0 = time.time()
    out, stats = rerank(task, run, cache, MODEL, DECODING, generate, top=args.top)
    secs = time.time() - t0
    print(f"windows {stats['windows']}, generated {stats['generated']} in {secs / 60:.1f} min, "
          f"ids missing from answers {stats['missing_ids']} "
          f"({stats['missing_ids'] / max(stats['windows'] * 20, 1):.1%} of slots)")
    if stats["generated"]:
        with open(RERANK / args.task / "cost.jsonl", "a") as f:
            f.write(json.dumps({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "run": args.run, "top": args.top,
                                "queries": len(run), "generated": stats["generated"], "seconds": round(secs, 1),
                                "gpus": 1}) + "\n")
    if not args.llm:
        name = f"E5_rerank_top{args.top}_{args.run}"
        save_run(mask(out, task.excluded, 1000), args.task, name)
        print(f"saved runs/{args.task}/{name}.json")


if __name__ == "__main__":
    main()
