# Profile prompt log

Hand-test = 5 groups x 4 items per task (1 query + 3 gold docs per group), Qwen2.5-7B-Instruct-AWQ on Kaggle T4.
"Gap" = mean cosine (Qwen3-Embedding-0.6B) within group minus across groups. Raw-text gap is the bar to beat.
Only 20 items per test, so gaps are a direction, not a result.

## Round 1 (2026-10-29), greedy decoding

| Setting | Raw gap | Profile gap | Words (median) | Notes |
|---|---|---|---|---|
| writing | +0.046 | **+0.018** | 25 | Worse than raw text |
| math (problem only) | +0.127 | +0.140 | 39 | Format 20/20 |
| math_soln (docs see solutions) | +0.127 | +0.150 | 36 | Format 20/20 |

Reports: `handtest_writing_v1.md`, `handtest_math_v1.md`, `handtest_math_soln_v1.md`.

Findings:
- Writing: profiles were generic ("short sentences, rapid rhythm, uses commas, technical vocabulary") so all
  looked alike (cosine 0.72-0.74 regardless of author). The fixed order of dimensions encouraged safe answers.
  2/20 degenerate repetition loops under greedy decoding. Some topic leakage (Rust, TypeScript, biochemistry)
  and wrong labels ("third person" for first-person text).
- Math: the "assume an extremal object -> ..." example in the prompt was copied into 4 unrelated profiles
  (false similarity). LaTeX leaked into profiles. Profiles too short (26-53 words). Telescoping and
  implicit-function-theorem groups clustered well. Solutions help when the move is hidden in the problem
  (e.g. "integral representation").

## Round 2 changes
- Writing: ask what makes *this author* recognisable; ban traits most blogs share; fixed labelled fields
  (Voice, Sentences, Punctuation, Tone and humour, Signature phrases, Other habits); quote non-topical
  verbal tics from the passage.
- Math: removed all concrete proof-move examples; words only (no formulas/symbols); added
  "Also known as:" line with 2-3 alternative phrasings; 60-100 words.
- Decoding: vLLM frequency_penalty=0.3 (generated tokens only) to stop loops. Variant names now hash
  prompts + decoding, so round-1 and round-2 caches never mix.

## Round 2 results (2026-10-29), greedy + frequency_penalty 0.3

7/20 round-2 Writing profiles echoed the passage after the answer ("Passage: ..."). `clean_profile()` now
strips that on read; numbers below are after cleaning. No regeneration needed.

Leave-one-out P@3 (share of each item's top-3 neighbours in its own group; chance 0.158), added because
the cosine gap undersold BM25-friendly profiles:

| Setting | BM25 raw | BM25 profile | Dense raw | Dense profile | Cosine gap raw / profile |
|---|---|---|---|---|---|
| writing r1 | 0.267 | 0.183 | 0.367 | 0.300 | +0.046 / +0.018 |
| **writing r2** | 0.267 | **0.350** | 0.367 | 0.250 | +0.046 / +0.012 |
| math r1 | 0.317 | 0.550 | 0.450 | 0.483 | +0.127 / +0.140 |
| **math r2** | 0.317 | 0.533 | 0.450 | **0.517** | +0.127 / +0.130 |
| math_soln r1 | 0.317 | 0.567 | 0.450 | 0.600 | +0.127 / +0.150 |
| **math_soln r2** | 0.317 | **0.683** | 0.450 | **0.650** | +0.127 / +0.147 |

Reports: `handtest_*_v2.md` (as run on Kaggle) and `handtest_*.md` (re-scored with cleaning + P@3).

Findings:
- Writing r2 profiles help BM25 (quoted signature phrases are lexical signals) but not dense. Expect the
  profile-BM25 index to carry Writing; fusion decides the rest.
- Math r2 beats raw text on both retrievers; with solutions it is best (consistent with the paper's
  oracle gaining from solutions, .329 -> .473).
- Remaining issues: Math profiles still contain formula symbols in 7-9/20 despite the instruction; some
  Writing "signature phrases" are topical sentences rather than tics.

**Decision:** freeze round-2 prompts for full-corpus profiling. Each setting is only 60 neighbour slots
(0.08 = ~5 hits), so further tuning on 20 items would overfit; real tuning happens on the 20% dev split.
