# E3/E4 results: math

All numbers masked. Cells are gold/pool. Paper's best single-stage retriever (Gemini-2-Embedding) nDCG@10 = .147 (pooled).

Dev = fixed 20% split (30 queries, `splits/math.json`), test = other 121. p = paired t-test on test nDCG@10 vs `E1 qwen3-0.6b_text_none`; +/- = better/worse on average. Claim a win only at p < 0.05.

- Text components picked on dev: `bm25_text_word`, `qwen3-0.6b_text_none`; significance baseline: `qwen3-0.6b_text_none`.
- math: profile components picked on dev: `bm25_profile_word`, `qwen3-0.6b_profile_query`; weights (BM25-t, dense-t, BM25-p, dense-p) tuned on dev: [0, 2, 0.5, 0.5].
- math_soln: profile components picked on dev: `soln_bm25_profile_word`, `soln_qwen3-0.6b_profile_query`; weights (BM25-t, dense-t, BM25-p, dense-p) tuned on dev: [0.5, 0.5, 0, 2].

| system | ndcg@10 | ndcg@50 | recall@10 | recall@50 | recall@100 | dev nDCG@10 | test nDCG@10 | p vs E1 qwen3-0.6b_text_none (test) |
|---|---|---|---|---|---|---|---|---|
| E1 bm25_text_word | 0.060/0.072 | 0.084/0.099 | 0.040/0.046 | 0.132/0.144 | 0.178/0.188 | 0.040/0.053 | 0.065/0.077 | 7.17e-05-/4.14e-06- |
| E1 qwen3-0.6b_text_none | 0.117/0.147 | 0.151/0.184 | 0.074/0.092 | 0.227/0.257 | 0.313/0.341 | 0.132/0.162 | 0.113/0.144 | -/- |
| RRF text only (BM25-t + dense-t) | 0.098/0.124 | 0.140/0.168 | 0.080/0.097 | 0.223/0.243 | 0.293/0.317 | 0.093/0.119 | 0.100/0.125 | 0.201-/0.121- |
| E3 bm25_profile_word | 0.121/0.144 | 0.158/0.182 | 0.091/0.104 | 0.244/0.261 | 0.344/0.359 | 0.114/0.141 | 0.123/0.145 | 0.494+/0.904+ |
| E3 qwen3-0.6b_profile_query | 0.120/0.134 | 0.164/0.181 | 0.098/0.101 | 0.259/0.274 | 0.358/0.378 | 0.138/0.139 | 0.116/0.132 | 0.851+/0.361- |
| E3 RRF profile (BM25-p + dense-p) | 0.124/0.146 | 0.171/0.194 | 0.094/0.107 | 0.268/0.287 | 0.368/0.382 | 0.117/0.136 | 0.126/0.148 | 0.351+/0.735+ |
| E4 RRF all 4 (k=60) | 0.142/0.175 | 0.184/0.215 | 0.117/0.135 | 0.282/0.306 | 0.383/0.410 | 0.152/0.183 | 0.139/0.173 | 0.0234+/0.0126+ |
| E4 weighted RRF all 4 w=[0, 2, 0.5, 0.5] | 0.134/0.171 | 0.171/0.209 | 0.094/0.114 | 0.255/0.287 | 0.359/0.387 | 0.174/0.207 | 0.124/0.162 | 0.186+/0.0316+ |
| E3 soln_bm25_profile_word [soln variant] | 0.128/0.140 | 0.175/0.187 | 0.120/0.123 | 0.258/0.267 | 0.344/0.358 | 0.106/0.125 | 0.134/0.143 | 0.278+/0.99- |
| E3 soln_qwen3-0.6b_profile_query [soln variant] | 0.142/0.162 | 0.195/0.215 | 0.123/0.131 | 0.295/0.307 | 0.409/0.422 | 0.112/0.131 | 0.149/0.170 | 0.0459+/0.134+ |
| E3 RRF profile (BM25-p + dense-p) [soln variant] | 0.147/0.161 | 0.195/0.213 | 0.141/0.145 | 0.291/0.311 | 0.405/0.423 | 0.129/0.143 | 0.151/0.166 | 0.0309+/0.201+ |
| E4 RRF all 4 (k=60) [soln variant] | 0.144/0.174 | 0.202/0.232 | 0.120/0.138 | 0.325/0.348 | 0.437/0.459 | 0.132/0.156 | 0.147/0.178 | 0.00826+/0.00731+ |
| E4 weighted RRF all 4 w=[0.5, 0.5, 0, 2] [soln variant] | 0.162/0.195 | 0.203/0.235 | 0.134/0.149 | 0.309/0.331 | 0.439/0.456 | 0.159/0.187 | 0.163/0.197 | 0.000871+/0.000361+ |

The `[soln variant]` rows profile documents together with their solutions. The paper's retrievers never saw solutions, so these rows are not the headline number.
