"""BM25 (rank-bm25, default params, as in the paper) and dense (Qwen3-Embedding + FAISS exact IP)."""
import re
from pathlib import Path

import numpy as np
from tqdm import tqdm

from .data import ROOT
from .runs import Run, topk_from_scores

CACHE = ROOT / "cache"

TOKENIZERS = {
    "split": lambda t: t.split(),                         # rank-bm25 README style
    "lower": lambda t: t.lower().split(),
    "word": lambda t: re.findall(r"\w+", t.lower()),
}


def bm25_search(docs: dict[str, str], queries: dict[str, str], k: int = 1000,
                tokenizer: str = "lower") -> Run:
    from rank_bm25 import BM25Okapi
    tok = TOKENIZERS[tokenizer]
    doc_ids = list(docs)
    bm25 = BM25Okapi([tok(docs[d]) for d in doc_ids])  # defaults: k1=1.5, b=0.75, epsilon=0.25
    run = {}
    for qid, text in tqdm(queries.items(), desc=f"bm25[{tokenizer}]"):
        scores = bm25.get_scores(tok(text))
        run[qid] = topk_from_scores(scores, doc_ids, k)
    return run


_MODELS = {}


def _model(name: str, max_len: int):
    if name not in _MODELS:
        import torch
        from sentence_transformers import SentenceTransformer
        kw = {"torch_dtype": torch.float16} if torch.cuda.is_available() else {}
        m = SentenceTransformer(name, model_kwargs=kw, tokenizer_kwargs={"padding_side": "left"})
        _MODELS[name] = m
    _MODELS[name].max_seq_length = max_len
    return _MODELS[name]


def encode(texts: dict[str, str], cache_name: str, model: str, prompt_name: str | None = None,
           max_len: int = 2048, batch_size: int = 8) -> tuple[list[str], np.ndarray]:
    """Encode and L2-normalise; cached to cache/emb/<cache_name>.npy (+ .ids)."""
    path = CACHE / "emb" / f"{cache_name}.npy"
    ids_path = path.with_suffix(".ids")
    ids = list(texts)
    if path.exists() and ids_path.read_text(encoding="utf-8").split("\n") == ids:
        return ids, np.load(path)
    emb = _model(model, max_len).encode(
        [texts[i] for i in ids], prompt_name=prompt_name, batch_size=batch_size,
        normalize_embeddings=True, show_progress_bar=True, convert_to_numpy=True,
    ).astype(np.float32)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path, emb)
    ids_path.write_text("\n".join(ids), encoding="utf-8")
    return ids, emb


def dense_search(doc_ids: list[str], doc_emb: np.ndarray, q_ids: list[str], q_emb: np.ndarray,
                 k: int = 1000) -> Run:
    import faiss
    index = faiss.IndexFlatIP(doc_emb.shape[1])  # exact inner product = cosine on normalised vectors
    index.add(doc_emb)
    scores, idx = index.search(q_emb, min(k, len(doc_ids)))
    return {q: {doc_ids[j]: float(s) for s, j in zip(scores[r], idx[r]) if j >= 0}
            for r, q in enumerate(q_ids)}
