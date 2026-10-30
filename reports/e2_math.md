# E2 query rewriting: math

Rewriter: `Qwen/Qwen2.5-7B-Instruct-AWQ` (same LLM and decoding as the profiles), prompt `prompts/rewrite_math.txt` (the paper gives no Math rewriter prompt; this follows its Twitter rewriter template).
Retriever: Qwen3-Embedding-0.6B over raw text; query prompt chosen on dev: `E2_rewrite_qwen3-0.6b_none`.
Answers not parseable as the expected format (whole answer used instead): 0/151.
Paper, same comparison: Gemini .147 -> GPT-5.2 rewriter + Gemini .185 (pooled).

All numbers masked; cells are gold/pool. Test = the fixed 80% split. p = paired t-test on test nDCG@10; +/- = better/worse on average.

| system | ndcg@10 | ndcg@50 | recall@10 | recall@50 | recall@100 | test nDCG@10 | p vs best E1 (test) | p vs E2 (test) |
|---|---|---|---|---|---|---|---|---|
| E1 qwen3-0.6b_text_none (best baseline) | 0.117/0.147 | 0.151/0.184 | 0.074/0.092 | 0.227/0.257 | 0.313/0.341 | 0.113/0.144 | - | 0.641+/0.829- |
| E2 E2_rewrite_qwen3-0.6b_none | 0.104/0.141 | 0.144/0.179 | 0.083/0.105 | 0.239/0.265 | 0.341/0.366 | 0.109/0.146 | 0.641-/0.829+ | - |
| E4 RRF all 4 (main) | 0.142/0.175 | 0.184/0.215 | 0.117/0.135 | 0.282/0.306 | 0.383/0.410 | 0.139/0.173 | 0.0234+/0.0126+ | 0.0122+/0.029+ |

## Example rewrites

**q00076**: Prove or disprove that the determinant of the $n \times n$ matrix $T_n$ with entries $\tan((i+j-1)x)$ follows a specific product formula involving trigonometric functions and powers of secant. This query captures the core reasoning pattern needed to solve the problem and is phrased to match problems from other areas that require similar insights, while remaining concise and avoiding verbose academic language.

**q00077**: Determine the sum using combinatorial identities involving binomial coefficients and negative binomial terms. Query: Evaluate the expression by applying combinatorial techniques with binomial coefficients and negative indices. Query: Solve the sum by leveraging combinatorial methods and properties of binomial coefficients.

**q00096**: Identify problems that require showing a sum involving a recursively defined function equals a product of odd terms, without using similar vocabulary. Query: Find problems where the key insight is to relate a sum of terms from a recursive function to a product of increasing odd numbers, using different mathematical contexts.

