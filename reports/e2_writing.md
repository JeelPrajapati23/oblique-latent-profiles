# E2 query rewriting: writing

Rewriter: `Qwen/Qwen2.5-7B-Instruct-AWQ` (same LLM and decoding as the profiles), prompt `prompts/rewrite_writing.txt` (the paper's authorship rewriter prompt, verbatim).
Retriever: Qwen3-Embedding-0.6B over raw text; query prompt chosen on dev: `E2_rewrite_qwen3-0.6b_query`.
Answers cut off by the 220-token cap before the JSON closed (partial rewrite used): 33/512.
Paper, same comparison: Gemini .164 -> GPT-5.2 rewriter + Gemini .018.

All numbers masked; cells are gold. Test = the fixed 80% split. p = paired t-test on test nDCG@10; +/- = better/worse on average.

| system | ndcg@10 | ndcg@50 | recall@10 | recall@50 | recall@100 | test nDCG@10 | p vs best E1 (test) | p vs E2 (test) |
|---|---|---|---|---|---|---|---|---|
| E1 bm25_text_split (best baseline) | 0.099 | 0.135 | 0.082 | 0.174 | 0.245 | 0.095 | - | 1.94e-25+ |
| E1 qwen3-0.6b_text_none (E2's retriever, original query) | 0.045 | 0.060 | 0.040 | 0.076 | 0.107 | 0.040 | 2.46e-15- | 4.06e-07+ |
| E2 E2_rewrite_qwen3-0.6b_query | 0.023 | 0.036 | 0.021 | 0.051 | 0.075 | 0.020 | 1.94e-25- | - |
| E4 RRF all 4 (main) | 0.060 | 0.094 | 0.053 | 0.134 | 0.196 | 0.056 | 5.06e-09- | 1.81e-12+ |

## Example rewrites

**1**: Identify texts that share the same authorial voice as the original, focusing on the use of technical jargon like 'adversarial robustness', 'reward hacking', and 'legislate from the bench'. Look for a similar emphasis on the need for scaling up compute and empirical experiments to improve alignment. Also, seek out a tone that balances optimism about progress with caution about the risks of waiting for AI to solve complex problems. The author's writing often includes detailed explanations of techn

**10**: Identify texts by an author who frequently uses colloquial language and humor, such as inserting smiley faces and making light-hearted observations about physical effort. The author also employs a conversational tone, often referencing specific academic resources like STOC or FOCS proceedings, and discusses topics in depth using extended surveys. Additionally, the author highlights new resources and courses, particularly those related to theoretical computer science (TCS), and shares discoveries

**1001**: Analyze texts that exhibit a focus on the trend of increasing AI productivity per unit of human input, rather than on the inevitability of Artificial General Intelligence (AGI). Look for discussions that challenge the concept of AGI timelines and instead emphasize the practical benefits and measurable trends in AI capabilities. The texts should also explore the potential for a future where human input is minimized in favor of autonomous AI output, and consider whether this could lead to a scenar

