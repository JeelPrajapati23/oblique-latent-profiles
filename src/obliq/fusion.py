"""Rank fusion over run files, and the fixed dev/test query split used for all tuning."""
import json
import random

from .data import ROOT
from .runs import Run

SPLITS = ROOT / "splits"


def rrf(runs: list[Run], k: int = 60, weights: list[float] | None = None, depth: int = 1000) -> Run:
    """Weighted reciprocal rank fusion: score(d) = sum_i w_i / (k + rank_i(d)), ranks from 1.
    Inputs must already be masked; fusing masked runs keeps them masked."""
    weights = weights or [1.0] * len(runs)
    out = {}
    for q in set().union(*runs):
        acc: dict[str, float] = {}
        for run, w in zip(runs, weights):
            if not w:
                continue
            ranked = sorted(run.get(q, {}).items(), key=lambda x: -x[1])
            for r, (d, _) in enumerate(ranked, 1):
                acc[d] = acc.get(d, 0.0) + w / (k + r)
        out[q] = dict(sorted(acc.items(), key=lambda x: -x[1])[:depth])
    return out


def dev_split(task_name: str, qids, frac: float = 0.2, seed: int = 0) -> tuple[set[str], set[str]]:
    """Fixed dev/test split, created once and saved to splits/<task>.json; later calls reuse it."""
    path = SPLITS / f"{task_name}.json"
    if path.exists():
        d = json.loads(path.read_text())
        assert set(d["dev"]) | set(d["test"]) == set(qids), f"{path} doesn't match the query set"
        return set(d["dev"]), set(d["test"])
    ids = sorted(qids)
    random.Random(seed).shuffle(ids)
    n = round(frac * len(ids))
    dev, test = sorted(ids[:n]), sorted(ids[n:])
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({"seed": seed, "frac": frac, "dev": dev, "test": test}, indent=1))
    return set(dev), set(test)
