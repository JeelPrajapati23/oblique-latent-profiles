"""E5: listwise LLM re-ranking (RankGPT-style sliding window) of a first-stage run's top results.

The window slides from the bottom of the top-n list to the top, so strong candidates can climb
all the way up. Every LLM answer is cached by a hash of its exact prompt, so re-running (or
rebuilding the run locally from a downloaded cache) never calls the LLM twice for the same window.
"""
import hashlib
import json
import re
from pathlib import Path

from .data import ROOT, Task
from .profiles import strip_math_query

RERANK = ROOT / "rerank"

INSTRUCTIONS = {
    "math": ("I will give you a query math problem and {n} candidate problems, each marked with an "
             "identifier [1] to [{n}]. Rank the candidates by how closely solving them needs the same core "
             "reasoning pattern as the query: the same key insight, proof technique or \"aha moment\". "
             "Candidates may come from completely different areas of mathematics and use different "
             "vocabulary; ignore topic and surface similarity."),
    "writing": ("I will give you a query passage and {n} candidate passages, each marked with an identifier "
                "[1] to [{n}]. Rank the candidates by how likely they were written by the same author as "
                "the query, judging only writing style (voice, sentence rhythm, punctuation, tone, verbal "
                "habits). The passages are about different topics; ignore topic similarity."),
}
LABELS = {"math": ("Query problem", "Candidate problems"), "writing": ("Query passage", "Candidate passages")}
MAX_CHARS = {"math": 1200, "writing": 700}  # per passage; keeps a 20-candidate window under ~5k tokens


def build_prompt(task: Task, qid: str, doc_ids: list[str]) -> str:
    q = task.queries[qid]
    q = strip_math_query(q) if task.name == "math" else q
    cap = MAX_CHARS[task.name]
    n = len(doc_ids)
    ql, cl = LABELS[task.name]
    cands = "\n\n".join(f"[{i}] {' '.join(task.corpus[d][:cap].split())}" for i, d in enumerate(doc_ids, 1))
    return (INSTRUCTIONS[task.name].format(n=n) + f"\n\n{ql}:\n{' '.join(q[:cap].split())}\n\n{cl}:\n\n{cands}\n\n"
            f"Answer with the identifiers only, most similar first, in the format [2] > [1] > [3] > ... "
            f"Include all {n} identifiers and nothing else.")


def parse_ranking(text: str, n: int) -> tuple[list[int], int]:
    """0-based permutation from '[3] > [1] > ...'; ids the model dropped keep their original order
    at the end. Also returns how many ids were missing (a parse-quality stat)."""
    seen = []
    for m in re.findall(r"\[(\d+)\]", text):
        i = int(m) - 1
        if 0 <= i < n and i not in seen:
            seen.append(i)
    missing = [i for i in range(n) if i not in seen]
    return seen + missing, len(missing)


def key(prompt: str, model: str, decoding: str) -> str:
    return hashlib.sha256(f"{model}\n{decoding}\n{prompt}".encode()).hexdigest()[:20]


class Cache:
    def __init__(self, path: Path):
        self.path = path
        self.rows = {}
        if path.exists():
            with open(path, encoding="utf-8") as f:
                for line in f:
                    try:
                        d = json.loads(line)
                    except json.JSONDecodeError:
                        continue  # half-written line from a killed run
                    self.rows[d["key"]] = d["out"]

    def add(self, items: list[tuple[str, str, str]]):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            for k, qid, out in items:
                self.rows[k] = out
                f.write(json.dumps({"key": k, "qid": qid, "out": out}, ensure_ascii=False) + "\n")


def rerank(task: Task, run: dict[str, dict[str, float]], cache: Cache, model: str, decoding: str,
           generate=None, top: int = 50, window: int = 20, step: int = 10) -> tuple[dict, dict]:
    """Sliding-window re-rank of each query's top `top` docs. generate(prompts) -> texts is only
    called for windows missing from the cache; with generate=None every window must be cached.
    Returns (new run, stats). Docs below `top` keep their first-stage order underneath."""
    orders = {q: [d for d, _ in sorted(docs.items(), key=lambda x: -x[1])] for q, docs in run.items()}
    heads = {q: o[:top] for q, o in orders.items()}
    stats = {"windows": 0, "generated": 0, "missing_ids": 0}
    end = top
    while True:
        start = max(0, end - window)
        todo = {q: h for q, h in heads.items() if len(h) > start}
        prompts = {q: build_prompt(task, q, h[start:end]) for q, h in todo.items()}
        keys = {q: key(p, model, decoding) for q, p in prompts.items()}
        new = [q for q in todo if keys[q] not in cache.rows]
        if new:
            assert generate is not None, f"{len(new)} windows not cached; run with an LLM"
            outs = generate([prompts[q] for q in new])
            cache.add([(keys[q], q, o) for q, o in zip(new, outs)])
            stats["generated"] += len(new)
        for q, h in todo.items():
            win = h[start:end]
            perm, miss = parse_ranking(cache.rows[keys[q]], len(win))
            h[start:end] = [win[i] for i in perm]
            stats["windows"] += 1
            stats["missing_ids"] += miss
        if start == 0:
            break
        end -= step
    out = {}
    for q, o in orders.items():
        ranked = heads[q] + o[top:]
        out[q] = {d: float(len(ranked) - r) for r, d in enumerate(ranked)}
    return out, stats
