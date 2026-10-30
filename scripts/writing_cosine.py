"""Writing analysis: are same-author snippets closer than different-author ones, per representation?

Uses the 540 author-labelled snippets (corpus_track.csv). Pairs from the same source post (the
per-query exclusion lists) are dropped, since retrieval never sees them either. Summary number per
representation: AUC = P(cos of a random same-author pair > cos of a random different-author pair).
Run after scripts/run_writing_fix.py (it reuses that script's embedding caches).

    python scripts/writing_cosine.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score

from obliq.data import DATA, ROOT, TASK_DIRS, load_task

EMB = ROOT / "cache" / "emb"
REPS = {  # label -> doc-embedding cache name
    "Raw text, Qwen3-0.6B": "writing_corpus_qwen3-0.6b_L2048",
    "Profile (all fields), Qwen3": "writing_docprof_writing-86bf72_qwen3-0.6b_L512",
    "Profile (no Voice/Tone), Qwen3": "writing_docprof_no_voice_tone_qwen3-0.6b_L512",
    "Profile (Signature + Habits), Qwen3": "writing_docprof_sig_habits_qwen3-0.6b_L512",
    "Raw text, Style-Embedding": "writing_corpus_style-emb_L512",
}
SAME, DIFF = "#2a78d6", "#eb6834"  # categorical slots 1-2 (validated pair)


def load_emb(name, ids):
    path = EMB / f"{name}.npy"
    if not path.exists():
        return None
    order = {d: i for i, d in enumerate((EMB / f"{name}.ids").read_text(encoding="utf-8").split("\n"))}
    return np.load(path)[[order[d] for d in ids]]


def main():
    task = load_task("writing")
    with open(DATA / TASK_DIRS["writing"] / "corpus" / "corpus_track.csv", encoding="utf-8") as f:
        author = {r["snippet_id"]: r["author_id"] for r in csv.DictReader(f)}
    ids = sorted(author, key=int)
    a = np.array([author[i] for i in ids])
    same = a[:, None] == a[None, :]
    keep = np.triu(np.ones_like(same), 1).astype(bool)
    pos = {d: i for i, d in enumerate(ids)}
    n_post = 0
    for q, ex in task.excluded.items():  # same-source-post pairs
        for d in ex:
            if q in pos and d in pos:
                keep[pos[q], pos[d]] = keep[pos[d], pos[q]] = False
                n_post += 1

    reps = {lab: load_emb(name, ids) for lab, name in REPS.items()}
    vec = TfidfVectorizer(analyzer="char", ngram_range=(2, 4), sublinear_tf=True, min_df=2, lowercase=False)
    vec.fit(task.corpus.values())  # same vocabulary/IDF as the retrieval run
    reps["Raw text, char 2-4-gram TF-IDF"] = vec.transform([task.corpus[i] for i in ids])
    reps = {k: v for k, v in reps.items() if v is not None}

    rows, sims = [], {}
    for lab, X in reps.items():
        S = X @ X.T
        S = S.toarray() if hasattr(S, "toarray") else S
        s, d = S[keep & same], S[keep & ~same]
        sims[lab] = (s, d)
        auc = roc_auc_score(np.r_[np.ones(len(s)), np.zeros(len(d))], np.r_[s, d])
        rows.append(f"| {lab} | {s.mean():.3f} | {d.mean():.3f} | {s.mean() - d.mean():+.3f} | {auc:.3f} |")

    n = len(sims)
    cols = 3
    fig, axes = plt.subplots((n + cols - 1) // cols, cols, figsize=(4.2 * cols, 3.2 * ((n + cols - 1) // cols)),
                             squeeze=False)
    for ax, (lab, (s, d)) in zip(axes.flat, sims.items()):
        bins = np.linspace(min(s.min(), d.min()), max(s.max(), d.max()), 50)
        ax.hist(d, bins=bins, density=True, color=DIFF, alpha=0.55, label="different author", linewidth=0)
        ax.hist(s, bins=bins, density=True, histtype="step", color=SAME, linewidth=2, label="same author")
        ax.set_title(lab, fontsize=10, color="#222")
        ax.set_xlabel("cosine similarity", fontsize=9, color="#555")
        ax.set_yticks([])
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(colors="#555", labelsize=8)
    for ax in list(axes.flat)[n:]:
        ax.axis("off")
    axes.flat[0].legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig_path = ROOT / "reports" / "figures" / "fig4_writing_author_similarity.png"
    fig_path.parent.mkdir(exist_ok=True)
    fig.savefig(fig_path, dpi=150, facecolor="white")

    n_same, n_diff = int((keep & same).sum()), int((keep & ~same).sum())
    lines = ["# Writing: same- vs different-author similarity", "",
             f"{len(ids)} author-labelled snippets, {len(set(a))} authors; {n_same} same-author and {n_diff} "
             f"different-author pairs ({n_post} same-source-post pairs dropped). AUC = P(same-author pair "
             "scores higher than a different-author pair); 0.5 = no author signal.", "",
             "| representation | mean cos same | mean cos diff | gap | AUC |", "|---|---|---|---|---|", *rows,
             "", f"![histograms](figures/{fig_path.name})"]
    (ROOT / "reports" / "analysis_writing_cosine.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
