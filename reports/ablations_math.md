# Ablations A1-A3 (Math)

All numbers masked, cells gold/pool. Components fixed to the main system's (no re-tuning). Dev = 30 / test = 121 queries; p = paired t-test on test nDCG@10 vs `main (7B, no topic, 60-100 words): E4 RRF all 4`.

| variant | cache | mean words / doc profile | doc profiles with a banned topic word | GPU-min |
|---|---|---|---|---|
| main (7B, no topic, 60-100 words) | `math-ee895b__Qwen2.5-7B-Instruct-AWQ` | 59 | 42% | 16 |
| A1 topic words allowed | `math_topic-1af30a__Qwen2.5-7B-Instruct-AWQ` | 61 | 48% | 21 |
| A2 3B profiler | `math-ee895b__Qwen2.5-3B-Instruct-AWQ` | 55 | 40% | 13 |
| A3 ~40-word profiles | `math_short-07ea6b__Qwen2.5-7B-Instruct-AWQ` | 43 | 35% | 16 |

| system | ndcg@10 | ndcg@50 | recall@10 | recall@50 | recall@100 | dev nDCG@10 | test nDCG@10 | p vs main (7B, no topic, 60-100 words): E4 RRF all 4 (test) |
|---|---|---|---|---|---|---|---|---|
| main (7B, no topic, 60-100 words): E3 RRF profile | 0.124/0.146 | 0.171/0.194 | 0.094/0.107 | 0.268/0.287 | 0.368/0.382 | 0.117/0.136 | 0.126/0.148 | 0.169-/0.0183- |
| main (7B, no topic, 60-100 words): E4 RRF all 4 | 0.142/0.175 | 0.184/0.215 | 0.117/0.135 | 0.282/0.306 | 0.383/0.410 | 0.152/0.183 | 0.139/0.173 | -/- |
| A1 topic words allowed: E3 RRF profile | 0.116/0.147 | 0.153/0.185 | 0.105/0.121 | 0.252/0.274 | 0.339/0.361 | 0.149/0.173 | 0.107/0.141 | 0.00478-/0.0114- |
| A1 topic words allowed: E4 RRF all 4 | 0.142/0.178 | 0.177/0.217 | 0.112/0.129 | 0.265/0.297 | 0.371/0.394 | 0.165/0.204 | 0.136/0.172 | 0.732-/0.902- |
| A2 3B profiler: E3 RRF profile | 0.091/0.108 | 0.126/0.145 | 0.072/0.082 | 0.191/0.207 | 0.279/0.293 | 0.110/0.129 | 0.087/0.103 | 2.12e-05-/9.67e-07- |
| A2 3B profiler: E4 RRF all 4 | 0.128/0.149 | 0.164/0.190 | 0.092/0.106 | 0.231/0.256 | 0.332/0.358 | 0.121/0.140 | 0.130/0.152 | 0.456-/0.0982- |
| A3 ~40-word profiles: E3 RRF profile | 0.120/0.136 | 0.151/0.170 | 0.109/0.117 | 0.219/0.239 | 0.312/0.332 | 0.109/0.115 | 0.123/0.141 | 0.239-/0.0266- |
| A3 ~40-word profiles: E4 RRF all 4 | 0.138/0.169 | 0.172/0.204 | 0.118/0.133 | 0.252/0.279 | 0.361/0.389 | 0.148/0.174 | 0.136/0.167 | 0.719-/0.567- |

E3 (profiles only) vs main E3, test queries:

| variant | gold: mean vs main (p) | pool: mean vs main (p) |
|---|---|---|
| A1 topic words allowed | 0.107 vs 0.126 (p = 0.205) | 0.141 vs 0.148 (p = 0.604) |
| A2 3B profiler | 0.087 vs 0.126 (p = 0.00746) | 0.103 vs 0.148 (p = 0.00566) |
| A3 ~40-word profiles | 0.123 vs 0.126 (p = 0.88) | 0.141 vs 0.148 (p = 0.665) |
