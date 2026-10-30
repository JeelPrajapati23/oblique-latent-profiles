"""Week 1: hand-test profile prompts on 20 items per task (5 groups x 4).

A group is one query plus 3 of its gold documents, so items in a group share the hidden
property (same author / same proof move) and items in different groups don't. The report shows
every profile for reading, plus three checks:
  - length and format compliance (60-120 words; Math has the 3 fixed fields)
  - topic leakage: content words the profile copies from its source text
  - within-group vs across-group cosine similarity, for raw text and for profiles

    python scripts/handtest_prompts.py --task writing
    python scripts/handtest_prompts.py --task math --setting math_soln
    # Kaggle (2x T4): LLM on GPU 0 via vLLM, embedder on GPU 1
    python scripts/handtest_prompts.py --task writing --backend vllm --embed-device cuda:1
"""
import argparse
import gc
import random
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from obliq.data import ROOT, load_task
from obliq.profiles import (TASK_PROMPTS, HFBackend, VLLMBackend, load_profiles, profile,
                            strip_math_query, variant_name)

MODELS = {"hf": "unsloth/Qwen2.5-7B-Instruct-bnb-4bit", "vllm": "Qwen/Qwen2.5-7B-Instruct-AWQ"}
EMBEDDER = "Qwen/Qwen3-Embedding-0.6B"
STOP = set("""this that with from have which their there they them then than when what where
would could should about into also only very such some more most other these those were been
being does doing your yours each both same just over under after before while because again
further once here many much will shall must might problem prove show find given let suppose
assume determine compute value values number numbers every exists exist""".split())


def sample_groups(task, n_groups=5, per_group=3, seed=0):
    rng = random.Random(seed)
    qids = sorted(task.qrels)
    rng.shuffle(qids)
    groups, used = [], set()
    for q in qids:
        rel = sorted(set(task.qrels[q]) - task.excluded.get(q, set()))
        if len(rel) < per_group or used & set(rel) or q in used:
            continue  # need disjoint groups so "different group" really means different property
        docs = rng.sample(rel, per_group)
        groups.append((q, docs))
        used |= set(task.qrels[q]) | {q}
        if len(groups) == n_groups:
            break
    return groups


def nwords(text):
    # counts "short_sentences,rhythmic" as 2 words, unlike str.split()
    return len(re.findall(r"[A-Za-z0-9']+", text))


def content_words(text):
    return {w for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in STOP}


def p_at3(sim, labels):
    """Leave-one-out: share of each item's top-3 neighbours that are in its group (chance = 3/19)."""
    hits = []
    for i in range(len(labels)):
        top = [j for j in np.argsort(-sim[i]) if j != i][:3]
        hits.append(sum(labels[j] == labels[i] for j in top) / 3)
    return float(np.mean(hits))


def bm25_sim(texts):
    from rank_bm25 import BM25Okapi
    tok = lambda t: re.findall(r"\w+", t.lower())
    bm25 = BM25Okapi([tok(t) for t in texts])
    return np.array([bm25.get_scores(tok(t)) for t in texts])


def group_sims(emb, labels):
    sims = emb @ emb.T
    same = [sims[i, j] for i in range(len(labels)) for j in range(i + 1, len(labels)) if labels[i] == labels[j]]
    diff = [sims[i, j] for i in range(len(labels)) for j in range(i + 1, len(labels)) if labels[i] != labels[j]]
    return float(np.mean(same)), float(np.mean(diff))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=["math", "writing"])
    ap.add_argument("--setting", default=None, help="math_soln = profile Math docs with solutions")
    ap.add_argument("--backend", default="hf", choices=["hf", "vllm"])
    ap.add_argument("--model", default=None)
    ap.add_argument("--embed-device", default="cuda:0")
    ap.add_argument("--rescore", action="store_true", help="use cached profiles, don't run the LLM")
    args = ap.parse_args()
    setting = args.setting or args.task
    args.model = args.model or MODELS[args.backend]

    task = load_task(args.task)
    groups = sample_groups(task)
    p = TASK_PROMPTS[setting]
    q_ids = [q for q, _ in groups]
    d_ids = [d for _, ds in groups for d in ds]
    backend_cls = HFBackend if args.backend == "hf" else VLLMBackend
    variant = variant_name(setting, args.model, backend_cls.decoding)
    if args.rescore:
        # re-score saved profiles (e.g. downloaded from Kaggle) without running the LLM
        q_prof = load_profiles(task.name, variant, "query")
        d_prof = load_profiles(task.name, variant, "doc")
        missing = [i for i in q_ids if i not in q_prof] + [i for i in d_ids if i not in d_prof]
        assert not missing, f"no cached profiles in {variant} for {missing[:5]}"
    else:
        backend = backend_cls(args.model)
        q_prof = profile(task, "query", q_ids, backend, variant, args.model, setting)
        d_prof = profile(task, "doc", d_ids, backend, variant, args.model, setting)
        del backend
        gc.collect()

    # items in display order: (group, kind, id, source text, profile)
    items = []
    for g, (q, docs) in enumerate(groups):
        src_q = strip_math_query(task.queries[q]) if args.task == "math" else task.queries[q]
        items.append((g, "query", q, src_q, q_prof[q]))
        items += [(g, "doc", d, task.corpus[d], d_prof[d]) for d in docs]

    import torch
    from sentence_transformers import SentenceTransformer
    torch.cuda.empty_cache()
    emb_model = SentenceTransformer(EMBEDDER, device=args.embed_device,
                                    model_kwargs={"torch_dtype": torch.float16})
    emb_model.max_seq_length = 2048
    labels = [it[0] for it in items]
    raw_texts, prof_texts = [it[3] for it in items], [it[4] for it in items]
    raw = emb_model.encode(raw_texts, normalize_embeddings=True, batch_size=4)
    prof = emb_model.encode(prof_texts, normalize_embeddings=True, batch_size=4)
    raw_same, raw_diff = group_sims(raw, labels)
    prof_same, prof_diff = group_sims(prof, labels)

    words = [nwords(it[4]) for it in items]
    leaks = [sorted(content_words(it[4]) & content_words(it[3])) for it in items]
    fields = {"math": ("Techniques:", "Proof move:", "Key insight:", "Also known as:"),
              "writing": ("Voice:", "Sentences:", "Punctuation:", "Tone and humour:",
                          "Signature phrases:", "Other habits:")}[args.task]
    fmt_ok = sum(all(f in it[4] for f in fields) for it in items)
    symbols = sum(bool(re.search(r"[$\\^_{}=]", it[4])) for it in items)

    lines = [f"# Prompt hand-test: {setting}", "",
             f"- Variant: `{variant}` (prompts: doc=`{p['doc']}`, query=`{p['query']}`)",
             f"- Model: `{args.model}`, decoding `{backend_cls.decoding}`",
             f"- Words per profile: min {min(words)}, median {int(np.median(words))}, max {max(words)} "
             f"(target 60-120); in range: {sum(60 <= w <= 120 for w in words)}/{len(words)}",
             f"- Format compliant ({len(fields)} fields): {fmt_ok}/{len(items)}",
             f"- Profiles containing formula symbols ($ \\ ^ _ {{ }} =): {symbols}/{len(items)}",
             f"- Profiles with copied content words: {sum(bool(l) for l in leaks)}/{len(items)}",
             "",
             "| Cosine (Qwen3-0.6B) | same group | different group | gap |",
             "|---|---|---|---|",
             f"| raw text | {raw_same:.3f} | {raw_diff:.3f} | {raw_same - raw_diff:+.3f} |",
             f"| profile | {prof_same:.3f} | {prof_diff:.3f} | {prof_same - prof_diff:+.3f} |",
             "", "A bigger gap means profiles separate the hidden property better than raw text does.", "",
             "| Leave-one-out P@3 (chance 0.158) | BM25 | dense |", "|---|---|---|",
             f"| raw text | {p_at3(bm25_sim(raw_texts), labels):.3f} | {p_at3(raw @ raw.T, labels):.3f} |",
             f"| profile | {p_at3(bm25_sim(prof_texts), labels):.3f} | {p_at3(prof @ prof.T, labels):.3f} |",
             "", "P@3 is closer to retrieval: for each item, how many of its top-3 neighbours share its "
             "hidden property. Cosine gap alone undersold BM25-friendly profiles (round 2).", ""]
    for (g, kind, i, src, pr), leak in zip(items, leaks):
        if kind == "query":
            lines += [f"## Group {g + 1}", ""]
        excerpt = src[:400].replace("\n", " ") + ("..." if len(src) > 400 else "")
        lines += [f"**{kind} `{i}`** ({nwords(pr)} words)", "",
                  f"> {excerpt}", "", f"Profile: {pr}", "",
                  f"Copied words: {', '.join(leak) if leak else '-'}", ""]
    out = ROOT / "reports" / f"handtest_{setting}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:22]))
    print(f"\nreport: {out}")


if __name__ == "__main__":
    main()
