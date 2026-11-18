# Run 008-core-pipeline-urllib3-demo

- note: first run of the claim pipeline in `core/` (`notinspec claims run`) on real docs with real models; human labels pending
- date: 2026-11-17 22:52 UTC (extraction) to 2026-11-18 07:50 UTC (retries + grounding; the PC slept in between)
- docs: urllib3 Sphinx XML in `core/examples/sphinx/urllib3`, pages `user-guide`, `reference/urllib3.util`, `v2-migration-guide` (81 prose chunks)
- command: `notinspec claims extract` (run ID `urllib3-demo-1`), then `notinspec claims run` (`urllib3-demo-2`, reuses the stored answers and asks again only for failed chunks), both with `--source user-guide --source reference/urllib3.util --source v2-migration-guide`
- extractors: `qwen/qwen3.8-27b` (provider defaults), `openai/gpt-oss-20b` (max tokens 8192, reasoning effort `low`), prompt v1
- NLI: `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` @ `b3546ea6b034`, fp32, argmax; grounding v1, premise `cited±1-in-block+lead-in`, sentences v1, chunker v3
- git: `57fdabb` on `core/claims-pipeline`; Python 3.12.6, torch 2.15.0+cpu, transformers 5.23.0, Windows laptop
- files: `claims.json` (every claim with status, premise, scores, missing identifiers), `claims-store.jsonl` (the extractor answers: `notinspec claims run` with this file as `claims-store.jsonl` in its output folder reproduces `claims.json` without Groq). The raw `llm-calls.jsonl` (178 records: 165 answers, 13 errors; 1.3 MB) is not committed.

## Extraction

| extractor | claims | chunks failed | claims skipped | tokens (prompt + completion) | per chunk |
|---|---|---|---|---|---|
| qwen/qwen3.8-27b | 362 | 1 (`truncated`: Groq's default completion limit) | 3 (empty `id`) | 104 790 over 84 answered calls | ~1.3k |
| gpt-oss-20b, effort low | 446 | 0 | 0 | 137 612 over 81 calls | ~1.7k |

- **Groq has an output-tokens-per-minute limit.** qwen: 1 000 output tokens/min (from the 429 body, "Request too large … on output tokens per minute (OTPM): Limit 1000"). The "requested" number in the body was the size of the previous answer, so a long answer blocks the next request for about a minute. 13 of 81 qwen chunks failed this way in the first pass, after the client's 5 retries. All of them passed when asked again. gpt-oss-20b never hit it.
- **gpt-oss-20b at the default effort** used ~3.5k tokens per chunk (B's recordings), so the demo would not have fit one day's 200k tokens. At `low` it used 1.7k. The cost: some of its claims are not self-contained ("Get the value for the read timeout.", "Returns: Value to use for the read timeout."), and it lists many facts from signatures and code (79 `not_checkable` vs 9 for qwen).
- qwen once returned a control character instead of a typographic apostrophe (`you\x02re`, `we\x00ve`), so 3 of its citations were not found.

## Grounding

| extractor | kept | citation_not_found | not_checkable | nli_neutral | nli_contradiction | id_missing |
|---|---|---|---|---|---|---|
| qwen/qwen3.8-27b | 339 | 9 | 9 | 3 | 0 | 2 |
| gpt-oss-20b | 338 | 18 | 79 | 6 | 1 | 4 |

- 25 citations are in the prose more than once (docstrings repeat sentences). Every one of them gave a single premise (the repeats were in the same ±1 window, or in the entry of a parameter the claim names), so NLI never had to choose. No premise was cut at 512 tokens.
- `citation_not_found`: besides the 3 broken apostrophes, "..." inside a citation (against prompt rule 5) and gpt-oss quoting code with literal `\n`.
- `id_missing` (6): 3 look like false drops. The claim uses the full path, but the section uses only the short name (`urllib3.util.resolve_cert_reqs` vs `resolve_cert_reqs`, `urllib3.util.parse_url` vs `parse_url()`, `urllib3.PoolManager.request` vs `request()`). The project prefix rule strips only `urllib3.`. The other 3 name `urllib3.request` on "Files & Binary Data", a section that never names it. The rule is not changed here, because the human labels should decide (it was tuned on run 007's sample).
- NLI drops only 10 of 808 claims, far fewer than in runs 006/007. Those runs had hand-made negatives and outside claims, and this run has only real extractor claims. Whether the 677 kept ones are right is what the labels measure.

## Human labels (pending)

Blind sample of 180 claims, seed `20261117`, built by `../../labeling/build_008.py` from `claims.json`. It holds every claim NLI or the identifier check dropped (16), every `citation_not_found` claim (27), 10 random `not_checkable` claims, and 127 random kept ones (63 from the guides, 64 from the API reference). Same labelling rules as run 007 (`../../labeling/template.html`). When `labels-human-008.csv` is in, run:

```sh
uv run python -I -X utf8 experiments/nli/runs/008-core-pipeline-urllib3-demo/posthoc/eval_labels.py \
    experiments/nli/runs/008-core-pipeline-urllib3-demo/claims.json <hidden>/key-008-DO-NOT-OPEN.csv experiments/nli/labels-human-008.csv
```

It reports precision of the kept claims (guide vs. API reference, per extractor), the good claims per drop reason (recall), and the false drops of the identifier check.
