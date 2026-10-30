"""Week 2: profile every document and query of a task with the frozen prompts (vLLM, Kaggle 2x T4).

Runs one vLLM process per GPU, each on every n-th id, writing to its own shard file; the parent
merges shards into the cache when they finish. Already-cached ids are skipped, so a run killed
by Kaggle's time limit resumes where it stopped. Wall time per run goes to cost.jsonl in the
cache folder (GPU minutes = seconds x gpus / 60).

    python scripts/profile_corpus.py --task writing --limit 200   # timing pilot (first 200 docs)
    python scripts/profile_corpus.py --task writing               # everything
    python scripts/profile_corpus.py --task math --setting math_soln --kinds doc
    python scripts/profile_corpus.py --task math --model Qwen/Qwen2.5-3B-Instruct-AWQ   # ablation A2
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from obliq.data import load_task
from obliq.profiles import PROFILES, VLLMBackend, load_profiles, merge_shards, profile, variant_name

MODEL = "Qwen/Qwen2.5-7B-Instruct-AWQ"


def ids_for(task, kind, limit):
    # sorted so the pilot's first 200 docs are also the first 200 of the full run (no rework)
    ids = sorted(task.corpus if kind == "doc" else task.queries)
    return ids[:limit] if limit else ids


def worker(args):
    """One GPU: profile ids[shard::nshards] for each kind."""
    task = load_task(args.task)
    variant = variant_name(args.setting, args.model, VLLMBackend.decoding)
    backend = VLLMBackend(args.model)
    for kind in args.kinds:
        mine = ids_for(task, kind, args.limit)[args.shard::args.nshards]
        profile(task, kind, mine, backend, variant, args.model, args.setting, shard=args.shard)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=["math", "writing"])
    ap.add_argument("--setting", default=None, help="math_soln = Math docs profiled with solutions")
    ap.add_argument("--model", default=MODEL, help="profiler LLM (ablation A2: Qwen/Qwen2.5-3B-Instruct-AWQ)")
    ap.add_argument("--kinds", nargs="+", default=["query", "doc"], choices=["query", "doc"])
    ap.add_argument("--limit", type=int, default=0, help="only the first N ids per kind (timing pilot)")
    ap.add_argument("--gpus", type=int, default=None, help="default: all visible GPUs")
    ap.add_argument("--shard", type=int, default=None, help=argparse.SUPPRESS)
    ap.add_argument("--nshards", type=int, default=1, help=argparse.SUPPRESS)
    args = ap.parse_args()
    args.setting = args.setting or args.task
    if args.shard is not None:
        return worker(args)

    task = load_task(args.task)
    variant = variant_name(args.setting, args.model, VLLMBackend.decoding)
    vdir = PROFILES / task.name / variant
    vdir.mkdir(parents=True, exist_ok=True)  # shard logs and cost.jsonl go here before any profile exists
    for kind in args.kinds:  # fold in shards from a previous killed run before counting
        merge_shards(task.name, variant, kind)
    todo = {k: [i for i in ids_for(task, k, args.limit) if i not in load_profiles(task.name, variant, k)]
            for k in args.kinds}
    print(f"{variant}: to generate " + ", ".join(f"{k}={len(v)}" for k, v in todo.items()), flush=True)
    if not any(todo.values()):
        return

    import torch
    gpus = args.gpus or max(torch.cuda.device_count(), 1)
    t0 = time.time()
    procs = []
    for g in range(gpus):
        cmd = [sys.executable, __file__, "--task", args.task, "--setting", args.setting,
               "--model", args.model, "--kinds", *args.kinds, "--limit", str(args.limit), "--shard", str(g), "--nshards", str(gpus)]
        env = {**os.environ, "CUDA_VISIBLE_DEVICES": str(g)}
        # GPU 0 shows its progress bar here; the others log to a file
        log = None if g == 0 else open(vdir / f"shard{g}.log", "w")
        procs.append((subprocess.Popen(cmd, env=env, stdout=log, stderr=subprocess.STDOUT if log else None), log))
    codes = [p.wait() for p, _ in procs]
    for _, log in procs:
        if log:
            log.close()
    secs = time.time() - t0

    for kind in args.kinds:
        merge_shards(task.name, variant, kind)
    left = {k: sum(i not in load_profiles(task.name, variant, k) for i in ids_for(task, k, args.limit))
            for k in args.kinds}
    n = sum(len(v) for v in todo.values()) - sum(left.values())
    rec = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "setting": args.setting, "model": args.model, "kinds": args.kinds,
           "limit": args.limit, "generated": n, "seconds": round(secs, 1), "gpus": gpus,
           "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
           "exit_codes": codes}
    with open(vdir / "cost.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    # includes vLLM start-up and model load, so the pilot overstates the per-item cost a little
    print(f"\ngenerated {n} in {secs / 60:.1f} min on {gpus} GPU(s) = {secs / max(n, 1):.2f} s/item wall, "
          f"{secs * gpus / 60:.1f} GPU-min; still missing {left}", flush=True)
    if args.limit:
        total = len(task.corpus) + len(task.queries)
        print(f"extrapolated full {args.setting} ({total} items): ~{secs / max(n, 1) * total / 3600:.1f} h wall")
    if any(codes) or any(left.values()):
        sys.exit(f"incomplete: exit codes {codes}, missing {left} (re-run to resume)")


if __name__ == "__main__":
    main()
