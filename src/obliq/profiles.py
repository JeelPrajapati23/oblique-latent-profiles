"""Latent profiles: build profiling prompts, generate with an LLM, cache to disk.

Cache layout: profiles/<task>/<variant>/{docs,queries}.jsonl with {"_id", "profile"} per line,
plus meta.json recording the prompt hash, model and generation settings. A variant's cache is
never mixed with output from a different prompt or model.
"""
import hashlib
import json
import re
from pathlib import Path

from .data import DATA, ROOT, Task

PROMPTS = ROOT / "prompts"
PROFILES = ROOT / "profiles"

MATH_Q_PREFIX = "Given the following mathematical problem:\n\n"
MATH_Q_SUFFIX_START = "\n\nFind other mathematical problems that require the same core reasoning pattern"

# Which prompt each task uses for documents and queries (queries never see solutions).
TASK_PROMPTS = {
    "writing": {"doc": "writing_style", "query": "writing_style"},
    "math": {"doc": "math_problem", "query": "math_problem"},
    "math_soln": {"doc": "math_problem_solution", "query": "math_problem"},
    # Ablations (Math only): A1 topic words allowed, A3 ~40-word profiles. A2 (3B profiler) reuses
    # "math" with another model; the model name is part of the cache folder.
    "math_topic": {"doc": "math_problem_topic", "query": "math_problem_topic"},
    "math_short": {"doc": "math_problem_short", "query": "math_problem_short"},
    # E2 query rewriters (queries only; "doc" is unused but keeps the variant hash well-defined).
    # Writing is the paper's authorship rewriter prompt verbatim (App. D); the paper gives no Math
    # rewriter prompt, so Math follows its published Twitter rewriter template.
    "writing_rewrite": {"doc": "rewrite_writing", "query": "rewrite_writing"},
    "math_rewrite": {"doc": "rewrite_math", "query": "rewrite_math"},
}

MAX_CHARS = 4000  # truncate long Writing snippets; style is visible well before this


def strip_math_query(text: str) -> str:
    """Math queries wrap a problem in fixed boilerplate; profile only the problem."""
    assert text.startswith(MATH_Q_PREFIX), text[:80]
    return text[len(MATH_Q_PREFIX):].split(MATH_Q_SUFFIX_START)[0].strip()


def load_math_solutions() -> dict[str, dict[str, str]]:
    rows = json.loads((DATA / "analogues/math/final_dataset.json").read_text(encoding="utf-8"))
    return {f"{r['competition']}___{r['year']}___{r['problem_id']}": r for r in rows}


def read_prompt(name: str) -> str:
    return (PROMPTS / f"{name}.txt").read_text(encoding="utf-8")


def build_prompts(task: Task, kind: str, ids: list[str], setting: str | None = None) -> dict[str, str]:
    """User-turn prompt text for each id. kind is 'doc' or 'query'."""
    setting = setting or task.name
    template = read_prompt(TASK_PROMPTS[setting][kind])
    if kind == "query":
        src = task.queries
        clean = strip_math_query if task.name == "math" else (lambda t: t)
        return {i: template.format(text=clean(src[i])[:MAX_CHARS]) for i in ids}
    if setting == "math_soln":
        sol = load_math_solutions()
        return {i: template.format(problem=sol[i]["problem"], solution=sol[i]["solution"][:MAX_CHARS])
                for i in ids}
    return {i: template.format(text=task.corpus[i][:MAX_CHARS]) for i in ids}


# ---------------------------------------------------------------- generation backends

class HFBackend:
    """Local transformers backend (Windows-friendly; used for hand-testing on the laptop GPU)."""

    # transformers has no output-only frequency penalty; block long verbatim loops instead.
    decoding = "greedy-norepeat8"

    def __init__(self, model: str, max_new_tokens: int = 220, batch_size: int = 4):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(model, padding_side="left")
        self.model = AutoModelForCausalLM.from_pretrained(model, device_map="cuda:0", torch_dtype=torch.float16)
        self.max_new_tokens, self.batch_size = max_new_tokens, batch_size

    def generate(self, prompts: list[str]) -> list[str]:
        import torch
        out = []
        for b in range(0, len(prompts), self.batch_size):
            chats = [self.tok.apply_chat_template([{"role": "user", "content": p}], tokenize=False,
                                                  add_generation_prompt=True)
                     for p in prompts[b:b + self.batch_size]]
            enc = self.tok(chats, return_tensors="pt", padding=True).to(self.model.device)
            with torch.no_grad():
                gen = self.model.generate(**enc, max_new_tokens=self.max_new_tokens, do_sample=False,
                                          no_repeat_ngram_size=8, pad_token_id=self.tok.pad_token_id)
            out += self.tok.batch_decode(gen[:, enc["input_ids"].shape[1]:], skip_special_tokens=True)
        return [o.strip() for o in out]


class VLLMBackend:
    """Batched vLLM backend (Kaggle / Linux GPU) for profiling whole corpora."""

    # Greedy decoding looped on some Writing profiles ("metabolic signatures" x30); a frequency
    # penalty on generated tokens only (not the prompt) stops that without blocking quotes.
    decoding = "greedy-freqpen0.3"

    def __init__(self, model: str, max_new_tokens: int = 220, **llm_kwargs):
        from vllm import LLM, SamplingParams
        # T4s have no bf16; one T4 (16 GB) holds the 7B AWQ model, leaving the 2nd GPU free.
        kw = {"dtype": "half", "max_model_len": 4096, "gpu_memory_utilization": 0.85, "seed": 0}
        self.llm = LLM(model=model, **{**kw, **llm_kwargs})
        self.params = SamplingParams(temperature=0.0, frequency_penalty=0.3, max_tokens=max_new_tokens)

    def generate(self, prompts: list[str]) -> list[str]:
        msgs = [[{"role": "user", "content": p}] for p in prompts]
        return [o.outputs[0].text.strip() for o in self.llm.chat(msgs, self.params, use_tqdm=True)]


# ---------------------------------------------------------------- cache

def _meta(task_setting: str, kind: str, model: str, max_new_tokens: int, decoding: str) -> dict:
    prompt = read_prompt(TASK_PROMPTS[task_setting][kind])
    return {"prompt": TASK_PROMPTS[task_setting][kind],
            "prompt_sha": hashlib.sha256(prompt.encode()).hexdigest()[:12],
            "model": model, "max_new_tokens": max_new_tokens, "max_chars": MAX_CHARS,
            "decoding": decoding}


def variant_name(setting: str, model: str, decoding: str) -> str:
    """Cache folder name; changes whenever a prompt, the model or the decoding changes."""
    p = TASK_PROMPTS[setting]
    key = read_prompt(p["doc"]) + read_prompt(p["query"]) + decoding
    return f"{setting}-{hashlib.sha256(key.encode()).hexdigest()[:6]}__{model.split('/')[-1]}"


CACHE_FILES = {"doc": "docs.jsonl", "query": "queries.jsonl"}


_ECHO = re.compile(r"\n\s*(Passage|Problem|Solution)\s*:.*", re.S)


def clean_profile(text: str) -> str:
    """The model sometimes appends the source text after its answer ("Passage: ..."); drop it.
    Applied on read, so the raw cache keeps exactly what the model generated."""
    return _ECHO.sub("", text).strip()


def _cache_paths(vdir: Path, kind: str) -> list[Path]:
    """Main cache file first, then any shard files left by parallel (one-per-GPU) runs."""
    stem = CACHE_FILES[kind].removesuffix(".jsonl")
    return [p for p in [vdir / CACHE_FILES[kind], *sorted(vdir.glob(f"{stem}.shard*.jsonl"))] if p.exists()]


def _read_rows(path: Path) -> dict[str, str]:
    rows = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue  # half-written last line from a killed run; that id is regenerated
            rows[d["_id"]] = d["profile"]
    return rows


def load_profiles(task: str, variant: str, kind: str, raw: bool = False) -> dict[str, str]:
    rows = {}
    for path in _cache_paths(PROFILES / task / variant, kind):
        rows.update(_read_rows(path))
    return rows if raw else {i: clean_profile(t) for i, t in rows.items()}


def _append(path: Path):
    """Open a cache file for appending, first ending any unterminated last line (e.g. a file
    written by Jupyter's %%writefile, or a run killed mid-write) so new rows start on their own line."""
    if path.exists() and path.stat().st_size:
        with open(path, "rb") as f:
            f.seek(-1, 2)
            if f.read(1) != b"\n":
                with open(path, "a", encoding="utf-8") as g:
                    g.write("\n")
    return open(path, "a", encoding="utf-8")


def merge_shards(task: str, variant: str, kind: str) -> None:
    """Fold shard files into the main cache file (skipping ids already there), then delete them."""
    vdir = PROFILES / task / variant
    main = vdir / CACHE_FILES[kind]
    have = _read_rows(main) if main.exists() else {}
    shards = [p for p in _cache_paths(vdir, kind) if p != main]
    if not shards:
        return  # also covers a brand-new variant whose folder doesn't exist yet
    with _append(main) as f:
        for sp in shards:
            for i, text in _read_rows(sp).items():
                if i not in have:
                    have[i] = text
                    f.write(json.dumps({"_id": i, "profile": text}, ensure_ascii=False) + "\n")
    for sp in shards:
        sp.unlink()


def profile(task: Task, kind: str, ids: list[str], backend, variant: str, model: str,
            setting: str | None = None, max_new_tokens: int = 220, chunk: int = 256,
            shard: int | None = None) -> dict[str, str]:
    """Generate profiles for ids not yet cached; append to the cache as each chunk finishes.
    With shard=k, new rows go to <kind>.shard<k>.jsonl so parallel processes never share a file."""
    setting = setting or task.name
    vdir = PROFILES / task.name / variant
    vdir.mkdir(parents=True, exist_ok=True)
    meta_path = vdir / f"meta_{kind}.json"
    meta = _meta(setting, kind, model, max_new_tokens, backend.decoding)
    if meta_path.exists():
        old = json.loads(meta_path.read_text())
        assert old == meta, f"cache {vdir} was built with different settings:\n{old}\nvs\n{meta}"
    else:
        # atomic, since parallel shards may write it at the same moment
        tmp = meta_path.with_suffix(f".tmp{shard or 0}")
        tmp.write_text(json.dumps(meta, indent=1))
        tmp.replace(meta_path)

    done = load_profiles(task.name, variant, kind)
    todo = [i for i in ids if i not in done]
    prompts = build_prompts(task, kind, todo, setting)
    out = vdir / (CACHE_FILES[kind] if shard is None else CACHE_FILES[kind].replace(".jsonl", f".shard{shard}.jsonl"))
    with _append(out) as f:
        for c in range(0, len(todo), chunk):
            part = todo[c:c + chunk]
            for i, text in zip(part, backend.generate([prompts[i] for i in part])):
                done[i] = clean_profile(text)
                f.write(json.dumps({"_id": i, "profile": text}, ensure_ascii=False) + "\n")
            f.flush()
    return {i: done[i] for i in ids}
