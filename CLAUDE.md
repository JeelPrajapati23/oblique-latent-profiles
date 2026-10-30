# CLAUDE.md — Latent Profiles for Oblique Retrieval (IT550)

Source of truth: `IT550 Project Latent Profiles for Oblique Retrieval.pdf` (project summary).
Base paper: `2605.06235v2.PDF` — *OBLIQ-Bench: Exposing Overlooked Bottlenecks in Modern Retrievers with Latent and Implicit Queries* (Tchuindjo, Shah & Khattab, MIT, arXiv preprint May 2026, https://arxiv.org/abs/2605.06235). When a number or file name is in doubt, check the paper PDF, not memory.

Course: IT550 Information Retrieval, Prof. Sandip Modha.

## Goal

Make retrieval work for **oblique queries**: relevance comes from a hidden property (writing style, proof technique, stance), not the topic.

**Method:** a small open LLM reads every document once, offline, and writes a short **latent profile** of its hidden traits. Index profiles alongside raw text, profile each query with the same LLM/prompt, fuse all result lists (RRF). Optionally re-rank the top results with a small LLM.

**Why it's new:** the paper only tried query-side fixes (rewriting, multi-hop agent); rewriting even hurt Writing-Style (0.164 → 0.018). We test the document side, which the paper names as an open direction.

**Main claim to test:** adding LLM document profiles to a free, open retriever raises nDCG@10 above the paper's best single-stage retriever — **0.147 on Math, 0.164 on Writing-Style**.

## Hard constraints

- **Free, open models only** (no Gemini, no GPT). Compute: laptop (BM25, fusion, eval) + Kaggle GPU (2× T4, ~30 h/week) for LLM profiling and dense encoding.
- **Cache every LLM output to disk** so it is computed exactly once. Never regenerate profiles that already exist.
- **Apply `per_query_excluded_ids.json` to every run before scoring** via a single `mask(run)` helper. Skipping it inflates scores and makes results incomparable.
- Reproduce baselines (E1) within ±0.01 of the paper **before** adding our method. If off, fix evaluation first.
- Paper results for Math and Writing are in **Table 3** (verified): columns are nDCG@10, nDCG@50, R@10, R@50, R@100. Math cells are gold/pooled; Writing has gold only. Some Math BM25 pooled cells look like typos (R@50 = R@100 = .029), so compare against gold first.
- Run all Python via `.venv\Scripts\python.exe` (CUDA torch 2.6 on the local RTX 4050, 6 GB; usable for Qwen3-0.6B encoding).

## Data: OBLIQ-Bench (HF `dianetc/OBLIQ-Bench`, CC-BY-4.0)

| Task | Queries | Corpus | Labels | Use |
|---|---|---|---|---|
| **Writing-Style** | 512 | ~10.9k snippets | real authorship (no LLM) | **Core** — lead with this |
| **Math Meta-Program** | 151 | ~3.66k problems | GPT-5, clustered | **Core** |
| Twitter-Conflict | 281 | ~72.4k tweets | GPT-5, rejudged | Stretch (~7× Writing's profiling cost) |
| Congress Hearings | 254 | ~214k passages | one gold | Optional |
| WildChat Errors | 40 | ~508k chats | — | Skip |

Files per task folder:
- `corpus.jsonl` (`_id`, `text`), `queries.jsonl` (`_id`, `text`, metadata)
- `qrels.tsv` — tab-separated **with header** (`query_id`, `corpus_id`, `score`). Convert to ranx format once; don't assume TREC layout.
- `qrels_pool.tsv` — pooled judgments (some tasks)
- `per_query_excluded_ids.json` (Math, Writing) — e.g. Writing hides snippets from the same source post.

## Paper baselines (nDCG@10)

| System | Math | Writing | Twitter | Congress |
|---|---|---|---|---|
| BM25 (rank-bm25 defaults) | .029 | .077 | .002 | .000 |
| LateOn 0.1B (multi-vector) | .128 | .105 | .010 | .083 |
| Qwen3-Embedding-0.6B | .143 | .046 | .012 | .006 |
| Qwen3-Embedding-4B | .129 | .033 | .039 | .040 |
| Gemini-2-Embedding | .147 | .164 | .132 | .059 |
| GPT-5.2 query rewriter + Gemini | .185 | .018 | .139 | .084 |
| GPT-5.2 multi-hop agent (4 rounds) | .207 | .061 | .215 | .183 |
| *Oracle* GPT-5.2 reranker (gold injected; upper bound) | .329 | .515 | .436 | .913 |

Math and Twitter use pooled judgments; Writing and Congress have a single gold doc per query.
We reproduce: BM25, Qwen3-Embedding-0.6B, and LateOn if time allows.

Paper Table 3 extra columns (nDCG@50, R@10, R@50, R@100):
- Math BM25 (G/P): .034/.025, .020/.029, .060/.029, .088/.029 · Math Qwen3-0.6B: .149/.176, .070/.088, .219/.247, .309/.336
- Writing BM25: .114, .062, .154, .208 · Writing Qwen3-0.6B: .060, .040, .075, .103

## E1 status (2026-10-28)
- Qwen3-0.6B reproduced within ±0.004 on every metric. Math matches best with the default `query` prompt (0.115/0.142); Writing with no prompt (0.045).
- BM25 Math: `split`/`lower` tokenizer 0.027/0.035 vs paper .022/.029 (OK). BM25 Writing: `word` 0.083 (+0.006), `split` 0.099 (+0.022). No single tokenizer matches both tasks; our BM25 is slightly stronger than the paper's, which is the conservative side for our claims.

## Profiling + E3/E4 status (2026-10-30)
- All profiles done on Kaggle (2× T4): Writing 158 GPU-min, Math 16, Math+soln 71. Installed in `profiles/`.
- `scripts/run_profiles.py` → `reports/e3_e4_{math,writing}.md`; dev split in `splits/<task>.json` (seed 0, 20%).
- Math: E4 equal-weight RRF of 4 indexes = 0.142 gold / **0.175 pooled** (> paper .147), p = .023/.013 vs Qwen3 text on test. Text-only RRF hurts (0.098/0.124), so the gain comes from the profiles. Dev-tuned weights overfit (30 dev queries) → headline is equal-weight RRF.
- Math analysis (`reports/analysis_math.md`): E4 vs Qwen3 text per query (pooled) 59 better / 35 worse / 57 tied. Gains: profiles name the specific move (telescoping, determinant structure) and lift gold docs from rank 20-80 into the top 10. Losses: series-evaluation problems whose profiles are generic ("series manipulation, zeta function properties"), so many near-duplicate profiles crowd out the gold doc. Online cost ~104 ms/query on the CPU plus one LLM call to profile the query. E5 (Qwen2.5-7B listwise re-rank of E4 top 50, 45 GPU-min, ~18 GPU-s/query): **hurts**, 0.126/0.156 vs E4 0.142/0.175 (46 worse / 23 better pooled, p = .067, not significant). The model does reorder a lot (median Kendall tau vs input 0.23; only 11% of windows returned unchanged), but its reordering is worse than RRF's, so it doesn't recognise shared reasoning from problem text alone. RQ5: a 7B open re-ranker closes none of the gap to the oracle's .329.
- E2 (same Qwen2.5-7B rewrites the query once → Qwen3 text; `reports/e2_<task>.md`; 4 + 6 GPU-min wall on 2× T4). Math: 0.104/0.141, no different from Qwen3 text (p = .64/.83); E4 beats E2 (p = .012/.029 on test). Writing: 0.023, half of Qwen3 text with the original query (0.045, p = 4e-7). That reproduces the paper's rewriter collapse (.164 → .018) with an open LLM; E4 0.060 beats E2 (p = 2e-12). Rewrites drift to the topic: they quote topical jargon and summarise the content instead of the style. **RQ4: document-side profiling beats query-side rewriting with the same LLM on both tasks.** 33/512 Writing answers hit the 220-token cap (partial rewrite used; rerunning with the fix didn't change the result).
- Writing: negative so far. Profiles alone are ~0.009 and E4 is 0.060 < BM25-text 0.099. Not a bug: profiles are templated (36% share the exact Voice line "we, neutral and informative, formal"), same-author vs random doc-profile cosine is 0.714 vs 0.704, and "signature phrases" are mostly topical.

## Writing fix B + D and cosine analysis (2026-10-30)
- `scripts/run_writing_fix.py` → `reports/writing_fix.md`. **B fails:** dropping Voice/Tone or keeping only Signature + Habits makes profiles *worse* (0.004–0.006 vs 0.008); E4 with filtered profiles is 0.075 < BM25-t 0.099. So C (re-profiling Writing, ~160 GPU-min) is **not** worth spending; write Writing up as a negative result for profiles.
- **D, the style signal exists:** char 2-4-gram TF-IDF 0.092, Wegmann Style-Embedding 0.075 (both alone ≈ BM25-t). Non-LLM fusion BM25-t + char 3-5 + style-emb = **0.128** (test 0.125 vs 0.095, p = 6e-9), still < Gemini .164. Adding them to E4 (6 indexes) gives 0.110: the profile indexes drag the fusion down. Only the char n-gram config was picked on dev; the fusion rows are a fixed small set, all reported.
- LUAR was not run (needs `trust_remote_code`, which the permission classifier blocked); Style-Embedding stands in for it.
- `scripts/writing_cosine.py` → `reports/analysis_writing_cosine.md` + `fig_writing_cosine.png` (540 author-labelled snippets from `corpus_track.csv`, 62 authors, same-post pairs dropped). Same- vs different-author AUC: profiles 0.538–0.550 (almost no author signal), raw Qwen3 0.663 (likely topic, since an author blogs on the same topics), Style-Embedding 0.654, char TF-IDF 0.645.

## Ablations A1–A3: done (2026-10-30) → `reports/ablations_math.md`
- E4 (gold/pooled) vs main 0.142/0.175: A1 topic allowed 0.142/0.178 (p = .73/.90), A2 3B 0.128/0.149 (p = .46/.10), A3 ~40 words 0.138/0.169 (p = .72/.57). No E4 difference is significant.
- E3 (profiles only, test) vs main 0.126/0.148: **A2 3B is significantly worse, 0.087/0.103 (p = .007/.006)**; A1 0.107/0.141 (p = .21/.60) and A3 0.123/0.141 (p = .88/.67) are not significant.
- Takeaways: profiler size matters (7B > 3B), while length and the no-topic rule don't. The A1 manipulation was weak, though: the banned-word rate only rose from 42% to 48%. GPU-min: A1 21, A2 13, A3 16.
- Setup: settings `math_topic` / `math_short`, 3B via `profile_corpus.py --model`, notebook `build_kaggle_notebook.py --ablation`, components fixed to the main system.

### Setup notes (written before the run)
- New settings in `TASK_PROMPTS`: `math_topic` (`prompts/math_problem_topic.txt`, only the no-topic sentence swapped for "also name the field and objects") and `math_short` (`math_problem_short.txt`, "about 40 words", fewer items per field). A2 = setting `math` with `profile_corpus.py --model Qwen/Qwen2.5-3B-Instruct-AWQ`; the main cache hash `math-ee895b` is unchanged.
- `build_kaggle_notebook.py --ablation` → `kaggle/ablation.ipynb` → `ablation_out.zip`. Then `scripts/run_ablations.py` → `reports/ablations_math.md` (components fixed to the main system, p vs main E4; reproduces main E4 0.142/0.175 exactly).
- Context for reading A1/A3: main doc profiles average **59 words** (the prompt asked for 60–100), and **42%** already contain one of the banned example topic words, so the "no topic" rule is only partly followed.

## Week 4: results tables + figures (2026-10-30)
- `scripts/make_results.py` → `reports/results.md` + `reports/tables.tex` (booktabs; uses UTF-8 –, †, ×) + `reports/figures/fig1–3`. Fig 4 (author similarity) comes from `writing_cosine.py`. Every number is recomputed from the masked run files.
- Tables: 1 E1 vs paper Table 3; 2 Math; 3 Writing; 4 ablations; 5 LLM cost. Math Qwen3 **gold** nDCG@10 from the paper isn't recorded here; it shows "–" until filled in from the PDF.
- **Open question:** Math E4 with dev-tuned weights [0, 2, 0.5, 0.5] scores 0.163/0.197 on *test* (p = .0009/.0004 vs Qwen3 text), higher than equal-weight E4 at 0.139/0.173. That contradicts the earlier note that dev-tuned weights overfit. The headline stays equal-weight RRF, which is the conservative choice, but the write-up should report the tuned row honestly.

- IEEE report: `report/ieee/` (main.tex, refs.bib, figures/; `scripts/make_pipeline_fig.py` draws Fig. 1), zipped as `report/ieee_report_overleaf.zip`. It hasn't been compiled locally (no TeX installed); it passed a static check of braces, environments and citations. Placeholders: author block, paper's Math Qwen3 gold nDCG@10. Slides (17, Slides artifact): https://claude.ai/artifact/G9wwCmNLMM6iASyF3Cvb5p; placeholders on the cover ([Your name]) and the repro slide ([gold]).
- Report draft (Claude Doc): https://claude.ai/artifact/TQtu7rqXTX11nQ9LsnTmnA. The reference list was written from memory and must be checked. Writing has **9.0 gold docs per query** (all same-author snippets), not a single gold doc as stated in the Data section above.

## Next steps (open as of 2026-10-30)
Step 1 (B + D) and step 3 (cosine histogram) below are done; see the section above.
Done: E1–E5 on Math; E1–E4 and E2 on Writing. Still open, in the order proposed to the user (the user hadn't chosen yet):
1. **Writing fix attempt, B + D (local, no GPU, ~2 h), recommended first.**
   - B: re-index the existing profiles without the generic fields (Voice, Tone), keeping Signature phrases + Other habits, and/or weight profile terms by how rare they are across authors.
   - D: non-LLM style baselines, character n-gram TF-IDF and LUAR, to show whether the style signal exists. If strong, also try fusing them into E4 as a 5th index.
   - Spend GPU on C (new "distinctive vs typical blog" prompt, re-profile Writing, ~160 GPU-min) only if B shows profiles can carry signal. Otherwise write Writing up as a negative result (A).
2. **Ablations A1–A3 on Math only** (~16 GPU-min each, one Kaggle notebook): topic words allowed; Qwen2.5-3B vs 7B; 40 vs 100 words.
3. **Writing cosine-similarity histogram** (same- vs different-author profiles; required analysis, local).
4. Week 4: report, figures, slides.

Kaggle workflow: build a notebook with `scripts/build_kaggle_notebook.py --<mode>`; the user uploads it and runs Save & Run All (Commit), then drops the output zip in the project folder. Unzip with `unzip -n` (never overwrite) after checking its contents.

## Code layout
- `src/obliq/data.py` — `load_task(name)` → corpus, queries, gold/pooled qrels, exclusions (auto-downloads to `data/obliq/`)
- `src/obliq/runs.py` — `mask(run, excluded, k)`, run save/load (`runs/<task>/<system>.json`)
- `src/obliq/evaluate.py` — ranx metrics; asserts runs are masked
- `src/obliq/retrievers.py` — BM25 (rank-bm25 defaults) and Qwen3 dense + FAISS; embeddings cached in `cache/emb/`
- `scripts/run_baselines.py` — E1
- `scripts/run_profiles.py` — E3/E4 (profile indexes, RRF, dev-split choices, t-tests); `src/obliq/fusion.py` — `rrf()`, `dev_split()`
- `scripts/rerank.py` + `src/obliq/rerank.py` — E5 listwise re-rank (window 20 / step 10, top 50 of E4), LLM answers cached in `rerank/<task>/windows.jsonl`; `--export` → Kaggle input, `--llm` on Kaggle (`build_kaggle_notebook.py --rerank`), no flag → rebuild run locally from cache
- `scripts/run_rewrite.py` — E2: Qwen2.5-7B query rewrites (settings `math_rewrite` / `writing_rewrite`, prompts `prompts/rewrite_*.txt`; Writing = paper's authorship prompt verbatim, Math = modelled on the paper's Twitter template since none is published) + Qwen3 text retrieval → `reports/e2_<task>.md`. Rewrites are generated by `build_kaggle_notebook.py --rewrite`.
- `scripts/analyze.py --task math` — `reports/analysis_<task>.md`: headline table, cost, online latency, 10 helped / 10 hurt queries
- `scripts/profile_corpus.py` — full-corpus profiling (one vLLM process per GPU, shard files merged into the cache, resumable, wall time in `cost.jsonl`); `scripts/build_kaggle_notebook.py --profile` packs it into `kaggle/profile_corpus.ipynb`

## Stack

| Part | Tool |
|---|---|
| Data loading | `datasets` / `huggingface_hub` (download `math/`, `writing/`) |
| BM25 | `rank-bm25` (same as paper); Pyserini optional for speed |
| Dense | `Qwen/Qwen3-Embedding-0.6B` + FAISS exact inner product (via sentence-transformers) |
| Multi-vector (optional) | `lightonai/LateOn` + PyLate |
| Profiling LLM | `Qwen2.5-7B-Instruct` AWQ 4-bit via vLLM. Fallbacks: Qwen2.5-3B, or Llama-3.1-8B on a free API tier |
| Re-ranker (optional) | same Qwen2.5-7B, listwise (RankGPT-style) prompt, or small cross-encoder |
| Fusion & metrics | `ranx` — RRF, nDCG@10, Recall@k, paired significance tests |

Shared run-file format between all components: `qid -> {doc_id: score}`.

## Pipeline (step by step)

1. **Load and mask.** Load corpus, queries, qrels, pooled qrels, exclusion IDs. One `mask(run)` helper; every system goes through it.
2. **Reproduce baselines.** BM25 + Qwen3-0.6B on raw text. Targets: Math .029 / .143 (pooled); Writing .077 / .046.
3. **Design profile prompts.** One per task, hand-test on 20 docs. Output 60–120 words, fixed format.
4. **Profile every document.** vLLM batch → `profiles.jsonl` (`_id`, `profile`). Time on 200 docs first (estimate 1–2 GPU h/task — measure it).
5. **Profile every query** with the same prompt. Writing query = a snippet; Math query = technique description, so its prompt asks "what techniques would a solution need?".
6. **Build four indexes:** BM25-text, dense-text, BM25-profile, dense-profile.
7. **Retrieve and fuse.** Top 1,000 per index, RRF (k=60). Also weighted fusion tuned on the dev split.
8. **Optional re-rank.** Listwise LLM over top 50 of fused list, windows of 10–20.
9. **Evaluate.** Mask, then nDCG@10 (main), nDCG@50, Recall@10/50/100; gold **and** pooled qrels for Math.

## Profile prompts

The "do NOT mention the topic" instruction is the core of the method — profiles must capture hidden traits, not repeat the topic.

Current prompts live in `prompts/` (frozen after hand-test round 2; history and numbers in `reports/prompt_log.md`). The summary PDF's original prompts were round 1.
- `writing_style.txt` — distinctive author habits in 6 labelled fields (Voice, Sentences, Punctuation, Tone and humour, Signature phrases, Other habits). Used for Writing docs and queries.
- `math_problem.txt` — problem only; Techniques / Proof move / Key insight / Also known as; words only, no formulas. Used for Math docs **and** queries (queries are stripped of their boilerplate wrapper first).
- `math_problem_solution.txt` — same fields, but docs also see their solution from `final_dataset.json`.

**Fairness rule for Math solutions:** the benchmark corpus is problems only, and the paper's retrievers never saw solutions (only its "Oracle + Soln" did). The **main** Math system uses `math_problem` profiles. `math_soln` is a separately labelled variant that must never be presented as the headline number. Queries never see solutions.

Profiling: Qwen2.5-7B-Instruct-AWQ via vLLM on Kaggle, greedy + `frequency_penalty=0.3`. Cache: `profiles/<task>/<setting>-<hash>__<model>/{docs,queries}.jsonl`; the hash covers prompts + decoding. Always read profiles through `load_profiles()`, which applies `clean_profile()` (strips echoed "Passage:" text).

## Experiments

Research questions:
- **RQ1** Reproduce paper's BM25 and Qwen3-0.6B numbers?
- **RQ2** Do profiles alone beat raw text?
- **RQ3** Does text+profile fusion beat either alone?
- **RQ4** Does document-side profiling beat query-side rewriting (esp. Writing, where paper's rewriter fell to 0.018)?
- **RQ5** (optional) How much of the oracle gap (0.329 / 0.515) does a small open re-ranker close?

| ID | System | Answers |
|---|---|---|
| E1 | BM25 text, Qwen3-0.6B text (reproduction) | RQ1 |
| E2 | Our query rewriter (same open LLM) + Qwen3 text | RQ4 (fair same-LLM comparison) |
| E3 | BM25 profile, Qwen3 profile (P-only) | RQ2 |
| E4 | RRF over all four indexes — **main system** | RQ3 |
| E5 | E4 + LLM re-rank of top 50 (no gold injected) | RQ5 |
| A1 | Ablation: profile prompt *with* topic words allowed | Is "no topic words" what works? |
| A2 | Ablation: profiler 3B vs 7B | Effect of LLM size |
| A3 | Ablation: profile length 40 vs 100 words | Cost vs quality |

### Rules for fair numbers
- Exclusion mask on every run.
- Report gold and pooled nDCG@10 for Math; note pooled qrels came from the paper's systems and can under-score new systems that find unjudged relevant docs.
- Tune fusion weights and prompts on a **fixed 20% dev split** of queries; report on the remaining 80% and on all queries. Never tune on test.
- Paired t-test (or randomisation test) per query vs best baseline; claim a win only at **p < 0.05**.
- Report cost: GPU minutes to profile the corpus, seconds per query.

### Analysis to include
- 10 queries where profiles helped most and 10 where they hurt, with profile text.
- Writing-Style: same-author profiles closer than different-author profiles (cosine-similarity histogram).

## Milestones (20 Oct → mid-Nov 2026; final deadline TBC)

| Week | Work | Done when |
|---|---|---|
| 1 (20–26 Oct) | Data, mask, BM25 + Qwen3-0.6B baselines, ranx eval; vLLM on Kaggle; hand-test prompts on 20 docs/task | E1 within ±0.01 of paper |
| 2 (27 Oct–2 Nov) | Profile all Math + Writing docs and queries; profile indexes; RRF + weighted fusion; dev/test split; E2 rewriter | E2–E4 numbers exist |
| 3 (3–9 Nov) | Significance tests, cost measurement, E5 re-ranker, ablations A1–A3, error analysis (Twitter-Conflict if time) | Full results table + analysis |
| 4 (10–16 Nov) | Report (method, results, analysis), figures, reproducible repo, slides | Submitted |

## Risks and fallbacks

| Risk | Early sign | Fallback |
|---|---|---|
| Profiles don't beat baselines | E3/E4 below E1 on dev in week 2 | Report as a finding with error analysis — a careful negative result is valid |
| Profiles leak topic | Profiles mention subjects | Tighten prompt, filter topic nouns, use A1 to show the effect |
| Can't reproduce baselines | E1 off by > 0.02 | Check exclusion mask, qrels type (gold vs pooled), BM25 tokenisation; contact authors |
| Math docs lack solutions | Corpus has problems only | Profile from problem text; note paper's oracle gained from solutions (.329 → .473) |
| GPU time runs out | 200 docs take > 5 min | Qwen2.5-3B, shorter profiles, or free API tier |
| Pooled qrels under-score us | Many top hits unjudged | Report gold-only nDCG, hand-judge a sample of unjudged hits |
| Base paper is a preprint | — | Cite as arXiv preprint (May 2026); lead with Writing-Style (real authorship labels) |

## Key references
- ★ OBLIQ-Bench paper + dataset (base).
- ★ Nogueira et al., Doc2Query (2019) — method lineage; Doc2Query-- (ECIR 2023) — filtering expansions.
- ★ Qwen3-Embedding-0.6B.
- Weller et al., theoretical limits of embedding retrieval (ICLR 2026); BRIGHT (ICLR 2025).
- Query-side comparisons: HyDE (ACL 2023), Query2doc (EMNLP 2023), RankGPT (EMNLP 2023, listwise prompt for E5).
- LUAR (EMNLP 2021) — optional extra style-embedding baseline for Writing-Style.

## Working conventions for Claude
- Follow this file for all work in this project; consult the summary PDF and the paper PDF when details are needed.
- Prefer reproducibility: fixed seeds, fixed dev split saved to disk, cached LLM outputs, run files saved per system.
- Never report a number that wasn't computed with the mask applied; label every number gold vs pooled.
- GPU-heavy steps (profiling, dense encoding) should be written as Kaggle-runnable scripts/notebooks; BM25, fusion and eval should run locally on CPU.
