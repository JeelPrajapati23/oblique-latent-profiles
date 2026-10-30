# Writing fix attempt: B (filtered profiles) + D (non-LLM style baselines)

All numbers masked, gold qrels. Paper's Gemini-2-Embedding nDCG@10 = .164. Dev = 102 queries, test = 410. p = paired t-test on test nDCG@10 vs `E1 bm25_text_split`; +/- = better/worse on average.

- Field coverage in doc profiles: Voice 100%, Sentences 100%, Punctuation 100%, Tone and humour 100%, Signature phrases 100%, Other habits 100%
- B `sig_habits` keeps ['Signature phrases', 'Other habits']; 0 doc profiles end up empty.
- B `no_voice_tone` keeps ['Sentences', 'Punctuation', 'Signature phrases', 'Other habits']; 0 doc profiles end up empty.
- Picked on dev: best B run `B_bm25_profile_no_voice_tone`, best char n-gram run `D_tfidf_char_35`.

| system | ndcg@10 | ndcg@50 | recall@10 | recall@50 | recall@100 | dev nDCG@10 | test nDCG@10 | p vs E1 bm25_text_split (test) |
|---|---|---|---|---|---|---|---|---|
| E1 bm25_text_split | 0.099 | 0.135 | 0.082 | 0.174 | 0.245 | 0.117 | 0.095 | - |
| E1 qwen3-0.6b_text_none | 0.045 | 0.060 | 0.040 | 0.076 | 0.107 | 0.066 | 0.040 | 2.46e-15- |
| E3 profile full (BM25-p word) | 0.008 | 0.017 | 0.007 | 0.028 | 0.046 | 0.009 | 0.008 | 2.76e-30- |
| E4 RRF all 4 (k=60) | 0.060 | 0.094 | 0.053 | 0.134 | 0.196 | 0.073 | 0.056 | 5.06e-09- |
| B bm25_profile_sig_habits | 0.006 | 0.011 | 0.005 | 0.018 | 0.031 | 0.005 | 0.006 | 8.74e-31- |
| B qwen3_profile_sig_habits | 0.004 | 0.008 | 0.004 | 0.016 | 0.030 | 0.003 | 0.004 | 2.35e-34- |
| B bm25_profile_no_voice_tone | 0.006 | 0.012 | 0.005 | 0.019 | 0.032 | 0.007 | 0.006 | 7.57e-32- |
| B qwen3_profile_no_voice_tone | 0.004 | 0.011 | 0.005 | 0.021 | 0.038 | 0.002 | 0.005 | 9.02e-33- |
| D tfidf_char_24 | 0.092 | 0.138 | 0.080 | 0.194 | 0.266 | 0.096 | 0.091 | 0.523- |
| D tfidf_char_35 | 0.091 | 0.136 | 0.079 | 0.191 | 0.266 | 0.102 | 0.088 | 0.192- |
| D tfidf_char_wb_25 | 0.086 | 0.126 | 0.076 | 0.176 | 0.244 | 0.098 | 0.083 | 0.0416- |
| D style_emb (Wegmann) | 0.075 | 0.113 | 0.068 | 0.159 | 0.210 | 0.081 | 0.074 | 0.0188- |
| E4 with B (B_bm25_profile_no_voice_tone) replacing BM25-p/dense-p | 0.075 | 0.111 | 0.066 | 0.152 | 0.205 | 0.096 | 0.069 | 5.66e-06- |
| E4 + D (D_tfidf_char_35) as 5th index | 0.090 | 0.136 | 0.078 | 0.188 | 0.253 | 0.106 | 0.086 | 0.113- |
| BM25-t + D (D_tfidf_char_35) | 0.107 | 0.153 | 0.086 | 0.201 | 0.282 | 0.130 | 0.101 | 0.0416+ |
| BM25-t + D style_emb | 0.120 | 0.177 | 0.108 | 0.244 | 0.319 | 0.129 | 0.118 | 0.000955+ |
| BM25-t + D (D_tfidf_char_35) + D style_emb | 0.128 | 0.183 | 0.104 | 0.244 | 0.353 | 0.139 | 0.125 | 5.68e-09+ |
| E4 + D char + D style_emb (6 indexes) | 0.110 | 0.159 | 0.097 | 0.217 | 0.305 | 0.124 | 0.106 | 0.0483+ |
