"""Pipeline diagram for the IEEE report (reports/figures/fig0_pipeline.png).

    python scripts/make_pipeline_fig.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "reports" / "figures" / "fig0_pipeline.png"
EDGE, ACCENT, INK, MUTED = "#8a8980", "#2a78d6", "#222222", "#555555"


def box(ax, cx, cy, w, h, title, sub=None, main=False, dashed=False):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor="#e3eefb" if main else "white", edgecolor=ACCENT if main else EDGE,
                                linewidth=1.6 if main else 1.0, linestyle="--" if dashed else "-"))
    if sub:
        ax.text(cx, cy + 0.09, title, ha="center", va="center", fontsize=8.5, color=INK,
                fontweight="bold" if main or sub else "normal")
        ax.text(cx, cy - 0.12, sub, ha="center", va="center", fontsize=7, color=MUTED)
    else:
        ax.text(cx, cy, title, ha="center", va="center", fontsize=8, color=INK)


def arrow(ax, pts, dashed=False):
    xs, ys = zip(*pts)
    ax.plot(xs[:-1] + (xs[-1],), ys, color=EDGE, linewidth=1, linestyle="--" if dashed else "-")
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1, mutation_scale=8, shrinkA=0, shrinkB=0))


def main():
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    ax.set_xlim(0, 7.6)
    ax.set_ylim(0.2, 3.3)
    ax.axis("off")
    box(ax, 0.85, 1.75, 1.5, 0.55, "Document or query", "raw text")
    box(ax, 2.75, 0.9, 1.6, 0.55, "Qwen2.5-7B profiler", "same prompt, no topic", main=True)
    ix, iw, ih = 4.85, 1.75, 0.42
    for y, t in [(2.95, "BM25 over text"), (2.4, "Qwen3-0.6B over text"),
                 (1.1, "BM25 over profile"), (0.55, "Qwen3-0.6B over profile")]:
        box(ax, ix, y, iw, ih, t)
    box(ax, 6.85, 1.75, 1.2, 0.55, "RRF, k = 60", "E4, main system", main=True)
    box(ax, 6.85, 0.55, 1.2, 0.42, "E5: 7B re-rank", "top 50, optional", dashed=True)
    left = ix - iw / 2
    arrow(ax, [(1.6, 1.85), (3.75, 1.85), (3.75, 2.95), (left, 2.95)])
    arrow(ax, [(3.75, 2.4), (left, 2.4)])
    ax.text(2.7, 1.93, "text as is", fontsize=7, color=MUTED, ha="center")
    arrow(ax, [(0.85, 1.475), (0.85, 0.9), (1.95, 0.9)])
    ax.text(0.92, 1.15, "writes a profile", fontsize=7, color=MUTED)
    arrow(ax, [(3.55, 0.9), (3.75, 0.9), (3.75, 1.1), (left, 1.1)])
    arrow(ax, [(3.75, 0.9), (3.75, 0.55), (left, 0.55)])
    right = ix + iw / 2
    for y in (2.95, 2.4, 1.1, 0.55):
        ax.plot([right, 5.95], [y, y], color=EDGE, linewidth=1)
    ax.plot([5.95, 5.95], [0.55, 2.95], color=EDGE, linewidth=1)
    arrow(ax, [(5.95, 1.75), (6.25, 1.75)])
    arrow(ax, [(6.85, 1.475), (6.85, 0.76)], dashed=True)
    ax.text(ix, 3.22, "each returns its top 1,000", fontsize=7, color=MUTED, ha="center")
    fig.tight_layout(pad=0.2)
    fig.savefig(OUT, dpi=300, facecolor="white")
    print(OUT)


if __name__ == "__main__":
    main()
