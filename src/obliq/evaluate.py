"""Evaluation with ranx. Runs must already be masked; we assert it."""
from ranx import Qrels as RQrels, Run as RRun, evaluate as rx_evaluate

from .data import Task
from .runs import Run

METRICS = ["ndcg@10", "ndcg@50", "recall@10", "recall@50", "recall@100"]


def check_masked(run: Run, task: Task):
    leaks = sum(len(set(docs) & task.excluded.get(q, set())) for q, docs in run.items())
    assert leaks == 0, f"{leaks} excluded docs present in run: call mask() first"


def _qrels_sets(task: Task, qids=None):
    for label, qrels in (("gold", task.qrels), ("pool", task.qrels_pool)):
        if qrels is not None:
            yield label, {q: r for q, r in qrels.items() if qids is None or q in qids}


def evaluate_run(run: Run, task: Task, metrics=METRICS, qids=None) -> dict[str, dict[str, float]]:
    """Returns {"gold": {...}, "pool": {...}} (pool only when the task has pooled qrels).
    qids restricts scoring to a subset of queries (e.g. the dev or test split)."""
    check_masked(run, task)
    # ranx needs every judged query present in the run; an empty result scores 0.
    out = {}
    for label, qrels in _qrels_sets(task, qids):
        full = {q: (run.get(q) or {"__none__": 0.0}) for q in qrels}
        res = rx_evaluate(RQrels(qrels), RRun(full), metrics)
        # ranx returns a bare float when given a single metric
        out[label] = res if isinstance(res, dict) else {metrics[0]: float(res)}
    return out


def per_query(run: Run, task: Task, metric: str = "ndcg@10", qids=None) -> dict[str, dict[str, float]]:
    """{"gold": {qid: score}, "pool": {...}} for paired significance tests."""
    check_masked(run, task)
    out = {}
    for label, qrels in _qrels_sets(task, qids):
        full = {q: (run.get(q) or {"__none__": 0.0}) for q in qrels}
        scores = rx_evaluate(RQrels(qrels), RRun(full), metric, return_mean=False)
        out[label] = dict(zip(sorted(qrels), map(float, scores)))  # ranx orders queries by id
    return out


def format_row(name: str, res: dict[str, dict[str, float]], metrics=METRICS) -> str:
    cells = []
    for m in metrics:
        vals = [f"{res[k][m]:.3f}" for k in ("gold", "pool") if k in res]
        cells.append("/".join(vals))
    return f"{name:<28}" + "  ".join(f"{c:>11}" for c in cells)


def header(metrics=METRICS) -> str:
    return f"{'system':<28}" + "  ".join(f"{m:>11}" for m in metrics)
