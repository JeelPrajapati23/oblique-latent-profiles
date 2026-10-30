# Latent Profiles for Oblique Retrieval

IT550 Information Retrieval course project (Prof. Sandip Modha).

An open LLM (Qwen2.5-7B-Instruct) reads every document once, offline, and writes a short **latent profile** of its hidden traits (the proof move of a math problem, the habits of an author). Profiles are indexed with BM25 and Qwen3-Embedding-0.6B next to the raw text, each query is profiled with the same prompt, and the four ranked lists are fused with reciprocal rank fusion (RRF). The benchmark is [OBLIQ-Bench](https://arxiv.org/abs/2605.06235) (Tchuindjo, Shah & Khattab, 2026), Math and Writing-Style tasks.

## Results (nDCG@10, all numbers masked)

| | Math (gold / pooled) | Writing-Style (gold) |
|---|---|---|
| Paper's best single-stage retriever (Gemini-2-Embedding) | – / .147 | .164 |
| Qwen3-0.6B on text (our baseline) | .117 / .147 | .045 |
| BM25 on text | .060 / .072 | .099 |
| E2: same 7B LLM rewrites the query | .104 / .141 | .023 |
| E3: profiles only | .124 / .146 | .010 |
| **E4: text + profiles, RRF (main)** | **.142 / .175** | .060 |
| E5: E4 + 7B listwise re-rank | .126 / .156 | – |
| BM25 + char n-grams + Style-Embedding (non-LLM) | – | .128 |

- **Math:** E4 beats the text baseline on the held-out 80% test split (paired t-test p = .023 gold / .013 pooled) and passes the paper's 0.147.
- **Writing-Style:** the method fails. Profiles carry almost no author signal (same- vs different-author AUC 0.55); character n-grams and a style embedding do.
- **Query side:** document-side profiling beats query rewriting with the same LLM on both tasks; the 7B re-ranker hurts.
- **Ablations (Math):** a 3B profiler is significantly worse than 7B; profile length and the no-topic instruction make no significant difference.

Full tables: `reports/results.md`. Report: `report/ieee/` (IEEEtran LaTeX). Per-experiment reports: `reports/*.md`.

## Layout

```
src/obliq/        library: data loading, mask(), retrievers, RRF + dev split, evaluation, profiling, re-ranking
scripts/          one script per experiment (below)
prompts/          frozen LLM prompts (history: reports/prompt_log.md)
profiles/         cached LLM outputs: profiles, query rewrites (never regenerated)
rerank/           cached E5 re-ranker answers
splits/           fixed 20% dev / 80% test query split (seed 0)
kaggle/           generated notebooks for the GPU steps
reports/          experiment reports, results tables, figures
report/ieee/      IEEE-style paper (main.tex, refs.bib, figures)
```

Not in git (rebuilt or downloaded): `data/` (OBLIQ-Bench, auto-downloaded from Hugging Face `dianetc/OBLIQ-Bench`), `cache/` (embeddings), `runs/` (run files), `logs/`.

## Setup

```
python -m venv .venv
.venv\Scripts\activate            # Windows; source .venv/bin/activate elsewhere
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

A CUDA GPU with ~6 GB is enough for Qwen3-0.6B encoding; BM25, fusion and evaluation run on the CPU.

## Reproduce

All LLM outputs (profiles, rewrites, re-ranker answers) are already cached in `profiles/` and `rerank/`, so every number can be rebuilt locally without a large GPU. Run in this order:

| Step | Command | Output |
|---|---|---|
| E1 baselines | `python scripts/run_baselines.py --tasks math writing --systems bm25 dense --bm25-tok split lower word --qprompt query none` | `runs/<task>/` |
| E3 / E4 | `python scripts/run_profiles.py --tasks writing math` | `reports/e3_e4_<task>.md` |
| E2 query rewriting | `python scripts/run_rewrite.py --tasks math writing` | `reports/e2_<task>.md` |
| E5 re-ranking (from cache) | `python scripts/rerank.py --task math` | `runs/math/E5_*.json` |
| Math analysis | `python scripts/analyze.py --task math` | `reports/analysis_math.md` |
| Writing fix + style baselines | `python scripts/run_writing_fix.py` | `reports/writing_fix.md` |
| Author-similarity analysis | `python scripts/writing_cosine.py` | `reports/analysis_writing_cosine.md` |
| Ablations A1–A3 | `python scripts/run_ablations.py` | `reports/ablations_math.md` |
| Final tables and figures | `python scripts/make_results.py` | `reports/results.md`, `reports/tables.tex`, `reports/figures/` |
| Pipeline figure | `python scripts/make_pipeline_fig.py` | `reports/figures/fig0_pipeline.png` |

### Regenerating LLM outputs (Kaggle, 2× T4)

`python scripts/build_kaggle_notebook.py --profile | --rewrite | --rerank | --ablation` writes a self-contained notebook to `kaggle/`. Upload it to Kaggle (GPU T4 ×2, Internet on), run Save & Run All (Commit), download the output zip and unzip it into the project with `unzip -n` (never overwrite). Profiles are cached under `profiles/<task>/<setting>-<hash>__<model>/`; the hash covers the prompts and decoding, so a changed prompt gets a new folder. GPU cost per job: `reports/results.md`, Table 5.

## Evaluation rules

- Every run passes through `mask()` with the benchmark's `per_query_excluded_ids.json` before scoring; the evaluator refuses unmasked runs.
- All choices (tokenizer, query prompt, fusion weights) are made on the fixed dev split; results are reported on all queries and on the test split.
- A win is claimed only at p < 0.05 (paired t-test on test nDCG@10). Math is reported with gold and pooled judgments.
- The Math solution-aware profiles (`math_soln`) are a labelled variant, never the headline: the benchmark's retrievers never see solutions.

## Citation

Tchuindjo, Shah & Khattab. *OBLIQ-Bench: Exposing Overlooked Bottlenecks in Modern Retrievers with Latent and Implicit Queries.* arXiv:2605.06235, 2026. Dataset: CC-BY-4.0.
