# Run 010-fiit-hydra-zen

- note: the claim pipeline (`notinspec claims run`) with the default FIIT extractors on **all of hydra-zen**, the first library with NumPy docstrings (field shape C, SPEC §6.1) and the first run outside urllib3; not human-labelled
- date: 2026-11-24, two passes into the same claims store:
  1. 11:13–11:29 UTC, 76 chunks (`--source "tutorials/*" --source generated/hydra_zen.builds --source generated/hydra_zen.ZenStore`): 11 min of extraction, 5 min of NLI
  2. 11:40–12:36 UTC, all 236 chunks; the 75 prose chunks of pass 1 were reused and 154 were asked: 30 min of extraction, 26 min of NLI over all claims
- docs: hydra-zen v0.17.2 Sphinx XML in `core/examples/sphinx/hydra-zen`, 236 chunks, of them 229 with prose (~78k tokens)
- command (pass 2, which wrote these files): `notinspec claims run --config core/examples/sphinx/hydra-zen/notinspec.yaml --run-id fiit-hydra-zen-2` (provider `fiit`, default extractors)
- extractors: `qwen3.8-flash-next` and `gemma4-26b-a4b-hpc`, both max tokens 16384, thinking off, prompt v1, claims parser v2 (same as run 009). Only these two free models were called (458 requests, checked in `llm-calls.jsonl`).
- NLI: `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` @ `b3546ea6b034`, fp32, argmax; grounding v2, premise `cited±1-in-block+lead-in`, windows v1, chunker v3
- git: `b5c4ce4` (main); Windows laptop, Python 3.12.10, torch on 10 threads
- tokens: 546k prompt + 249k completion over both passes; the longest answer was 4.7k completion tokens, every answer ended with `stop`
- files: `claims.json`, `claims-store.jsonl` (with this file in its output folder, `notinspec claims run` reuses every answer and asks the proxy nothing). The raw `llm-calls.jsonl` (2.7 MB + 1.2 MB) is not committed.

## Extraction

| extractor | claims | chunks failed | claims skipped |
|---|---|---|---|
| qwen3.8-flash-next | 1785 | 0 | 0 |
| gemma4-26b-a4b-hpc | 1431 | 0 | 0 |

## Grounding

| extractor | kept | citation_not_found | not_checkable | nli_neutral | nli_contradiction | id_missing |
|---|---|---|---|---|---|---|
| qwen3.8-flash-next | 1603 (90 %) | 55 | 50 | 65 | 3 | 9 |
| gemma4-26b-a4b-hpc | 1280 (89 %) | 29 | 43 | 43 | 4 | 32 |

Run 009 (urllib3, 81 chunks): 96 % kept for both.

By page type (kept / claims):

| pages | qwen | gemma |
|---|---|---|
| API reference (`generated/*`, `api_reference`) | 91 % of 842 | 87 % of 745 |
| changelog (`changes`) | 92 % of 483 | 95 % of 396 |
| tutorials (`tutorials/*`) | 87 % of 215 | 84 % of 129 |
| explanation (`explanation/*`) | 79 % of 105 | 91 % of 78 |
| how-to (`how_to/*`) | 89 % of 88 | 92 % of 51 |
| other (`index`, section indexes) | 83 % of 52 | 94 % of 32 |

## Why claims were dropped

One reader went through the drops and a sample of kept claims (not labels, nobody else checked). **Most drops on hydra-zen are false drops caused by the grounding, not wrong claims.**

- **`id_missing` (41): 35 are one pattern.** On autosummary pages (`generated/*`) the breadcrumb is `hydra-zen > hydra_zen.ZenStore > ZenStore`: the page title is the full path, the heading the short name. The extractor joins them into a path that does not exist (`hydra_zen.ZenStore.ZenStore.__call__` 15×, `hydra_zen.wrapper.Zen.Zen.__call__` 6×, …; gemma 29, qwen 6). The facts themselves read right. Related to the full-path item in #35.
- **`citation_not_found` (84):**
  - ~42 quote a list's lead-in together with one item (`Values of the following types can be specified directly in configs:\n\n- bool`), one claim per item, mostly qwen. The claims are right. The premise rule already takes the list lead-in, the citation check does not.
  - 22 use `...` across blocks or list items (20 qwen, mostly the changelog); #46 accepts `...` only within one prose unit.
  - the rest are real paraphrases (e.g. gemma adds a subject: "they do not populate the global store …").
- **`nli_contradiction` (7): all 7 read as false contradictions.** Examples: `hydra_convert` "partial" (the premise starts mid-sentence, "list, respectively. …", and ends with the next option, `"all"`), and "instantiates with execution checks disabled, unless a whitelist is active" against a correct claim with the negation turned around.
- **`nli_neutral` (108): 14 of 15 read say what the docs say.** The premise misses what the claim names: it ends with a colon before a code block or list ("holds a mapping of:", "to exclude parameters by index:"), or refers to an example (`this build`, `DNN`, `bar`, "this change"). One rests on code the premise does not contain (`job.return_value`). hydra-zen's NumPy docstrings and tutorials are full of examples, so this shows up here and hardly did on urllib3.
- `not_checkable` (93): the citation is in code (e.g. a comment in an example), as designed.

## Quick signals (not labels)

- 14 kept claims drawn at random all match the docs. Changelog claims are often stated without their version ("Parameters can be excluded from auto-population by name using the `zen_exclude` field."): they are *change* claims, which the pipeline does not turn into `Change` yet (SPEC §6.3, #35).
- Kept claims that start without a named subject (same regex as run 009): qwen 93 (6 %), gemma 76 (6 %).
- 915 of gemma's 1280 kept claims (71 %) have a near-duplicate from qwen in the same chunk (token Jaccard ≥ 0.6); run 009: 72 %.
- No chunk failed or was cut off, also on the longest API pages (`builds`, `ZenStore`).

## What this means

- The two free extractors handle a third docstring shape and a changelog without failures, and what they say reads right. Precision of the extractors is not the problem on these pages; whether they miss facts (recall) is not measured (#52).
- The kept rate fell from 96 % to ~90 % because of the grounding: the autosummary breadcrumb, list citations and premises cut before code or lists. These need fixes with a `GROUNDING_VERSION` bump, checked on labelled data first.
