# Run 009-fiit-urllib3-demo

- note: the claim pipeline (`notinspec claims run`) with the default extractors on the FIIT LiteLLM proxy, on the same pages as run 008; not human-labelled
- date: 2026-11-21, 16:27–16:55 UTC (extraction and grounding, 27 min, one pass)
- docs: urllib3 Sphinx XML in `core/examples/sphinx/urllib3`, pages `user-guide`, `reference/urllib3.util`, `v2-migration-guide` (81 prose chunks)
- command: `notinspec claims run --config core/examples/sphinx/urllib3/notinspec.yaml --source user-guide --source reference/urllib3.util --source v2-migration-guide --run-id fiit-demo-1` (provider `fiit`)
- extractors: `qwen3.8-flash-next` and `gemma4-26b-a4b-hpc`, both max tokens 16384, thinking off (`chat_template_kwargs` `enable_thinking: false`), prompt v1, claims parser v2
- NLI: `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` @ `b3546ea6b034`, fp32, argmax; grounding v1, premise `cited±1-in-block+lead-in`, windows v1, chunker v3 (same as run 008)
- git: `dc76084` on `core/fiit-extractors`; Windows laptop, NLI on 2 threads
- files: `claims.json`, `claims-store.jsonl` (with this file in its output folder, `notinspec claims run` reuses every answer and asks the proxy nothing). The raw `llm-calls.jsonl` (1.2 MB) is not committed.

## Extraction

| extractor | claims | chunks failed | claims skipped |
|---|---|---|---|
| qwen3.8-flash-next | 470 | 0 | 0 |
| gemma4-26b-a4b-hpc | 421 | 0 | 0 |

`Utilities > Retry`, cut off at 2048 tokens by Groq's qwen in run 008, was answered whole by both. Its later parameters now have kept claims (`retry_after_max` 6 vs 1 in run 008, `backoff_jitter` 4 vs 1, `allowed_methods` 8 vs 4).

## Grounding

| extractor | kept | citation_not_found | not_checkable | nli_neutral | nli_contradiction | id_missing |
|---|---|---|---|---|---|---|
| qwen3.8-flash-next | 449 (96 %) | 5 | 10 | 6 | 0 | 0 |
| gemma4-26b-a4b-hpc | 404 (96 %) | 7 | 7 | 2 | 0 | 1 |

Run 008 (Groq) for comparison: qwen/qwen3.8-27b 339 of 362 kept (94 %), gpt-oss-20b 338 of 446 (76 %, 79 `not_checkable`: it quoted signatures and code). 853 kept claims now vs 677.

## Quick signals (not labels)

- Kept claims that start without a named subject ("It …", "This …", "Returns …", "The parameter …"; a regex, so a rough count): qwen 22 (5 %), gemma 29 (7 %); run 008: 22 (6 %) and 42 (12 %).
- **The two extractors agree far more than before.** 292 of gemma's 404 kept claims (72 %) have a near-duplicate from qwen in the same chunk (token Jaccard ≥ 0.6); in run 008, 149 of gpt-oss's 338 (44 %). The second extractor adds fewer new facts, and K5a (duplicates within a chunk) matters more.
- Whether the kept claims are right is what labels would measure; none were made.
