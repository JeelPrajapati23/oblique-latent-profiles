"""Run files (qid -> {doc_id: score}), the exclusion mask, and top-k helpers."""
import json
from pathlib import Path

import numpy as np

from .data import ROOT

RUNS = ROOT / "runs"
Run = dict[str, dict[str, float]]


def mask(run: Run, excluded: dict[str, set[str]], k: int | None = None) -> Run:
    """Drop each query's excluded doc ids, then keep the top k. Every system goes through this."""
    out = {}
    for qid, docs in run.items():
        drop = excluded.get(qid, ())
        kept = sorted(((d, s) for d, s in docs.items() if d not in drop), key=lambda x: -x[1])
        out[qid] = dict(kept[:k] if k else kept)
    return out


def topk_from_scores(scores: np.ndarray, doc_ids: list[str], k: int) -> dict[str, float]:
    k = min(k, len(doc_ids))
    idx = np.argpartition(-scores, k - 1)[:k]
    idx = idx[np.argsort(-scores[idx])]
    return {doc_ids[i]: float(scores[i]) for i in idx}


def run_path(task: str, system: str) -> Path:
    return RUNS / task / f"{system}.json"


def save_run(run: Run, task: str, system: str) -> Path:
    path = run_path(task, system)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(run))
    return path


def load_run(task: str, system: str) -> Run:
    return json.loads(run_path(task, system).read_text())
