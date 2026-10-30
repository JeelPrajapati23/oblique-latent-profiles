# E3/E4 results: writing

All numbers masked. Cells are gold. Paper's best single-stage retriever (Gemini-2-Embedding) nDCG@10 = .164.

Dev = fixed 20% split (102 queries, `splits/writing.json`), test = other 410. p = paired t-test on test nDCG@10 vs `E1 bm25_text_split`; +/- = better/worse on average. Claim a win only at p < 0.05.

- Text components picked on dev: `bm25_text_split`, `qwen3-0.6b_text_none`; significance baseline: `bm25_text_split`.
- writing: profile components picked on dev: `bm25_profile_word`, `qwen3-0.6b_profile_query`; weights (BM25-t, dense-t, BM25-p, dense-p) tuned on dev: [2, 1, 0.5, 0].

| system | ndcg@10 | ndcg@50 | recall@10 | recall@50 | recall@100 | dev nDCG@10 | test nDCG@10 | p vs E1 bm25_text_split (test) |
|---|---|---|---|---|---|---|---|---|
| E1 bm25_text_split | 0.099 | 0.135 | 0.082 | 0.174 | 0.245 | 0.117 | 0.095 | - |
| E1 qwen3-0.6b_text_none | 0.045 | 0.060 | 0.040 | 0.076 | 0.107 | 0.066 | 0.040 | 2.46e-15- |
| RRF text only (BM25-t + dense-t) | 0.085 | 0.123 | 0.072 | 0.162 | 0.225 | 0.111 | 0.079 | 0.00508- |
| E3 bm25_profile_word | 0.008 | 0.017 | 0.007 | 0.028 | 0.046 | 0.009 | 0.008 | 2.76e-30- |
| E3 qwen3-0.6b_profile_query | 0.009 | 0.018 | 0.008 | 0.030 | 0.052 | 0.017 | 0.008 | 1.27e-30- |
| E3 RRF profile (BM25-p + dense-p) | 0.010 | 0.020 | 0.009 | 0.034 | 0.058 | 0.014 | 0.009 | 1.23e-29- |
| E4 RRF all 4 (k=60) | 0.060 | 0.094 | 0.053 | 0.134 | 0.196 | 0.073 | 0.056 | 5.06e-09- |
| E4 weighted RRF all 4 w=[2, 1, 0.5, 0] | 0.098 | 0.137 | 0.085 | 0.181 | 0.252 | 0.125 | 0.091 | 0.453- |
