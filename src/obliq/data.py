"""Load OBLIQ-Bench tasks (corpus, queries, gold/pooled qrels, per-query exclusions)."""
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "obliq"
TASK_DIRS = {"math": "analogues/math", "writing": "analogues/writing"}

Qrels = dict[str, dict[str, int]]


@dataclass
class Task:
    name: str
    corpus: dict[str, str]
    queries: dict[str, str]
    qrels: Qrels                      # gold judgments
    qrels_pool: Qrels | None          # pooled judgments (Math only)
    excluded: dict[str, set[str]] = field(default_factory=dict)


def download(tasks=("math", "writing")):
    from huggingface_hub import snapshot_download
    snapshot_download("dianetc/OBLIQ-Bench", repo_type="dataset", local_dir=DATA,
                      allow_patterns=[f"{TASK_DIRS[t]}/*" for t in tasks] + ["README.md"])


def _read_jsonl(path: Path) -> dict[str, str]:
    with open(path, encoding="utf-8") as f:
        return {d["_id"]: d["text"] for d in map(json.loads, f) if d}


def _read_qrels(path: Path) -> Qrels | None:
    # Tab-separated with a header; column names differ per task (query-id vs query_id).
    if not path.exists():
        return None
    qrels: Qrels = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        for qid, did, score in reader:
            if int(score) > 0:
                qrels.setdefault(qid, {})[did] = int(score)
    return qrels


def load_task(name: str) -> Task:
    base = DATA / TASK_DIRS[name]
    qdir = base / "queries+qrels"
    if not (base / "corpus" / "corpus.jsonl").exists():
        download((name,))
    excl_path = qdir / "per_query_excluded_ids.json"
    excluded = {}
    if excl_path.exists():
        excluded = {q: set(ids) for q, ids in json.loads(excl_path.read_text()).items()}
    return Task(
        name=name,
        corpus=_read_jsonl(base / "corpus" / "corpus.jsonl"),
        queries=_read_jsonl(qdir / "queries.jsonl"),
        qrels=_read_qrels(qdir / "qrels.tsv"),
        qrels_pool=_read_qrels(qdir / "qrels_pool.tsv"),
        excluded=excluded,
    )
