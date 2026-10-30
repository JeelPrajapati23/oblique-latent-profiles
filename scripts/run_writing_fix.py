"""Writing fix attempt: B (re-index profiles without the generic fields) and D (non-LLM style baselines).

B: keep only some profile fields (the templated Voice / Tone lines carry no author signal), then BM25 and
   Qwen3 dense over the filtered profiles.
D: character n-gram TF-IDF on raw text, and a style embedding (AnnaWegmann/Style-Embedding) on raw text.
   If either carries style signal, fuse it into E4 as a 5th index.

Every choice is made on the fixed dev split; the report shows all / dev / test and a paired t-test on test.

    python scripts/run_writing_fix.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from obliq.data import ROOT, load_task
from obliq.fusion import dev_split, rrf
from obliq.profiles import VLLMBackend, load_profiles, variant_name
from obliq.retrievers import bm25_search, dense_search, encode
from obliq.runs import load_run, mask, run_path, save_run
from run_profiles import K, LLM, QWEN, pick, report

STYLE = "AnnaWegmann/Style-Embedding"
FIELDS = ["Voice", "Sentences", "Punctuation", "Tone and humour", "Signature phrases", "Other habits"]
KEEP = {
    "sig_habits": ["Signature phrases", "Other habits"],
    "no_voice_tone": ["Sentences", "Punctuation", "Signature phrases", "Other habits"],
}
_FIELD = re.compile(rf"^\s*({'|'.join(map(re.escape, FIELDS))})\s*:\s*(.*)$")


def keep_fields(profile: str, keep: list[str]) -> str:
    """Values of the kept fields only (labels dropped so they don't become shared BM25 terms)."""
    out = []
    for line in profile.splitlines():
        m = _FIELD.match(line)
        if m and m.group(1) in keep:
            out.append(m.group(2))
    return "\n".join(out)


def cached(task, name, fn):
    if not run_path(task.name, name).exists():
        save_run(mask(fn(), task.excluded, K), task.name, name)
    return load_run(task.name, name)


def char_tfidf(docs, queries, k, analyzer, ngrams):
    from sklearn.feature_extraction.text import TfidfVectorizer
    vec = TfidfVectorizer(analyzer=analyzer, ngram_range=ngrams, sublinear_tf=True, min_df=2,
                          max_df=0.5, lowercase=False, dtype=np.float32)
    d_ids, q_ids = list(docs), list(queries)
    D = vec.fit_transform([docs[i] for i in d_ids])
    Q = vec.transform([queries[i] for i in q_ids])
    run = {}
    for s in range(0, len(q_ids), 64):  # rows are L2-normalised, so the dot product is cosine
        S = (Q[s:s + 64] @ D.T).toarray()
        for r, q in enumerate(q_ids[s:s + 64]):
            top = np.argpartition(-S[r], k - 1)[:k]
            run[q] = {d_ids[j]: float(S[r, j]) for j in top}
    return run


def main():
    task = load_task("writing")
    k_fetch = K + max(len(v) for v in task.excluded.values())
    dev, test = dev_split("writing", task.qrels)
    v = variant_name("writing", LLM, VLLMBackend.decoding)
    docs_p, q_p = load_profiles("writing", v, "doc"), load_profiles("writing", v, "query")

    text = {n: load_run("writing", n) for n in ["bm25_text_split", "qwen3-0.6b_text_none"]}
    e4 = {n: load_run("writing", n) for n in
          ["E3_bm25_profile_word", "E3_qwen3-0.6b_profile_query", "E4_RRF_all_4_k_60"]}
    rows = {"E1 bm25_text_split": text["bm25_text_split"],
            "E1 qwen3-0.6b_text_none": text["qwen3-0.6b_text_none"],
            "E3 profile full (BM25-p word)": e4["E3_bm25_profile_word"],
            "E4 RRF all 4 (k=60)": e4["E4_RRF_all_4_k_60"]}
    notes = []

    # --- B: field-filtered profiles
    fieldcov = {f: sum(bool(re.search(rf"^\s*{re.escape(f)}\s*:", p, re.M)) for p in docs_p.values())
                / len(docs_p) for f in FIELDS}
    notes.append("- Field coverage in doc profiles: " + ", ".join(f"{f} {c:.0%}" for f, c in fieldcov.items()))
    best_b = {}
    for kname, keep in KEEP.items():
        d = {i: keep_fields(p, keep) for i, p in docs_p.items()}
        q = {i: keep_fields(p, keep) for i, p in q_p.items()}
        n_empty = sum(not t for t in d.values())
        notes.append(f"- B `{kname}` keeps {keep}; {n_empty} doc profiles end up empty.")
        cands = {f"B_bm25_profile_{kname}": cached(task, f"B_bm25_profile_{kname}",
                                                   lambda: bm25_search(d, q, k_fetch, "word"))}
        d_ids, d_emb = encode({i: t or " " for i, t in d.items()}, f"writing_docprof_{kname}_qwen3-0.6b_L512",
                              QWEN, max_len=512, batch_size=32)
        q_ids, q_emb = encode({i: t or " " for i, t in q.items()}, f"writing_qprof_{kname}_qwen3-0.6b_query_L512",
                              QWEN, prompt_name="query", max_len=512, batch_size=32)
        cands[f"B_qwen3_profile_{kname}"] = cached(task, f"B_qwen3_profile_{kname}",
                                                    lambda: dense_search(d_ids, d_emb, q_ids, q_emb, k_fetch))
        for n, r in cands.items():
            rows[f"B {n.removeprefix('B_')}"] = r
        best_b.update(cands)

    # --- D: non-LLM style baselines on raw text
    char = {}
    for analyzer, ng in [("char", (2, 4)), ("char", (3, 5)), ("char_wb", (2, 5))]:
        n = f"D_tfidf_{analyzer}_{ng[0]}{ng[1]}"
        char[n] = cached(task, n, lambda: char_tfidf(task.corpus, task.queries, k_fetch, analyzer, ng))
    best_char = pick(char, task, dev)
    for n, r in char.items():
        rows[f"D {n.removeprefix('D_')}"] = r
    style = None
    try:
        d_ids, d_emb = encode(task.corpus, "writing_corpus_style-emb_L512", STYLE, max_len=512, batch_size=32)
        q_ids, q_emb = encode(task.queries, "writing_queries_style-emb_L512", STYLE, max_len=512, batch_size=32)
        style = cached(task, "D_style_emb", lambda: dense_search(d_ids, d_emb, q_ids, q_emb, k_fetch))
        rows["D style_emb (Wegmann)"] = style
    except Exception as e:  # noqa: BLE001 - report and carry on with the other baselines
        notes.append(f"- Style-Embedding failed to load: `{type(e).__name__}: {e}`")
        print("style embedding failed:", e)

    # --- fusion: best B and best D as extra indexes, all picked on dev
    b_pick = pick(best_b, task, dev)
    four = [text["bm25_text_split"], text["qwen3-0.6b_text_none"],
            e4["E3_bm25_profile_word"], e4["E3_qwen3-0.6b_profile_query"]]
    fused = {
        f"E4 with B ({b_pick}) replacing BM25-p/dense-p": rrf(four[:2] + [best_b[b_pick]]),
        f"E4 + D ({best_char}) as 5th index": rrf(four + [char[best_char]]),
        f"BM25-t + D ({best_char})": rrf([text["bm25_text_split"], char[best_char]]),
    }
    if style is not None:
        fused["BM25-t + D style_emb"] = rrf([text["bm25_text_split"], style])
        fused[f"BM25-t + D ({best_char}) + D style_emb"] = rrf([text["bm25_text_split"], char[best_char], style])
        fused["E4 + D char + D style_emb (6 indexes)"] = rrf(four + [char[best_char], style])
    for n, r in fused.items():
        save_run(r, "writing", "F_" + re.sub(r"[^\w.-]+", "_", n).strip("_"))
    rows.update(fused)
    notes.append(f"- Picked on dev: best B run `{b_pick}`, best char n-gram run `{best_char}`.")

    table, labels = report(task, rows, dev, test, "E1 bm25_text_split")
    lines = ["# Writing fix attempt: B (filtered profiles) + D (non-LLM style baselines)", "",
             f"All numbers masked, {labels} qrels. Paper's Gemini-2-Embedding nDCG@10 = .164. "
             f"Dev = {len(dev)} queries, test = {len(test)}. p = paired t-test on test nDCG@10 vs "
             "`E1 bm25_text_split`; +/- = better/worse on average.", "", *notes, "", *table]
    out = ROOT / "reports" / "writing_fix.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
