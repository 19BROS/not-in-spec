# Run 006-realistic-negatives

- note: 2 extractors (sonnet-medium, flash-3.6-high) on 4 new sections (changelog, long, httpx), outside/beyond + cross-section claims, fact-checkers MiniCheck + HHEM
- started: `2026-11-07T18:37:51`
- models: `['cross-encoder/nli-deberta-v3-base', 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli', 'vectara/hallucination_evaluation_model', 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli', 'lytang/MiniCheck-DeBERTa-v3-Large']`
- contexts: `['breadcrumb']`
- premises: `['window', 'local']`
- radius: `1`
- sections: `all`
- batch: `8`
- git: `{'commit': 'e8077b00a58fcaac2cbebef8f3f9dc7762970048', 'branch': 'feat/nli-and-extractors-testing', 'dirty_experiment_files': True}`
- inputs: `{'pairs_windows_sha256': 'a04e136ff451', 'labels_sha256': '44ded39573b9'}`
- versions: `{'python': '3.12.10', 'torch': '2.15.0+cpu', 'transformers': '5.22.2'}`
- threads: `10`
- seconds: `{'cross-encoder/nli-deberta-v3-base': {'revision': '', 'breadcrumb/window': {'seconds': 270.8, 'scored': 828, 'unique': 1080}, 'breadcrumb/local': {'seconds': 65.9, 'scored': 427, 'unique': 571}}, 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli': {'revision': '', 'breadcrumb/window': {'seconds': 273.2, 'scored': 828, 'unique': 1080}, 'breadcrumb/local': {'seconds': 67.8, 'scored': 427, 'unique': 571}}, 'vectara/hallucination_evaluation_model': {'revision': 'de9a5e6ba9ba49531a022dba17e35ffeb2a6fad8', 'breadcrumb/window': {'seconds': 354.9, 'scored': 1080, 'unique': 1080}, 'breadcrumb/local': {'seconds': 87.7, 'scored': 553, 'unique': 571}}, 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli': {'revision': '', 'breadcrumb/window': {'seconds': 862.9, 'scored': 828, 'unique': 1080}, 'breadcrumb/local': {'seconds': 218.8, 'scored': 427, 'unique': 571}}, 'lytang/MiniCheck-DeBERTa-v3-Large': {'revision': '', 'breadcrumb/window': {'seconds': 1173.8, 'scored': 1080, 'unique': 1080}, 'breadcrumb/local': {'seconds': 282.7, 'scored': 553, 'unique': 571}}}`
- finished: `2026-11-07T19:38:53`

## Metrics vs labels.csv (609 labelled claims, annotator: claude-draft)

Keep = NLI says entailment (claim survives grounding). Dropped by the citation check = not kept. `nb` = without borderline labels. Premise `window` = NLI window, `local` = cited sentence(s) +-1, `both` = kept only if both say entailment.

| model | context | premise | win | n | keep acc | keep recall | keep precision | false keeps | contra recall | keep acc nb |
|---|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-base | breadcrumb | window | 128 | 350 | 85% | 85% | 93% | 16 | 69% | 86% |
| nli-deberta-v3-base | breadcrumb | window | 400 | 350 | 67% | 60% | 95% | 9 | 64% | 67% |
| nli-deberta-v3-base | breadcrumb | local | 128 | 350 | 89% | 92% | 93% | 19 | 69% | 90% |
| nli-deberta-v3-base | breadcrumb | local | 400 | 350 | 89% | 92% | 93% | 19 | 69% | 90% |
| nli-deberta-v3-base | breadcrumb | both | 128 | 350 | 82% | 81% | 93% | 15 | 69% | 83% |
| nli-deberta-v3-base | breadcrumb | both | 400 | 350 | 65% | 56% | 95% | 7 | 69% | 65% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | 350 | 92% | 95% | 94% | 15 | 89% | 94% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | 350 | 90% | 94% | 93% | 18 | 81% | 92% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | 350 | 92% | 95% | 94% | 16 | 86% | 94% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | 350 | 92% | 95% | 94% | 16 | 86% | 94% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | 350 | 90% | 93% | 94% | 15 | 89% | 92% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | 350 | 89% | 92% | 94% | 15 | 86% | 91% |
| hallucination_evaluation_model | breadcrumb | window | 128 | 350 | 88% | 99% | 87% | 40 | n/a | 90% |
| hallucination_evaluation_model | breadcrumb | window | 400 | 350 | 88% | 98% | 87% | 39 | n/a | 89% |
| hallucination_evaluation_model | breadcrumb | local | 128 | 350 | 87% | 98% | 87% | 39 | n/a | 90% |
| hallucination_evaluation_model | breadcrumb | local | 400 | 350 | 87% | 98% | 87% | 39 | n/a | 90% |
| hallucination_evaluation_model | breadcrumb | both | 128 | 350 | 88% | 98% | 88% | 36 | n/a | 90% |
| hallucination_evaluation_model | breadcrumb | both | 400 | 350 | 89% | 97% | 89% | 32 | n/a | 90% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | 350 | 95% | 98% | 94% | 15 | 92% | 96% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | 350 | 93% | 100% | 92% | 22 | 81% | 95% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | 350 | 95% | 98% | 95% | 13 | 89% | 96% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | 350 | 95% | 98% | 95% | 13 | 89% | 96% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | 350 | 95% | 98% | 96% | 12 | 92% | 96% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | 350 | 95% | 97% | 96% | 11 | 92% | 96% |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | 350 | 88% | 92% | 92% | 20 | n/a | 90% |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | 350 | 90% | 98% | 90% | 29 | n/a | 92% |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | 350 | 89% | 90% | 94% | 14 | n/a | 90% |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | 350 | 89% | 90% | 94% | 14 | n/a | 90% |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | 350 | 87% | 88% | 95% | 13 | n/a | 89% |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | 350 | 88% | 89% | 94% | 14 | n/a | 89% |

## Should-drop claims kept, by source (argmax)

Claims whose gold label is not entailment, split by where they come from. Cell = kept / total (lower is better). `cross` = a claim scored against a related section's prose (gold neutral by default, not part of the metrics above; some may truly be entailed, review the list at the end).

| model | context | premise | win | real | negative | outside | beyond | cross |
|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-base | breadcrumb | window | 128 | 1/2 | 7/43 | 2/23 | 6/21 | 7/259 |
| nli-deberta-v3-base | breadcrumb | window | 400 | 1/2 | 3/43 | 1/23 | 4/21 | 4/259 |
| nli-deberta-v3-base | breadcrumb | local | 128 | 1/2 | 7/43 | 4/23 | 7/21 | 9/259 |
| nli-deberta-v3-base | breadcrumb | local | 400 | 1/2 | 7/43 | 4/23 | 7/21 | 9/259 |
| nli-deberta-v3-base | breadcrumb | both | 128 | 1/2 | 6/43 | 2/23 | 6/21 | 3/259 |
| nli-deberta-v3-base | breadcrumb | both | 400 | 1/2 | 1/43 | 1/23 | 4/21 | 1/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | 1/2 | 3/43 | 5/23 | 6/21 | 49/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | 1/2 | 5/43 | 6/23 | 6/21 | 48/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | 1/2 | 4/43 | 5/23 | 6/21 | 42/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | 1/2 | 4/43 | 5/23 | 6/21 | 42/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | 1/2 | 3/43 | 5/23 | 6/21 | 36/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | 1/2 | 3/43 | 5/23 | 6/21 | 33/259 |
| hallucination_evaluation_model | breadcrumb | window | 128 | 1/2 | 21/43 | 8/23 | 10/21 | 16/259 |
| hallucination_evaluation_model | breadcrumb | window | 400 | 1/2 | 23/43 | 4/23 | 11/21 | 26/259 |
| hallucination_evaluation_model | breadcrumb | local | 128 | 1/2 | 21/43 | 6/23 | 11/21 | 26/259 |
| hallucination_evaluation_model | breadcrumb | local | 400 | 1/2 | 21/43 | 6/23 | 11/21 | 26/259 |
| hallucination_evaluation_model | breadcrumb | both | 128 | 1/2 | 19/43 | 6/23 | 10/21 | 15/259 |
| hallucination_evaluation_model | breadcrumb | both | 400 | 1/2 | 19/43 | 2/23 | 10/21 | 22/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | 1/2 | 4/43 | 5/23 | 5/21 | 27/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | 1/2 | 7/43 | 8/23 | 6/21 | 40/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | 0/2 | 4/43 | 4/23 | 5/21 | 27/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | 0/2 | 4/43 | 4/23 | 5/21 | 27/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | 0/2 | 3/43 | 4/23 | 5/21 | 24/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | 0/2 | 3/43 | 3/23 | 5/21 | 25/259 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | 1/2 | 10/43 | 2/23 | 7/21 | 4/259 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | 1/2 | 14/43 | 5/23 | 9/21 | 17/259 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | 1/2 | 6/43 | 1/23 | 6/21 | 5/259 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | 1/2 | 6/43 | 1/23 | 6/21 | 5/259 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | 1/2 | 6/43 | 1/23 | 5/21 | 3/259 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | 1/2 | 6/43 | 1/23 | 6/21 | 5/259 |

## Threshold sweep

Keep if p_entailment >= threshold (argmax = keep if entailment is the top label). Cell = keep recall / false keeps.

| model | context | premise | win | argmax | >= 0.3 | >= 0.5 | >= 0.7 | >= 0.9 |
|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-base | breadcrumb | window | 128 | 85% / 16 | 86% / 17 | 85% / 16 | 84% / 13 | 83% / 11 |
| nli-deberta-v3-base | breadcrumb | window | 400 | 60% / 9 | 61% / 9 | 60% / 9 | 56% / 7 | 52% / 6 |
| nli-deberta-v3-base | breadcrumb | local | 128 | 92% / 19 | 92% / 20 | 92% / 19 | 91% / 17 | 90% / 15 |
| nli-deberta-v3-base | breadcrumb | local | 400 | 92% / 19 | 92% / 20 | 92% / 19 | 91% / 17 | 90% / 15 |
| nli-deberta-v3-base | breadcrumb | both | 128 | 81% / 15 | 82% / 16 | 81% / 15 | 80% / 12 | 78% / 10 |
| nli-deberta-v3-base | breadcrumb | both | 400 | 56% / 7 | 57% / 7 | 56% / 7 | 52% / 6 | 48% / 6 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | 95% / 15 | 97% / 15 | 95% / 15 | 94% / 13 | 91% / 12 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | 94% / 18 | 95% / 20 | 93% / 18 | 92% / 16 | 90% / 12 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | 95% / 16 | 96% / 16 | 95% / 15 | 93% / 13 | 88% / 12 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | 95% / 16 | 96% / 16 | 95% / 15 | 93% / 13 | 88% / 12 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | 93% / 15 | 95% / 15 | 93% / 14 | 92% / 12 | 86% / 11 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | 92% / 15 | 93% / 15 | 91% / 14 | 89% / 12 | 83% / 10 |
| hallucination_evaluation_model | breadcrumb | window | 128 | 99% / 40 | 100% / 46 | 99% / 40 | 97% / 26 | 76% / 12 |
| hallucination_evaluation_model | breadcrumb | window | 400 | 98% / 39 | 99% / 48 | 98% / 39 | 93% / 30 | 74% / 15 |
| hallucination_evaluation_model | breadcrumb | local | 128 | 98% / 39 | 100% / 50 | 98% / 39 | 96% / 30 | 80% / 16 |
| hallucination_evaluation_model | breadcrumb | local | 400 | 98% / 39 | 100% / 50 | 98% / 39 | 96% / 30 | 80% / 16 |
| hallucination_evaluation_model | breadcrumb | both | 128 | 98% / 36 | 100% / 45 | 98% / 36 | 94% / 25 | 72% / 11 |
| hallucination_evaluation_model | breadcrumb | both | 400 | 97% / 32 | 99% / 43 | 97% / 32 | 91% / 26 | 66% / 11 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | 98% / 15 | 99% / 16 | 98% / 15 | 98% / 15 | 98% / 12 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | 100% / 22 | 100% / 24 | 100% / 22 | 99% / 18 | 99% / 15 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | 98% / 13 | 98% / 14 | 98% / 13 | 97% / 13 | 95% / 12 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | 98% / 13 | 98% / 14 | 98% / 13 | 97% / 13 | 95% / 12 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | 98% / 12 | 98% / 13 | 98% / 12 | 97% / 12 | 95% / 10 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | 97% / 11 | 98% / 13 | 97% / 11 | 96% / 11 | 95% / 10 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | 92% / 20 | 95% / 26 | 92% / 20 | 90% / 13 | 76% / 4 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | 98% / 29 | 100% / 34 | 98% / 29 | 93% / 22 | 79% / 16 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | 90% / 14 | 93% / 19 | 90% / 14 | 84% / 13 | 63% / 5 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | 90% / 14 | 93% / 19 | 90% / 14 | 84% / 13 | 63% / 5 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | 88% / 13 | 91% / 18 | 88% / 13 | 82% / 11 | 60% / 3 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | 89% / 14 | 93% / 19 | 89% / 14 | 83% / 12 | 61% / 4 |

## Labels per extractor

| model | context | premise | win | section | extractor | ent | neu | con | dropped |
|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 31 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 0 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 3 | 6 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 2 | 12 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | 2 | 1 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium | 15 | 0 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 30 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 35 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | 9 | 5 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 7 | 2 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 2 | 2 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 12 | 1 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | opus-high | 12 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | sonnet-medium-outside | 0 | 1 | 3 | 2 |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 11 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 11 | 12 | 10 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 0 | 1 | 6 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 22 | 11 | 7 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 0 | 6 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 0 | 6 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 0 | 9 | 7 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | 6 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 0 | 5 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 2 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | 8 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | 0 | 3 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 30 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 36 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | 6 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | 11 | 3 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 12 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 16 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 14 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 3 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 2 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 4 | 10 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | opus-high | 11 | 6 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | sonnet-medium-outside | 0 | 1 | 3 | 2 |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 11 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 2 | 6 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 2 | 11 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | 2 | 1 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | 13 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 30 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 1 | 37 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 13 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 9 | 1 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 2 | 2 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 12 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 6 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 1 | 2 | 6 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 6 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | flash-3.6-high | 5 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | 3 | 2 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 10 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 1 | 9 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 2 | 6 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 2 | 11 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | 2 | 1 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | 13 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 30 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 1 | 37 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 13 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 9 | 1 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 2 | 2 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 12 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 6 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 1 | 2 | 6 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 6 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | flash-3.6-high | 5 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | 3 | 2 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 10 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 1 | 9 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 31 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 1 | 6 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 1 | 11 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 1 | 3 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | 2 | 1 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | 12 | 3 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | 0 | 5 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 31 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 38 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | 7 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | 9 | 5 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 13 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 7 | 2 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 2 | 2 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 11 | 2 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 6 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | opus-high | 12 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 6 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | flash-3.6-high | 5 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | 3 | 2 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 10 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 9 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 11 | 12 | 10 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 0 | 2 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 22 | 11 | 7 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 0 | 6 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 0 | 8 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 0 | 12 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | 3 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 0 | 4 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 2 | 3 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | 5 | 11 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | 0 | 4 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 31 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 38 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | 8 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | 6 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | 11 | 3 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 13 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 3 | 7 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 4 | 2 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 2 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 6 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | opus-high | 11 | 6 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 6 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | flash-3.6-high | 5 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | 3 | 2 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 10 | 1 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 9 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 6 | 3 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 10 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium | 15 | 0 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 21 | 11 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 7 | 21 | 12 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 5 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 4 | 9 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 5 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 6 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 4 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 7 | 0 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 10 | 0 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 3 | 1 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 4 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 1 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 1 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 1 | 14 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 13 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 1 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 6 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 11 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 2 | 3 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 30 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 5 | 32 | 3 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 4 | 7 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 6 | 6 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 5 | 7 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 5 | 11 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 4 | 10 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 5 | 0 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 7 | 0 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 1 | 3 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 3 | 2 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 1 | 5 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 1 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 1 | 14 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 13 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 7 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 6 | 9 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | 2 | 1 | 3 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | 15 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 36 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 3 | 9 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 5 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 4 | 13 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 4 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 9 | 0 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 11 | 1 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 3 | 1 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 5 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 2 | 5 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 2 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 1 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 1 | 14 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 12 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 7 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 6 | 9 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | 2 | 1 | 3 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | 15 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 36 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 3 | 9 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 5 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 4 | 13 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 4 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 9 | 0 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 11 | 1 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 3 | 1 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 5 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 2 | 5 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 2 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 1 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 1 | 14 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 12 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 6 | 3 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 10 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | 14 | 1 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 36 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 3 | 9 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 5 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 4 | 13 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 4 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 7 | 0 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 9 | 1 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 3 | 1 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 5 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 1 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 1 | 14 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 12 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 6 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 11 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 2 | 3 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | 15 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 36 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 5 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 3 | 14 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 3 | 12 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 5 | 0 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 6 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 3 | 1 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 5 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 1 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 1 | 14 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 12 | 2 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 4 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 3 | 13 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 1 | 39 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | 4 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 3 | 10 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 16 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 14 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 4 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | negatives-handmade | 2 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 31 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 5 | 6 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | 1 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 1 | 39 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | 6 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 3 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 2 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 3 | 10 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 4 | 13 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 3 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 14 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | negatives-handmade | 2 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 6 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 32 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 38 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 4 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 3 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 2 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 2 | 15 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 14 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 4 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 3 | 6 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 1 | 14 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | negatives-handmade | 1 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 6 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 32 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 38 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 4 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 3 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 2 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 2 | 15 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 14 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 4 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 3 | 6 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 1 | 14 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | negatives-handmade | 1 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 4 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 3 | 13 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 1 | 39 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | 4 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 16 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 14 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 4 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | negatives-handmade | 2 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 31 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 5 | 6 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | 0 | 6 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 1 | 39 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | 4 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 3 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 2 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 2 | 15 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 3 | 3 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 14 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | negatives-handmade | 2 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 3 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 3 | 0 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 7 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 5 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 2 | 29 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 3 | 31 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 16 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | sonnet-medium-outside | 0 | 3 | 1 | 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 2 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 3 | 0 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 9 | 1 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 7 | 8 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 2 | 30 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 7 | 28 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 9 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 3 | 9 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 3 | 9 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 2 | 14 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 12 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 3 | 2 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 1 | 2 | 3 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 14 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 3 | 1 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 1 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | sonnet-medium-outside | 0 | 3 | 1 | 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 3 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 0 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 7 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 5 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | 10 | 0 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | 2 | 1 | 3 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 37 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 3 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 2 | 14 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 3 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 0 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 7 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 5 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | 10 | 0 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | 2 | 1 | 3 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 37 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 3 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 2 | 14 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 3 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 0 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 7 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 5 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | 10 | 0 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 37 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 15 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 3 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 0 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 6 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 5 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | 10 | 0 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 37 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 3 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 15 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 30 | 3 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 3 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 2 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 0 | 16 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium | 15 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | 4 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | 13 | 1 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 13 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | negatives-handmade | 2 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 5 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 4 | 3 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 38 | 2 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 4 | 2 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 4 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 3 | 13 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | 4 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 10 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 3 | 10 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 1 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 16 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 14 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 4 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | negatives-handmade | 2 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 2 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 1 | 15 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | 12 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 5 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 13 | 1 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 1 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 2 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 1 | 15 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | 12 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 5 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 13 | 1 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 1 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 30 | 3 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 2 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 0 | 16 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | 12 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | 4 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | 13 | 1 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 13 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | negatives-handmade | 1 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 31 | 2 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 38 | 2 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 2 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 1 | 15 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | 12 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | 5 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | 13 | 1 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 1 | 5 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | negatives-handmade | 1 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |

## Wrong keep / drop decisions (argmax)

| model | context | premise | win | section | extractor | id | gold | NLI | p_ent | claim |
|---|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.9971 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9907 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9907 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c9 | entailment | neutral | 0.0001 | urllib3 raised `UnrewindableBodyError` instead of `ValueError` when retrying a request whose body had `tell()` but not `seek()`. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c10 | entailment | neutral | 0.0014 | urllib3 decoded percent-encoded SOCKS proxy credentials before authenticating with the proxy server. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c3 | entailment | neutral | 0.0075 | urllib3 fixed usage of `proxy_ssl_context` with `ProxyManager` when `use_forwarding_for_https=True`. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c4 | entailment | neutral | 0.0007 | Passing `ssl_context` instead of `proxy_ssl_context` for HTTPS proxies when `use_forwarding_for_https=True` in urllib3 now emits a `FutureWarning`. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c5 | entailment | neutral | 0.001 | Passing `ssl_context` instead of `proxy_ssl_context` for HTTPS proxies when `use_forwarding_for_https=True` in urllib3 will raise an error in v3.0. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c9 | entailment | neutral | 0.0008 | urllib3 raised `UnrewindableBodyError` instead of `ValueError` when retrying a request whose body had `tell()` but not `seek()`. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c10 | entailment | neutral | 0.0164 | urllib3 decoded percent-encoded SOCKS proxy credentials before authenticating with the proxy server. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c13 | entailment | neutral | 0.0048 | urllib3 fixed `is_ipaddress()` to detect non-standard IPv4 forms accepted by `socket.connect`, such as hex (`0x7f000001`), octal (`0177.0.0.1`), and decimal integers (`2130706433`). |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c14 | entailment | neutral | 0.0487 | Detecting non-standard IPv4 forms in `is_ipaddress()` ensures SSL certificate verification uses the correct mode for these addresses. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c15 | entailment | neutral | 0.0038 | urllib3 fixed `HTTPConnectionPool.urlopen` raising a misleading `FullPoolError` instead of `ValueError` when called with an invalid `timeout` argument on a pool created with `block=True`. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c16 | entailment | neutral | 0.0019 | urllib3 fixed port-zero handling to preserve explicit `:0` values instead of substituting default ports 80 or 443 in URL parsing, pool selection, proxy configuration, `connection_from_url()`, and HTTP/2 request authority. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c17 | entailment | contradiction | 0.0007 | urllib3 fixed a bug where `PoolManager` passed the `assert_hostname` and `assert_fingerprint` parameters to HTTP connection pools. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c18 | entailment | contradiction | 0.0013 | urllib3 fixed `HTTPConnectionPool.urlopen()` and HTTP proxy forwarding to strip URL fragments from absolute request targets before sending requests. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c19 | entailment | contradiction | 0.0073 | urllib3 added safeguards to the proxy tunneling code to prevent potential security issues when handling invalid characters in the proxy host and HTTP headers. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c20 | entailment | contradiction | 0.0036 | The proxy tunneling safeguards change in urllib3 affects users of Python 3.10, Python 3.11, and Python 3.12 when the standard library does not contain the fix. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | contradiction | 0.0209 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c22 | entailment | neutral | 0.0179 | urllib3 fixed `HTTPSConnection.connect()` overriding `ProxyConfig.ssl_context`'s certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c23 | entailment | neutral | 0.0276 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c24 | entailment | neutral | 0.0062 | `HTTPSConnection` continues to use its `ssl_context` as a fallback when an HTTPS proxy forwards an HTTP target. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c25 | entailment | contradiction | 0.0003 | urllib3 fixed URL parsing to more strictly enforce RFC 3986 host syntax, rejecting invalid host input such as raw spaces and control characters, malformed percent-encodings, and percent-encoded control characters in HTTP(S) hosts and IPv6 zone identifiers, including proxy CONNECT tunnel targets. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c26 | entailment | contradiction | 0.0019 | Host normalization in urllib3 now follows RFC 3986 normalization rules for percent-encoded octets by decoding percent-encoded unreserved characters. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c27 | entailment | contradiction | 0.0012 | Host normalization in urllib3 now follows RFC 3986 normalization rules for percent-encoded octets by uppercasing the hexadecimal digits of retained percent-encoded octets. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c28 | entailment | contradiction | 0.0004 | urllib3 fixed an `AttributeError` on Python built with OpenSSL 4+, where `ssl.PROTOCOL_TLSv1` no longer exists. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c29 | entailment | contradiction | 0.0004 | In Python built with OpenSSL 4+, `ssl.PROTOCOL_TLSv1` no longer exists. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9953 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.9874 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9825 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b2 | entailment (borderline) | neutral | 0.243 | urllib3 now resolves LifoQueue from the queue module after ConnectionPool instantiation because gevent monkey-patches queue.LifoQueue. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0031 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c2 | entailment | neutral | 0.2227 | Replacing obsolete folded header lines (obs-fold) with spaces prevents raw CRLF sequences from appearing in header values such as Set-Cookie in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c4 | entailment | neutral | 0.0052 | In urllib3, passing ssl_context instead of proxy_ssl_context to ProxyManager for HTTPS proxies with use_forwarding_for_https=True now emits a FutureWarning. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c5 | entailment | neutral | 0.0538 | In urllib3, passing ssl_context instead of proxy_ssl_context to ProxyManager for HTTPS proxies with use_forwarding_for_https=True will raise an error in v3.0. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c13 | entailment | neutral | 0.0168 | The 64 KiB chunk size used by HTTPResponse.drain_conn() is the same as the default amt when doing HTTPResponse.stream(...). |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c15 | entailment | neutral | 0.01 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include hex such as 0x7f000001. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | neutral | 0.0008 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c17 | entailment | neutral | 0.026 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include decimal integers such as 2130706433. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c18 | entailment | neutral | 0.2452 | Detecting non-standard IPv4 forms in is_ipaddress() ensures SSL certificate verification uses the correct mode for these addresses in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c21 | entailment | neutral | 0.0009 | The port-zero handling fix in urllib3 2.8.0 applies to URL parsing, pool selection, proxy configuration, connection_from_url(), and HTTP/2 request authority. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c25 | entailment | contradiction | 0.0058 | The proxy tunneling safeguards in urllib3 2.8.0 affect users of Python 3.10, Python 3.11, and Python 3.12 when the standard library does not contain the fix. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c26 | entailment | contradiction | 0.1704 | Users on newer Python versions than 3.10, 3.11 and 3.12 should upgrade to Python 3.13.14+ or 3.14.5+ to get the same security fixes as the urllib3 proxy tunneling safeguards. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0009 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c28 | entailment | neutral | 0.0194 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c29 | entailment | neutral | 0.0202 | HTTPSConnection continues to use its ssl_context as a fallback when an HTTPS proxy forwards an HTTP target. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c31 | entailment | contradiction | 0.0024 | urllib3 URL parsing rejects invalid host input such as raw spaces and control characters, malformed percent-encodings, and percent-encoded control characters in HTTP(S) hosts and IPv6 zone identifiers. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c34 | entailment | contradiction | 0.0059 | urllib3 host normalization decodes percent-encoded unreserved characters. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c35 | entailment | contradiction | 0.0006 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c36 | entailment | contradiction | 0.01 | In urllib3 2.8.0, an AttributeError was fixed on Python built with OpenSSL 4+, where ssl.PROTOCOL_TLSv1 no longer exists. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9964 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | c5 | entailment | neutral | 0.0003 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | c6 | entailment | neutral | 0.0026 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | c8 | entailment | neutral | 0.4492 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | c9 | entailment | neutral | 0.0891 | In urllib3, proxy identity checks are configured with `proxy_assert_hostname` or `proxy_assert_fingerprint`. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high | c11 | entailment | neutral | 0.3729 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.6982 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9977 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.987 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | o1 | entailment (borderline) | neutral | 0.0008 | urllib3 provides the proxy_ssl_context parameter for configuring TLS settings used when connecting to an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium | c10 | entailment | contradiction | 0.0095 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop is tracked as GHSA-gh4c-6fx4-qh6g. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | c2 | entailment | neutral | 0.0029 | The security issue in urllib3 where the TLS configuration for HTTPS proxies could be ignored or overridden has High severity. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | c3 | entailment | neutral | 0.0011 | The security issue in urllib3 where the TLS configuration for HTTPS proxies could be ignored or overridden is tracked as GHSA-8988-9cw3-xx77. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | c6 | entailment | neutral | 0.0013 | The security issue in urllib3 where `HTTPResponse.stream()` and `read_chunked()` could buffer a chunk-size line of unbounded length in memory has High severity. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | c7 | entailment | neutral | 0.0004 | The security issue in urllib3 where `HTTPResponse.stream()` and `read_chunked()` could buffer a chunk-size line of unbounded length in memory is tracked as GHSA-vxq7-64xx-v4gw. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | c9 | entailment | neutral | 0.1732 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop has Medium severity. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | c10 | entailment | neutral | 0.0009 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop is tracked as GHSA-gh4c-6fx4-qh6g. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | c11 | entailment | neutral | 0.0003 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| nli-deberta-v3-base | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium | c14 | entailment | neutral | 0.0019 | In urllib3, proxy identity checks should be configured with `proxy_assert_hostname` or `proxy_assert_fingerprint`. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0012 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.4994 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0006 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0374 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0007 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0008 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.0016 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0321 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0994 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0042 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0156 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0239 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8397 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0475 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0661 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0664 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.1975 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0475 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0026 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0008 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.3992 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.0686 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0661 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.131 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.3101 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0016 | HTTPX supports only four types of timeouts. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9981 | The limits argument is used to configure pool timeouts in HTTPX. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0028 | HTTPX supports only four types of timeouts. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9947 | The limits argument is used to configure pool timeouts in HTTPX. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c4 | entailment | neutral | 0.0258 | If HTTPX is unable to connect within the connect timeout time frame, a ConnectTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.0039 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c8 | entailment | contradiction | 0.1201 | If HTTPX is unable to send data within the write timeout time frame, a WriteTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c10 | entailment | neutral | 0.0004 | If HTTPX is unable to acquire a connection within the pool timeout time frame, a PoolTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c3 | entailment | neutral | 0.0073 | The HTTPX connect timeout specifies the maximum amount of time to wait until a socket connection to the requested host is established. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c4 | entailment | neutral | 0.0025 | If HTTPX is unable to connect within the connect timeout time frame, a ConnectTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c5 | entailment | neutral | 0.002 | The HTTPX read timeout specifies the maximum duration to wait for a chunk of data to be received. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | neutral | 0.0019 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c7 | entailment | neutral | 0.0026 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c8 | entailment | neutral | 0.0015 | If HTTPX is unable to send data within the write timeout time frame, a WriteTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c9 | entailment | neutral | 0.0032 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c10 | entailment | neutral | 0.0021 | If HTTPX is unable to acquire a connection within the pool timeout time frame, a PoolTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.7812 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.6231 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n1 | contradiction | entailment | 0.6363 | httpx has three different types of timeouts: connect, read, and write. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n4 | contradiction | entailment | 0.8724 | In httpx, the maximum number of allowable connections in the connection pool is configured by the timeout argument. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | contradiction | 0.0406 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.001 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c3 | entailment | neutral | 0.0073 | The HTTPX connect timeout specifies the maximum amount of time to wait until a socket connection to the requested host is established. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c4 | entailment | neutral | 0.072 | HTTPX raises a `ConnectTimeout` exception if it is unable to connect within the connect timeout. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c5 | entailment | neutral | 0.002 | The HTTPX read timeout specifies the maximum duration to wait for a chunk of data to be received. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c6 | entailment | neutral | 0.0024 | A chunk of the response body is an example of a chunk of data covered by the HTTPX read timeout. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | neutral | 0.0067 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c8 | entailment | neutral | 0.0026 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c9 | entailment | neutral | 0.0027 | A chunk of the request body is an example of a chunk of data covered by the HTTPX write timeout. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c10 | entailment | neutral | 0.0052 | HTTPX raises a `WriteTimeout` exception if it is unable to send data within the write timeout. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c11 | entailment | neutral | 0.0032 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c12 | entailment | neutral | 0.0152 | HTTPX raises a `PoolTimeout` exception if it is unable to acquire a connection within the pool timeout. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0011 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0028 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0025 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0008 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0021 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0059 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0005 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0045 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0015 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0006 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0023 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0036 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0004 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0113 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0097 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0006 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0044 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0125 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0012 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0246 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0013 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0039 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9973 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c3 | entailment | neutral | 0.0072 | The retries parameter of urllib3's request() controls retries. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0007 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0015 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0008 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9971 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5696 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.9927 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.998 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| nli-deberta-v3-base | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.006 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5696 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.9927 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.998 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| nli-deberta-v3-base | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.006 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.9971 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9942 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.9971 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9942 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9952 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9952 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9825 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.6984 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9825 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.6984 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0033 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0033 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9983 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9907 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9983 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9907 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.0013 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.0014 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0008 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.0013 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.0014 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0008 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9908 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9977 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9908 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9977 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o1 | entailment (borderline) | contradiction | 0.0002 | urllib3 provides the proxy_ssl_context parameter for configuring TLS settings used when connecting to an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.7923 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o1 | entailment (borderline) | contradiction | 0.0002 | urllib3 provides the proxy_ssl_context parameter for configuring TLS settings used when connecting to an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.7923 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c4 | entailment | neutral | 0.0047 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c5 | entailment | neutral | 0.0049 | In urllib3 2.8.0, a security issue was fixed where `read_chunked()` could buffer a chunk-size line of unbounded length in memory. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.024 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c4 | entailment | neutral | 0.0047 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c5 | entailment | neutral | 0.0049 | In urllib3 2.8.0, a security issue was fixed where `read_chunked()` could buffer a chunk-size line of unbounded length in memory. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.024 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0209 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0209 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.011 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0169 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.011 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0169 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.7985 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.7985 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0011 | HTTPX supports only four types of timeouts. |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9977 | The limits argument is used to configure pool timeouts in HTTPX. |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0011 | HTTPX supports only four types of timeouts. |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9977 | The limits argument is used to configure pool timeouts in HTTPX. |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.0153 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c10 | entailment | neutral | 0.0001 | If HTTPX is unable to acquire a connection within the pool timeout time frame, a PoolTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.0153 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c10 | entailment | neutral | 0.0001 | If HTTPX is unable to acquire a connection within the pool timeout time frame, a PoolTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.9881 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.9942 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.9881 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.9942 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c1 | entailment | neutral | 0.0002 | HTTPX allows specifying timeout behavior in more fine grained detail. |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0034 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c1 | entailment | neutral | 0.0002 | HTTPX allows specifying timeout behavior in more fine grained detail. |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0034 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0047 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0047 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.9363 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.9363 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.001 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.001 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0016 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9975 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0016 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9975 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5023 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.9927 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9976 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0019 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5023 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.9927 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9976 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0019 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | flash-3.6-high | c2 | entailment | neutral | 0.3939 | Timeouts are measured in seconds. |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | flash-3.6-high | c2 | entailment | neutral | 0.3939 | Timeouts are measured in seconds. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.9971 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9907 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9907 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c9 | entailment | neutral | 0.0001 | urllib3 raised `UnrewindableBodyError` instead of `ValueError` when retrying a request whose body had `tell()` but not `seek()`. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c10 | entailment | neutral | 0.0014 | urllib3 decoded percent-encoded SOCKS proxy credentials before authenticating with the proxy server. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c3 | entailment | neutral | 0.0075 | urllib3 fixed usage of `proxy_ssl_context` with `ProxyManager` when `use_forwarding_for_https=True`. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c4 | entailment | neutral | 0.0007 | Passing `ssl_context` instead of `proxy_ssl_context` for HTTPS proxies when `use_forwarding_for_https=True` in urllib3 now emits a `FutureWarning`. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c5 | entailment | neutral | 0.001 | Passing `ssl_context` instead of `proxy_ssl_context` for HTTPS proxies when `use_forwarding_for_https=True` in urllib3 will raise an error in v3.0. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c9 | entailment | neutral | 0.0008 | urllib3 raised `UnrewindableBodyError` instead of `ValueError` when retrying a request whose body had `tell()` but not `seek()`. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c10 | entailment | neutral | 0.0164 | urllib3 decoded percent-encoded SOCKS proxy credentials before authenticating with the proxy server. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c13 | entailment | neutral | 0.0048 | urllib3 fixed `is_ipaddress()` to detect non-standard IPv4 forms accepted by `socket.connect`, such as hex (`0x7f000001`), octal (`0177.0.0.1`), and decimal integers (`2130706433`). |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c14 | entailment | neutral | 0.0487 | Detecting non-standard IPv4 forms in `is_ipaddress()` ensures SSL certificate verification uses the correct mode for these addresses. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c15 | entailment | neutral | 0.0038 | urllib3 fixed `HTTPConnectionPool.urlopen` raising a misleading `FullPoolError` instead of `ValueError` when called with an invalid `timeout` argument on a pool created with `block=True`. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c16 | entailment | neutral | 0.0019 | urllib3 fixed port-zero handling to preserve explicit `:0` values instead of substituting default ports 80 or 443 in URL parsing, pool selection, proxy configuration, `connection_from_url()`, and HTTP/2 request authority. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c17 | entailment | contradiction | 0.0007 | urllib3 fixed a bug where `PoolManager` passed the `assert_hostname` and `assert_fingerprint` parameters to HTTP connection pools. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c18 | entailment | contradiction | 0.0013 | urllib3 fixed `HTTPConnectionPool.urlopen()` and HTTP proxy forwarding to strip URL fragments from absolute request targets before sending requests. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c19 | entailment | contradiction | 0.0073 | urllib3 added safeguards to the proxy tunneling code to prevent potential security issues when handling invalid characters in the proxy host and HTTP headers. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c20 | entailment | contradiction | 0.0036 | The proxy tunneling safeguards change in urllib3 affects users of Python 3.10, Python 3.11, and Python 3.12 when the standard library does not contain the fix. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | contradiction | 0.0209 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c22 | entailment | neutral | 0.0179 | urllib3 fixed `HTTPSConnection.connect()` overriding `ProxyConfig.ssl_context`'s certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c23 | entailment | neutral | 0.0276 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c24 | entailment | neutral | 0.0062 | `HTTPSConnection` continues to use its `ssl_context` as a fallback when an HTTPS proxy forwards an HTTP target. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c25 | entailment | contradiction | 0.0003 | urllib3 fixed URL parsing to more strictly enforce RFC 3986 host syntax, rejecting invalid host input such as raw spaces and control characters, malformed percent-encodings, and percent-encoded control characters in HTTP(S) hosts and IPv6 zone identifiers, including proxy CONNECT tunnel targets. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c26 | entailment | contradiction | 0.0019 | Host normalization in urllib3 now follows RFC 3986 normalization rules for percent-encoded octets by decoding percent-encoded unreserved characters. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c27 | entailment | contradiction | 0.0012 | Host normalization in urllib3 now follows RFC 3986 normalization rules for percent-encoded octets by uppercasing the hexadecimal digits of retained percent-encoded octets. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c28 | entailment | contradiction | 0.0004 | urllib3 fixed an `AttributeError` on Python built with OpenSSL 4+, where `ssl.PROTOCOL_TLSv1` no longer exists. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c29 | entailment | contradiction | 0.0004 | In Python built with OpenSSL 4+, `ssl.PROTOCOL_TLSv1` no longer exists. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9952 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9825 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b2 | entailment (borderline) | neutral | 0.243 | urllib3 now resolves LifoQueue from the queue module after ConnectionPool instantiation because gevent monkey-patches queue.LifoQueue. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0031 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c2 | entailment | neutral | 0.2227 | Replacing obsolete folded header lines (obs-fold) with spaces prevents raw CRLF sequences from appearing in header values such as Set-Cookie in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c4 | entailment | neutral | 0.0052 | In urllib3, passing ssl_context instead of proxy_ssl_context to ProxyManager for HTTPS proxies with use_forwarding_for_https=True now emits a FutureWarning. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c5 | entailment | neutral | 0.0538 | In urllib3, passing ssl_context instead of proxy_ssl_context to ProxyManager for HTTPS proxies with use_forwarding_for_https=True will raise an error in v3.0. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c13 | entailment | neutral | 0.0168 | The 64 KiB chunk size used by HTTPResponse.drain_conn() is the same as the default amt when doing HTTPResponse.stream(...). |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c15 | entailment | neutral | 0.01 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include hex such as 0x7f000001. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | neutral | 0.0008 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c17 | entailment | neutral | 0.026 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include decimal integers such as 2130706433. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c18 | entailment | neutral | 0.2452 | Detecting non-standard IPv4 forms in is_ipaddress() ensures SSL certificate verification uses the correct mode for these addresses in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c21 | entailment | neutral | 0.0009 | The port-zero handling fix in urllib3 2.8.0 applies to URL parsing, pool selection, proxy configuration, connection_from_url(), and HTTP/2 request authority. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c25 | entailment | contradiction | 0.0058 | The proxy tunneling safeguards in urllib3 2.8.0 affect users of Python 3.10, Python 3.11, and Python 3.12 when the standard library does not contain the fix. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c26 | entailment | contradiction | 0.1704 | Users on newer Python versions than 3.10, 3.11 and 3.12 should upgrade to Python 3.13.14+ or 3.14.5+ to get the same security fixes as the urllib3 proxy tunneling safeguards. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0009 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c28 | entailment | neutral | 0.0194 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c29 | entailment | neutral | 0.0202 | HTTPSConnection continues to use its ssl_context as a fallback when an HTTPS proxy forwards an HTTP target. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c31 | entailment | contradiction | 0.0024 | urllib3 URL parsing rejects invalid host input such as raw spaces and control characters, malformed percent-encodings, and percent-encoded control characters in HTTP(S) hosts and IPv6 zone identifiers. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c34 | entailment | contradiction | 0.0059 | urllib3 host normalization decodes percent-encoded unreserved characters. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c35 | entailment | contradiction | 0.0006 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c36 | entailment | contradiction | 0.01 | In urllib3 2.8.0, an AttributeError was fixed on Python built with OpenSSL 4+, where ssl.PROTOCOL_TLSv1 no longer exists. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9964 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.0013 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.0014 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0008 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.0013 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.0014 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0008 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c5 | entailment | neutral | 0.0003 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c6 | entailment | neutral | 0.0026 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c8 | entailment | neutral | 0.4492 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c9 | entailment | neutral | 0.0891 | In urllib3, proxy identity checks are configured with `proxy_assert_hostname` or `proxy_assert_fingerprint`. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c11 | entailment | neutral | 0.3729 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.6982 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9977 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.987 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | o1 | entailment (borderline) | contradiction | 0.0002 | urllib3 provides the proxy_ssl_context parameter for configuring TLS settings used when connecting to an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | o1 | entailment (borderline) | contradiction | 0.0002 | urllib3 provides the proxy_ssl_context parameter for configuring TLS settings used when connecting to an HTTPS proxy. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c4 | entailment | neutral | 0.0047 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c5 | entailment | neutral | 0.0049 | In urllib3 2.8.0, a security issue was fixed where `read_chunked()` could buffer a chunk-size line of unbounded length in memory. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.024 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c10 | entailment | contradiction | 0.0095 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop is tracked as GHSA-gh4c-6fx4-qh6g. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c2 | entailment | neutral | 0.0029 | The security issue in urllib3 where the TLS configuration for HTTPS proxies could be ignored or overridden has High severity. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c3 | entailment | neutral | 0.0011 | The security issue in urllib3 where the TLS configuration for HTTPS proxies could be ignored or overridden is tracked as GHSA-8988-9cw3-xx77. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c4 | entailment | neutral | 0.0047 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c5 | entailment | neutral | 0.0049 | In urllib3 2.8.0, a security issue was fixed where `read_chunked()` could buffer a chunk-size line of unbounded length in memory. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c6 | entailment | neutral | 0.0013 | The security issue in urllib3 where `HTTPResponse.stream()` and `read_chunked()` could buffer a chunk-size line of unbounded length in memory has High severity. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c7 | entailment | neutral | 0.0004 | The security issue in urllib3 where `HTTPResponse.stream()` and `read_chunked()` could buffer a chunk-size line of unbounded length in memory is tracked as GHSA-vxq7-64xx-v4gw. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.024 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c9 | entailment | neutral | 0.1732 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop has Medium severity. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c10 | entailment | neutral | 0.0009 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop is tracked as GHSA-gh4c-6fx4-qh6g. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c11 | entailment | neutral | 0.0003 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| nli-deberta-v3-base | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c14 | entailment | neutral | 0.0019 | In urllib3, proxy identity checks should be configured with `proxy_assert_hostname` or `proxy_assert_fingerprint`. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0012 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.4994 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0006 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0209 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0007 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0008 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.0016 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0321 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.011 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0169 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0994 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0042 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0156 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.011 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0169 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0239 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.7985 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0475 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0661 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0664 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.1975 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0475 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0026 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0008 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.3992 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.0686 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0661 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.131 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.3101 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0011 | HTTPX supports only four types of timeouts. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9977 | The limits argument is used to configure pool timeouts in HTTPX. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0011 | HTTPX supports only four types of timeouts. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9947 | The limits argument is used to configure pool timeouts in HTTPX. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c4 | entailment | neutral | 0.0258 | If HTTPX is unable to connect within the connect timeout time frame, a ConnectTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.0039 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c8 | entailment | contradiction | 0.1201 | If HTTPX is unable to send data within the write timeout time frame, a WriteTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c10 | entailment | neutral | 0.0001 | If HTTPX is unable to acquire a connection within the pool timeout time frame, a PoolTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c3 | entailment | neutral | 0.0073 | The HTTPX connect timeout specifies the maximum amount of time to wait until a socket connection to the requested host is established. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c4 | entailment | neutral | 0.0025 | If HTTPX is unable to connect within the connect timeout time frame, a ConnectTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c5 | entailment | neutral | 0.002 | The HTTPX read timeout specifies the maximum duration to wait for a chunk of data to be received. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.0019 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c7 | entailment | neutral | 0.0026 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c8 | entailment | neutral | 0.0015 | If HTTPX is unable to send data within the write timeout time frame, a WriteTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c9 | entailment | neutral | 0.0032 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c10 | entailment | neutral | 0.0001 | If HTTPX is unable to acquire a connection within the pool timeout time frame, a PoolTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.7812 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.6231 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c1 | entailment | neutral | 0.0002 | HTTPX allows specifying timeout behavior in more fine grained detail. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | contradiction | 0.0406 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.001 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c1 | entailment | neutral | 0.0002 | HTTPX allows specifying timeout behavior in more fine grained detail. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c3 | entailment | neutral | 0.0073 | The HTTPX connect timeout specifies the maximum amount of time to wait until a socket connection to the requested host is established. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c4 | entailment | neutral | 0.072 | HTTPX raises a `ConnectTimeout` exception if it is unable to connect within the connect timeout. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c5 | entailment | neutral | 0.002 | The HTTPX read timeout specifies the maximum duration to wait for a chunk of data to be received. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c6 | entailment | neutral | 0.0024 | A chunk of the response body is an example of a chunk of data covered by the HTTPX read timeout. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | neutral | 0.0067 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c8 | entailment | neutral | 0.0026 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c9 | entailment | neutral | 0.0027 | A chunk of the request body is an example of a chunk of data covered by the HTTPX write timeout. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c10 | entailment | neutral | 0.0052 | HTTPX raises a `WriteTimeout` exception if it is unable to send data within the write timeout. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c11 | entailment | neutral | 0.0032 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c12 | entailment | neutral | 0.0152 | HTTPX raises a `PoolTimeout` exception if it is unable to acquire a connection within the pool timeout. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0034 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0011 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0028 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0025 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0008 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0021 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0059 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0005 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0045 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0015 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0006 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0023 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0036 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0004 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0113 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0097 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0006 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0044 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0125 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0012 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0246 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0013 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0039 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9973 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c3 | entailment | neutral | 0.0072 | The retries parameter of urllib3's request() controls retries. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0007 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0015 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0008 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9971 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5023 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.9927 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9976 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0019 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5023 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.9927 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9976 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0019 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| nli-deberta-v3-base | breadcrumb | both | 128 | using-timeouts | flash-3.6-high | c2 | entailment | neutral | 0.3939 | Timeouts are measured in seconds. |
| nli-deberta-v3-base | breadcrumb | both | 400 | using-timeouts | flash-3.6-high | c2 | entailment | neutral | 0.3939 | Timeouts are measured in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.924 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9318 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.8762 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9318 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9875 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9932 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n5 | contradiction | entailment | 0.6 | urllib3 2.8.0 raises ValueError instead of UnrewindableBodyError when retrying a request whose body has tell() but not seek(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9736 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9644 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.8852 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0053 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0473 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9941 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9697 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9904 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9608 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9942 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9882 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.5009 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.9231 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.847 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.9702 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium | c10 | entailment | contradiction | 0.3343 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop is tracked as GHSA-gh4c-6fx4-qh6g. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.4451 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8055 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.9405 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.01 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9969 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.013 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9644 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.0066 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c7 | entailment | contradiction | 0.2985 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c8 | entailment | contradiction | 0.0952 | If HTTPX is unable to send data within the write timeout time frame, a WriteTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c9 | entailment | contradiction | 0.4275 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c4 | entailment | contradiction | 0.2862 | If HTTPX is unable to connect within the connect timeout time frame, a ConnectTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c5 | entailment | contradiction | 0.4012 | The HTTPX read timeout specifies the maximum duration to wait for a chunk of data to be received. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.0562 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c7 | entailment | contradiction | 0.1118 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c8 | entailment | contradiction | 0.0471 | If HTTPX is unable to send data within the write timeout time frame, a WriteTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c9 | entailment | contradiction | 0.1847 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.6075 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.5 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | contradiction | 0.0092 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c8 | entailment | contradiction | 0.2985 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c10 | entailment | contradiction | 0.0349 | HTTPX raises a `WriteTimeout` exception if it is unable to send data within the write timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c11 | entailment | contradiction | 0.4275 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c4 | entailment | contradiction | 0.1095 | HTTPX raises a `ConnectTimeout` exception if it is unable to connect within the connect timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c5 | entailment | contradiction | 0.4012 | The HTTPX read timeout specifies the maximum duration to wait for a chunk of data to be received. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | contradiction | 0.0314 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c8 | entailment | contradiction | 0.1118 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c10 | entailment | contradiction | 0.0452 | HTTPX raises a `WriteTimeout` exception if it is unable to send data within the write timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c11 | entailment | contradiction | 0.1847 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c12 | entailment | contradiction | 0.2743 | HTTPX raises a `PoolTimeout` exception if it is unable to acquire a connection within the pool timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.7512 | Specifying redirect=False disables the retrying logic of urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9776 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9917 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9759 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9906 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0627 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9759 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9906 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0627 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.924 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9502 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.924 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9502 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9837 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9837 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9736 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9736 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0208 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0208 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9944 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9764 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9944 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9764 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.437 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.3881 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.195 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.437 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.3881 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.195 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9354 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9935 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9354 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9935 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.481 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.6532 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.481 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.6532 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.1903 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.1903 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.4268 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.4268 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8964 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8964 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0269 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9947 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0269 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9947 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.115 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c7 | entailment | contradiction | 0.1123 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.115 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c7 | entailment | contradiction | 0.1123 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.6405 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.6405 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | contradiction | 0.2546 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c8 | entailment | contradiction | 0.1123 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0379 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | contradiction | 0.2546 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c8 | entailment | contradiction | 0.1123 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0379 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9906 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9906 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9867 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9852 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0139 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9867 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9852 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0139 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.924 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9318 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.8762 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9318 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9837 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9837 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9736 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9644 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0053 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0208 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9941 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9697 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9904 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9608 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.437 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.3881 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.195 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.437 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.3881 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.195 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9935 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9882 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.481 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.6532 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.481 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.6532 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.1903 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c10 | entailment | contradiction | 0.3343 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop is tracked as GHSA-gh4c-6fx4-qh6g. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.1903 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.4268 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.4451 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.4268 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8055 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8964 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.01 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9947 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.013 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9644 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.0066 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c7 | entailment | contradiction | 0.1123 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c8 | entailment | contradiction | 0.0952 | If HTTPX is unable to send data within the write timeout time frame, a WriteTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c9 | entailment | contradiction | 0.4275 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c4 | entailment | contradiction | 0.2862 | If HTTPX is unable to connect within the connect timeout time frame, a ConnectTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c5 | entailment | contradiction | 0.4012 | The HTTPX read timeout specifies the maximum duration to wait for a chunk of data to be received. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | contradiction | 0.0562 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c7 | entailment | contradiction | 0.1118 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c8 | entailment | contradiction | 0.0471 | If HTTPX is unable to send data within the write timeout time frame, a WriteTimeout exception is raised. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c9 | entailment | contradiction | 0.1847 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.6075 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.5 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | contradiction | 0.0092 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c8 | entailment | contradiction | 0.1123 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c10 | entailment | contradiction | 0.0349 | HTTPX raises a `WriteTimeout` exception if it is unable to send data within the write timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c11 | entailment | contradiction | 0.4275 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0379 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c4 | entailment | contradiction | 0.1095 | HTTPX raises a `ConnectTimeout` exception if it is unable to connect within the connect timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c5 | entailment | contradiction | 0.4012 | The HTTPX read timeout specifies the maximum duration to wait for a chunk of data to be received. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c7 | entailment | contradiction | 0.0314 | HTTPX raises a `ReadTimeout` exception if it is unable to receive data within the read timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c8 | entailment | contradiction | 0.1118 | The HTTPX write timeout specifies the maximum duration to wait for a chunk of data to be sent. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c10 | entailment | contradiction | 0.0452 | HTTPX raises a `WriteTimeout` exception if it is unable to send data within the write timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c11 | entailment | contradiction | 0.1847 | The HTTPX pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c12 | entailment | contradiction | 0.2743 | HTTPX raises a `PoolTimeout` exception if it is unable to acquire a connection within the pool timeout. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0379 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9776 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9906 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9759 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9852 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0139 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9759 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9852 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | contradiction | 0.0139 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o3 | neutral | entailment | 0.5256 | UnrewindableBodyError is an exception class defined in the urllib3.exceptions module. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.951 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.5946 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9828 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o3 | neutral | entailment | 0.5643 | UnrewindableBodyError is an exception class defined in the urllib3.exceptions module. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.7421 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.8868 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9828 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c33 | entailment | neutral | 0.3708 | urllib3 fixed `assert_fingerprint()` to raise `SSLError` instead of `binascii.Error` when a fingerprint has a supported length but contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c12 | entailment | neutral | 0.3417 | The default `amt` when calling `HTTPResponse.stream(...)` in urllib3 is 64 KiB. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c33 | entailment | neutral | 0.3708 | urllib3 fixed `assert_fingerprint()` to raise `SSLError` instead of `binascii.Error` when a fingerprint has a supported length but contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n1 | contradiction | entailment | 0.7402 | urllib3 2.8.0 changed HTTPResponse.drain_conn() to discard unread response data in 32 KiB chunks. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9334 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n3 | contradiction | entailment | 0.851 | urllib3 2.8.0 substitutes the default ports 80 or 443 for an explicit :0 port in URL parsing. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.8142 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n5 | contradiction | entailment | 0.6538 | urllib3 2.8.0 raises ValueError instead of UnrewindableBodyError when retrying a request whose body has tell() but not seek(). |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.8596 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.9327 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n1 | contradiction | entailment | 0.6205 | urllib3 2.8.0 changed HTTPResponse.drain_conn() to discard unread response data in 32 KiB chunks. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9412 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n3 | contradiction | entailment | 0.7323 | urllib3 2.8.0 substitutes the default ports 80 or 443 for an explicit :0 port in URL parsing. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.9121 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n5 | contradiction | entailment | 0.9552 | urllib3 2.8.0 raises ValueError instead of UnrewindableBodyError when retrying a request whose body has tell() but not seek(). |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.8596 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.9327 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.5663 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.5939 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.6194 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b1 | neutral | entailment | 0.6238 | urllib3 always emits a FutureWarning whenever ssl_context is passed to a ProxyManager instead of proxy_ssl_context. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b3 | neutral | entailment | 0.6445 | urllib3 fixed the SOCKS proxy credential bug so that percent-encoded passwords no longer cause authentication failures with the proxy server. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.6328 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9723 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9414 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.5603 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9515 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9023 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.7237 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n2 | contradiction | entailment | 0.7997 | In urllib3 2.8.0, destination client certificates still apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9665 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n6 | contradiction (borderline) | entailment | 0.6111 | urllib3 2.7.0 fixed the ignored TLS configuration for HTTPS proxies. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.8341 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | n2 | contradiction | entailment | 0.7822 | In urllib3 2.8.0, destination client certificates still apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9415 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | n6 | contradiction (borderline) | entailment | 0.6351 | urllib3 2.7.0 fixed the ignored TLS configuration for HTTPS proxies. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.6252 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | b1 | neutral | entailment | 0.649 | urllib3 2.8.0 requires all users with HTTPS proxies to change their configurations. |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n3 | contradiction | entailment | 0.7588 | Retry ignores delays requested by the server in a Retry-After header. |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.9563 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.961 | With exponential backoff, Retry waits before the second attempt. |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.8896 | Retrying immediately without backoff is recommended for production systems. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n1 | contradiction | entailment | 0.5929 | By default, Retry sleeps one second between retry attempts. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n2 | contradiction | entailment | 0.7691 | The default backoff_factor of Retry is 0.5. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n3 | contradiction | entailment | 0.8393 | Retry ignores delays requested by the server in a Retry-After header. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8985 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9348 | With exponential backoff, Retry waits before the second attempt. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.9444 | Retrying immediately without backoff is recommended for production systems. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.1667 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | o1 | neutral | entailment | 0.7412 | An httpx.Timeout instance can be passed to the timeout parameter of httpx.Client. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.2218 | HTTPX supports only four types of timeouts. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b2 | contradiction (borderline) | entailment | 0.6241 | The HTTPX read timeout specifies the maximum duration to wait for an entire response body to be received. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9657 | The limits argument is used to configure pool timeouts in HTTPX. |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.2341 | HTTPX supports only four types of timeouts. |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b2 | contradiction (borderline) | entailment | 0.8251 | The HTTPX read timeout specifies the maximum duration to wait for an entire response body to be received. |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9055 | The limits argument is used to configure pool timeouts in HTTPX. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n1 | contradiction | entailment | 0.5772 | httpx has three different types of timeouts: connect, read, and write. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.8387 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.5881 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n4 | contradiction | entailment | 0.9617 | In httpx, the maximum number of allowable connections in the connection pool is configured by the timeout argument. |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n1 | contradiction | entailment | 0.8207 | httpx has three different types of timeouts: connect, read, and write. |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.967 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.8932 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n4 | contradiction | entailment | 0.9468 | In httpx, the maximum number of allowable connections in the connection pool is configured by the timeout argument. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.5422 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.785 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.8574 | Specifying redirect=False disables the retrying logic of urllib3. |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.834 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.9209 | Specifying redirect=False disables the retrying logic of urllib3. |
| hallucination_evaluation_model | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9283 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| hallucination_evaluation_model | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9777 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.7308 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.8999 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| hallucination_evaluation_model | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.5901 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.7308 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.8999 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| hallucination_evaluation_model | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.5901 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.951 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.8534 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9727 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.951 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.8534 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9727 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n1 | contradiction | entailment | 0.7402 | urllib3 2.8.0 changed HTTPResponse.drain_conn() to discard unread response data in 32 KiB chunks. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9479 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n3 | contradiction | entailment | 0.8308 | urllib3 2.8.0 substitutes the default ports 80 or 443 for an explicit :0 port in URL parsing. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.8526 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n5 | contradiction | entailment | 0.6863 | urllib3 2.8.0 raises ValueError instead of UnrewindableBodyError when retrying a request whose body has tell() but not seek(). |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.6621 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.8653 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n1 | contradiction | entailment | 0.7402 | urllib3 2.8.0 changed HTTPResponse.drain_conn() to discard unread response data in 32 KiB chunks. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9479 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n3 | contradiction | entailment | 0.8308 | urllib3 2.8.0 substitutes the default ports 80 or 443 for an explicit :0 port in URL parsing. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.8526 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n5 | contradiction | entailment | 0.6863 | urllib3 2.8.0 raises ValueError instead of UnrewindableBodyError when retrying a request whose body has tell() but not seek(). |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.6621 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.8653 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.5663 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.7089 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b3 | neutral | entailment | 0.7774 | urllib3 fixed the SOCKS proxy credential bug so that percent-encoded passwords no longer cause authentication failures with the proxy server. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.5663 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.7089 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b3 | neutral | entailment | 0.7774 | urllib3 fixed the SOCKS proxy credential bug so that percent-encoded passwords no longer cause authentication failures with the proxy server. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9659 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9532 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9659 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9532 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.3516 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.3481 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.3468 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.3516 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.3481 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.3468 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9089 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n2 | contradiction | entailment | 0.7827 | In urllib3 2.8.0, destination client certificates still apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9657 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9089 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n2 | contradiction | entailment | 0.7827 | In urllib3 2.8.0, destination client certificates still apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9657 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o1 | entailment (borderline) | neutral | 0.4333 | urllib3 provides the proxy_ssl_context parameter for configuring TLS settings used when connecting to an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.5062 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | b1 | neutral | entailment | 0.6583 | urllib3 2.8.0 requires all users with HTTPS proxies to change their configurations. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o1 | entailment (borderline) | neutral | 0.4333 | urllib3 provides the proxy_ssl_context parameter for configuring TLS settings used when connecting to an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.5062 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | b1 | neutral | entailment | 0.6583 | urllib3 2.8.0 requires all users with HTTPS proxies to change their configurations. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n3 | contradiction | entailment | 0.908 | Retry ignores delays requested by the server in a Retry-After header. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.9605 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9278 | With exponential backoff, Retry waits before the second attempt. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.8987 | Retrying immediately without backoff is recommended for production systems. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n3 | contradiction | entailment | 0.908 | Retry ignores delays requested by the server in a Retry-After header. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.9605 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9278 | With exponential backoff, Retry waits before the second attempt. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.8987 | Retrying immediately without backoff is recommended for production systems. |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | o1 | neutral | entailment | 0.7897 | An httpx.Timeout instance can be passed to the timeout parameter of httpx.Client. |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.137 | HTTPX supports only four types of timeouts. |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b2 | contradiction (borderline) | entailment | 0.8295 | The HTTPX read timeout specifies the maximum duration to wait for an entire response body to be received. |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9736 | The limits argument is used to configure pool timeouts in HTTPX. |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | o1 | neutral | entailment | 0.7897 | An httpx.Timeout instance can be passed to the timeout parameter of httpx.Client. |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.137 | HTTPX supports only four types of timeouts. |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b2 | contradiction (borderline) | entailment | 0.8295 | The HTTPX read timeout specifies the maximum duration to wait for an entire response body to be received. |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9736 | The limits argument is used to configure pool timeouts in HTTPX. |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.9369 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.962 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n4 | contradiction | entailment | 0.962 | In httpx, the maximum number of allowable connections in the connection pool is configured by the timeout argument. |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.9369 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.962 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n4 | contradiction | entailment | 0.962 | In httpx, the maximum number of allowable connections in the connection pool is configured by the timeout argument. |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.6166 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.6166 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.7388 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.9275 | Specifying redirect=False disables the retrying logic of urllib3. |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | negatives-handmade | n7 | contradiction | entailment | 0.6195 | A retry policy set at the PoolManager level cannot be overridden per request. |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.7388 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.9275 | Specifying redirect=False disables the retrying logic of urllib3. |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | negatives-handmade | n7 | contradiction | entailment | 0.6195 | A retry policy set at the PoolManager level cannot be overridden per request. |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9219 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9219 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.8238 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.853 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.6768 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.8238 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.853 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.6768 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| hallucination_evaluation_model | breadcrumb | local | 128 | using-timeouts | negatives-handmade | n3 | contradiction | entailment | 0.5291 | A timeout set at the urllib3 PoolManager level cannot be overridden for an individual request. |
| hallucination_evaluation_model | breadcrumb | local | 400 | using-timeouts | negatives-handmade | n3 | contradiction | entailment | 0.5291 | A timeout set at the urllib3 PoolManager level cannot be overridden for an individual request. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.951 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.5946 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9727 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.7421 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.8534 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9727 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c33 | entailment | neutral | 0.3708 | urllib3 fixed `assert_fingerprint()` to raise `SSLError` instead of `binascii.Error` when a fingerprint has a supported length but contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c12 | entailment | neutral | 0.3417 | The default `amt` when calling `HTTPResponse.stream(...)` in urllib3 is 64 KiB. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c33 | entailment | neutral | 0.3708 | urllib3 fixed `assert_fingerprint()` to raise `SSLError` instead of `binascii.Error` when a fingerprint has a supported length but contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n1 | contradiction | entailment | 0.7402 | urllib3 2.8.0 changed HTTPResponse.drain_conn() to discard unread response data in 32 KiB chunks. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9334 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n3 | contradiction | entailment | 0.8308 | urllib3 2.8.0 substitutes the default ports 80 or 443 for an explicit :0 port in URL parsing. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.8142 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n5 | contradiction | entailment | 0.6538 | urllib3 2.8.0 raises ValueError instead of UnrewindableBodyError when retrying a request whose body has tell() but not seek(). |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.6621 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.8653 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n1 | contradiction | entailment | 0.6205 | urllib3 2.8.0 changed HTTPResponse.drain_conn() to discard unread response data in 32 KiB chunks. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9412 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n3 | contradiction | entailment | 0.7323 | urllib3 2.8.0 substitutes the default ports 80 or 443 for an explicit :0 port in URL parsing. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.8526 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n5 | contradiction | entailment | 0.6863 | urllib3 2.8.0 raises ValueError instead of UnrewindableBodyError when retrying a request whose body has tell() but not seek(). |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.6621 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.8653 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.5663 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.5939 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.6194 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b3 | neutral | entailment | 0.6445 | urllib3 fixed the SOCKS proxy credential bug so that percent-encoded passwords no longer cause authentication failures with the proxy server. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9659 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9414 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9515 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9023 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.3516 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.3481 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.3468 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.3516 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.3481 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.3468 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.7237 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | n2 | contradiction | entailment | 0.7827 | In urllib3 2.8.0, destination client certificates still apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9657 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.8341 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | n2 | contradiction | entailment | 0.7822 | In urllib3 2.8.0, destination client certificates still apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9415 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | o1 | entailment (borderline) | neutral | 0.4333 | urllib3 provides the proxy_ssl_context parameter for configuring TLS settings used when connecting to an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.5062 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | b1 | neutral | entailment | 0.649 | urllib3 2.8.0 requires all users with HTTPS proxies to change their configurations. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | o1 | entailment (borderline) | neutral | 0.4333 | urllib3 provides the proxy_ssl_context parameter for configuring TLS settings used when connecting to an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n3 | contradiction | entailment | 0.7588 | Retry ignores delays requested by the server in a Retry-After header. |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.9563 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9278 | With exponential backoff, Retry waits before the second attempt. |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.8896 | Retrying immediately without backoff is recommended for production systems. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | n3 | contradiction | entailment | 0.8393 | Retry ignores delays requested by the server in a Retry-After header. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8985 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9278 | With exponential backoff, Retry waits before the second attempt. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.8987 | Retrying immediately without backoff is recommended for production systems. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.1667 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | o1 | neutral | entailment | 0.7412 | An httpx.Timeout instance can be passed to the timeout parameter of httpx.Client. |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.137 | HTTPX supports only four types of timeouts. |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b2 | contradiction (borderline) | entailment | 0.6241 | The HTTPX read timeout specifies the maximum duration to wait for an entire response body to be received. |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9657 | The limits argument is used to configure pool timeouts in HTTPX. |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.137 | HTTPX supports only four types of timeouts. |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b2 | contradiction (borderline) | entailment | 0.8251 | The HTTPX read timeout specifies the maximum duration to wait for an entire response body to be received. |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9055 | The limits argument is used to configure pool timeouts in HTTPX. |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.8387 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.5881 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n4 | contradiction | entailment | 0.9617 | In httpx, the maximum number of allowable connections in the connection pool is configured by the timeout argument. |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.9369 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.8932 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n4 | contradiction | entailment | 0.9468 | In httpx, the maximum number of allowable connections in the connection pool is configured by the timeout argument. |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.5422 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.7388 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.8574 | Specifying redirect=False disables the retrying logic of urllib3. |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.7388 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.9209 | Specifying redirect=False disables the retrying logic of urllib3. |
| hallucination_evaluation_model | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9219 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| hallucination_evaluation_model | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9219 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.7308 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.853 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| hallucination_evaluation_model | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.5901 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.7308 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.853 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| hallucination_evaluation_model | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.5901 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9954 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o3 | neutral | entailment | 0.6984 | UnrewindableBodyError is an exception class defined in the urllib3.exceptions module. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9954 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9926 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.8775 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.9832 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.999 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.9923 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.9832 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9557 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9729 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.7729 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b1 | neutral | entailment | 0.938 | urllib3 always emits a FutureWarning whenever ssl_context is passed to a ProxyManager instead of proxy_ssl_context. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b2 | entailment (borderline) | neutral | 0.1344 | urllib3 now resolves LifoQueue from the queue module after ConnectionPool instantiation because gevent monkey-patches queue.LifoQueue. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.726 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9992 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9991 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9994 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9995 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9985 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.9892 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9965 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.9602 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3038 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0217 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9882 | With exponential backoff, Retry waits before the second attempt. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0763 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9974 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | o1 | neutral | entailment | 0.6682 | An httpx.Timeout instance can be passed to the timeout parameter of httpx.Client. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9992 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.7922 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o2 | neutral | entailment | 0.6795 | httpx.ConnectTimeout, httpx.ReadTimeout, httpx.WriteTimeout and httpx.PoolTimeout are all subclasses of httpx.TimeoutException. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0048 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.6964 | Specifying redirect=False disables the retrying logic of urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9965 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9991 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9886 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.7594 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9988 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9886 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.7594 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9988 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9961 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9961 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9932 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.9679 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9932 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.9679 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9557 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9557 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.7388 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9974 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.7388 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9974 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | contradiction | 0.2079 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | contradiction | 0.2079 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9977 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9988 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9977 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9988 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9826 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9826 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.3904 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0946 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1422 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.3904 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0946 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1422 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0179 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9978 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0179 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9978 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0031 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0031 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9987 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.9398 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9971 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9987 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.9398 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9971 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9954 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9954 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9926 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.9679 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9932 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.9679 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9557 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9557 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b2 | entailment (borderline) | neutral | 0.1344 | urllib3 now resolves LifoQueue from the queue module after ConnectionPool instantiation because gevent monkey-patches queue.LifoQueue. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.726 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9974 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9974 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | contradiction | 0.2079 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | contradiction | 0.2079 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9988 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9988 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9826 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9826 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.3904 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0946 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0217 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.3904 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0946 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1422 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0179 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9974 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0179 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9978 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0031 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0031 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9886 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.7594 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9971 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9886 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.7594 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9971 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.8933 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.6307 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o1 | neutral | entailment | 0.6305 | urllib3.ProxyManager is a subclass of urllib3.PoolManager. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o3 | neutral | entailment | 0.9502 | UnrewindableBodyError is an exception class defined in the urllib3.exceptions module. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.9502 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.9281 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.6307 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.2732 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c28 | entailment | neutral | 0.2976 | urllib3 fixed an `AttributeError` on Python built with OpenSSL 4+, where `ssl.PROTOCOL_TLSv1` no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c29 | entailment | neutral | 0.4335 | In Python built with OpenSSL 4+, `ssl.PROTOCOL_TLSv1` no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c28 | entailment | neutral | 0.3541 | urllib3 fixed an `AttributeError` on Python built with OpenSSL 4+, where `ssl.PROTOCOL_TLSv1` no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.961 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n5 | contradiction | entailment | 0.5158 | urllib3 2.8.0 raises ValueError instead of UnrewindableBodyError when retrying a request whose body has tell() but not seek(). |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.825 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9575 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.712 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n5 | contradiction | entailment | 0.9111 | urllib3 2.8.0 raises ValueError instead of UnrewindableBodyError when retrying a request whose body has tell() but not seek(). |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.825 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b2 | entailment (borderline) | neutral | 0.3353 | urllib3 now resolves LifoQueue from the queue module after ConnectionPool instantiation because gevent monkey-patches queue.LifoQueue. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.5615 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b1 | neutral | entailment | 0.579 | urllib3 always emits a FutureWarning whenever ssl_context is passed to a ProxyManager instead of proxy_ssl_context. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b3 | neutral | entailment | 0.5697 | urllib3 fixed the SOCKS proxy credential bug so that percent-encoded passwords no longer cause authentication failures with the proxy server. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c36 | entailment | neutral | 0.2719 | In urllib3 2.8.0, an AttributeError was fixed on Python built with OpenSSL 4+, where ssl.PROTOCOL_TLSv1 no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c26 | entailment | neutral | 0.4065 | Users on newer Python versions than 3.10, 3.11 and 3.12 should upgrade to Python 3.13.14+ or 3.14.5+ to get the same security fixes as the urllib3 proxy tunneling safeguards. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c36 | entailment | neutral | 0.2999 | In urllib3 2.8.0, an AttributeError was fixed on Python built with OpenSSL 4+, where ssl.PROTOCOL_TLSv1 no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b1 | neutral | entailment | 0.5984 | urllib3's HTTPResponse.stream() always buffers chunk-size lines of unbounded length in memory. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9232 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.942 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9592 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.949 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.97 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | negatives-handmade | n6 | contradiction (borderline) | entailment | 0.5345 | urllib3 2.7.0 fixed the ignored TLS configuration for HTTPS proxies. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9776 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-security | negatives-handmade | n6 | contradiction (borderline) | entailment | 0.9395 | urllib3 2.7.0 fixed the ignored TLS configuration for HTTPS proxies. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.7671 | urllib3 supports decoding deflate-encoded response bodies. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-security | sonnet-medium | c9 | entailment | neutral | 0.1896 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop has Medium severity. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.1881 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c4 | entailment | neutral | 0.2631 | A non-zero backoff_factor can be set to introduce exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.3871 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.4177 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.2703 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0864 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.1729 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0698 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.2161 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.1732 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.3419 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8828 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n2 | contradiction | entailment | 0.9318 | The default backoff_factor of Retry is 0.5. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.9697 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9753 | With exponential backoff, Retry waits before the second attempt. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.9273 | The backoff delays of Retry grow linearly between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.4876 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.2017 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.3206 | HTTPX supports only four types of timeouts. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.8806 | The limits argument is used to configure pool timeouts in HTTPX. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9685 | The limits argument is used to configure pool timeouts in HTTPX. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.7699 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.7227 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n2 | contradiction | entailment | 0.7662 | If httpx is unable to connect within the connect timeout, a ReadTimeout exception is raised. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.9628 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.5253 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0148 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.5185 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.5584 | Specifying redirect=False disables the retrying logic of urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.8929 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.7037 | Specifying redirect=False disables the retrying logic of urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.8998 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9596 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5005 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.8395 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.4674 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5005 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.8395 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.4674 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.8933 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.6839 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.8933 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.6839 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.2022 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.2022 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9391 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.7744 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9391 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.7744 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b2 | entailment (borderline) | neutral | 0.3801 | urllib3 now resolves LifoQueue from the queue module after ConnectionPool instantiation because gevent monkey-patches queue.LifoQueue. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b2 | entailment (borderline) | neutral | 0.3801 | urllib3 now resolves LifoQueue from the queue module after ConnectionPool instantiation because gevent monkey-patches queue.LifoQueue. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9068 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.8757 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9068 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.8757 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.1806 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.1817 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0751 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.1806 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.1817 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0751 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9599 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9599 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c4 | entailment | neutral | 0.3079 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c5 | entailment | neutral | 0.2457 | In urllib3 2.8.0, a security issue was fixed where `read_chunked()` could buffer a chunk-size line of unbounded length in memory. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.1146 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c9 | entailment | neutral | 0.2751 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop has Medium severity. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c4 | entailment | neutral | 0.3079 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c5 | entailment | neutral | 0.2457 | In urllib3 2.8.0, a security issue was fixed where `read_chunked()` could buffer a chunk-size line of unbounded length in memory. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.1146 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c9 | entailment | neutral | 0.2751 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop has Medium severity. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.3143 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.3143 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.1369 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.3779 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0977 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.1626 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.1082 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1869 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.1826 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.1369 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.3779 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0977 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.1626 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.1082 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1869 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.1826 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8587 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8587 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.4172 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.4172 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.3608 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.3608 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.1603 | HTTPX supports only four types of timeouts. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9474 | The limits argument is used to configure pool timeouts in HTTPX. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.1603 | HTTPX supports only four types of timeouts. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9474 | The limits argument is used to configure pool timeouts in HTTPX. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.8815 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.8815 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0184 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0184 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.2745 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.2745 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.9137 | Specifying redirect=False disables the retrying logic of urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.9137 | Specifying redirect=False disables the retrying logic of urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.2786 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.2786 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.229 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.3412 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.7569 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.229 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.3412 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.7569 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.8984 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.8743 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.4901 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.8984 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.8743 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.4901 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.8933 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.8933 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o5 | neutral | entailment | 0.6839 | HTTPConnectionPool.urlopen raises a ValueError whenever it is called with an invalid timeout argument. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.2022 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c28 | entailment | neutral | 0.2976 | urllib3 fixed an `AttributeError` on Python built with OpenSSL 4+, where `ssl.PROTOCOL_TLSv1` no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c29 | entailment | neutral | 0.4335 | In Python built with OpenSSL 4+, `ssl.PROTOCOL_TLSv1` no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.2022 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c28 | entailment | neutral | 0.3541 | urllib3 fixed an `AttributeError` on Python built with OpenSSL 4+, where `ssl.PROTOCOL_TLSv1` no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9391 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.7744 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9391 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.7744 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b2 | entailment (borderline) | neutral | 0.3353 | urllib3 now resolves LifoQueue from the queue module after ConnectionPool instantiation because gevent monkey-patches queue.LifoQueue. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b2 | entailment (borderline) | neutral | 0.3801 | urllib3 now resolves LifoQueue from the queue module after ConnectionPool instantiation because gevent monkey-patches queue.LifoQueue. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c36 | entailment | neutral | 0.2719 | In urllib3 2.8.0, an AttributeError was fixed on Python built with OpenSSL 4+, where ssl.PROTOCOL_TLSv1 no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c26 | entailment | neutral | 0.4065 | Users on newer Python versions than 3.10, 3.11 and 3.12 should upgrade to Python 3.13.14+ or 3.14.5+ to get the same security fixes as the urllib3 proxy tunneling safeguards. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c36 | entailment | neutral | 0.2999 | In urllib3 2.8.0, an AttributeError was fixed on Python built with OpenSSL 4+, where ssl.PROTOCOL_TLSv1 no longer exists. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9068 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.8757 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9068 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.8757 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.1806 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.1817 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0751 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.1806 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.1817 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0751 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9599 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9599 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c4 | entailment | neutral | 0.3079 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c5 | entailment | neutral | 0.2457 | In urllib3 2.8.0, a security issue was fixed where `read_chunked()` could buffer a chunk-size line of unbounded length in memory. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.1146 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-security | sonnet-medium | c9 | entailment | neutral | 0.1896 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop has Medium severity. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c4 | entailment | neutral | 0.3079 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c5 | entailment | neutral | 0.2457 | In urllib3 2.8.0, a security issue was fixed where `read_chunked()` could buffer a chunk-size line of unbounded length in memory. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.1146 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-security | sonnet-medium | c9 | entailment | neutral | 0.2751 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop has Medium severity. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.1881 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.3143 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c4 | entailment | neutral | 0.2631 | A non-zero backoff_factor can be set to introduce exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.3871 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.1369 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.2703 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0864 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.1626 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0698 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1869 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.1732 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.1369 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.3779 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0977 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.1626 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.1082 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1869 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.1826 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8587 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8587 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.4172 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.4172 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.2017 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.3608 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.1603 | HTTPX supports only four types of timeouts. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.8806 | The limits argument is used to configure pool timeouts in HTTPX. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.1603 | HTTPX supports only four types of timeouts. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9474 | The limits argument is used to configure pool timeouts in HTTPX. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.7227 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n3 | contradiction | entailment | 0.8815 | The httpx pool timeout specifies the maximum duration to wait for data to be sent. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0148 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0184 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.2745 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.2745 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.5584 | Specifying redirect=False disables the retrying logic of urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.7037 | Specifying redirect=False disables the retrying logic of urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.2786 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.2786 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.229 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.3412 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.7569 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.229 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.3412 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.7569 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5005 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.8395 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.4674 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5005 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.8395 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.4674 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |

## Cross-section pairs kept (argmax)

| model | context | premise | win | premise section | claim from | id | p_ent | claim |
|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9437 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.8532 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9971 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9437 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| nli-deberta-v3-base | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9969 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.8635 | A Retry instance can be used for more granular control of retries in urllib3. |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.8116 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.9761 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5705 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| nli-deberta-v3-base | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9957 | A Timeout instance allows specifying separate connect and read timeouts. |
| nli-deberta-v3-base | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9847 | A Timeout instance allows specifying separate connect and read timeouts. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.992 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9962 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.992 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9962 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9853 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.995 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9853 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.995 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9943 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9943 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| nli-deberta-v3-base | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9947 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| nli-deberta-v3-base | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9947 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.7464 | Retries can be controlled using the retries parameter to request() in urllib3. |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.7464 | Retries can be controlled using the retries parameter to request() in urllib3. |
| nli-deberta-v3-base | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9865 | A Timeout instance allows specifying separate connect and read timeouts. |
| nli-deberta-v3-base | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9865 | A Timeout instance allows specifying separate connect and read timeouts. |
| nli-deberta-v3-base | breadcrumb | local | 128 | using-timeouts | httpx-timeouts-fine-tuning~sonnet-medium | c1 | 0.4822 | HTTPX allows specifying timeout behavior in more fine grained detail. |
| nli-deberta-v3-base | breadcrumb | local | 400 | using-timeouts | httpx-timeouts-fine-tuning~sonnet-medium | c1 | 0.4822 | HTTPX allows specifying timeout behavior in more fine grained detail. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.992 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9853 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| nli-deberta-v3-base | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9865 | A Timeout instance allows specifying separate connect and read timeouts. |
| nli-deberta-v3-base | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9847 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9815 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.6745 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c3 | 0.5906 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9242 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9403 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9912 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.8666 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.7056 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9685 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.7762 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.988 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9281 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c4 | 0.5252 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9408 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c13 | 0.6879 | In urllib3, proxy CA certificates and client certificates should be configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9906 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c4 | 0.4769 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9823 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9865 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9146 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9787 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9258 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c8 | 0.6853 | In urllib3, LifoQueue is no longer taken from the default cached QueueCls class property of ConnectionPool when initializing the default ConnectionPool.pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c10 | 0.6911 | In urllib3 2.8.0, UnrewindableBodyError is raised instead of ValueError when retrying a request whose body had tell() but not seek(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c16 | 0.5675 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c26 | 0.5158 | Users on newer Python versions than 3.10, 3.11 and 3.12 should upgrade to Python 3.13.14+ or 3.14.5+ to get the same security fixes as the urllib3 proxy tunneling safeguards. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.8971 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9795 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c35 | 0.9671 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c16 | 0.6046 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c17 | 0.5354 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include decimal integers such as 2130706433. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.5265 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9531 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c35 | 0.9634 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c1 | 0.8835 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.9813 | Retries can be controlled using the retries parameter to request() in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.8424 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c8 | 0.5221 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9312 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c1 | 0.9693 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.996 | Retries can be controlled using the retries parameter to request() in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.9714 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9873 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c1 | 0.8835 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c3 | 0.9243 | Retries in urllib3 can be controlled using the retries parameter to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.8228 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c13 | 0.7963 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c1 | 0.9693 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c3 | 0.9922 | Retries in urllib3 can be controlled using the retries parameter to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c6 | 0.7635 | The number of retries in urllib3 can be changed by specifying an integer. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.9722 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.7033 | The Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c13 | 0.9492 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c1 | 0.8835 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.9692 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.8178 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c8 | 0.5334 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.9147 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c1 | 0.9693 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.994 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.9714 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c8 | 0.6922 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.9786 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c1 | 0.8835 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c3 | 0.9178 | urllib3 retries can be controlled using the retries parameter to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9045 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c10 | 0.3777 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.9543 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c17 | 0.6032 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c1 | 0.9693 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c3 | 0.9922 | urllib3 retries can be controlled using the retries parameter to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9753 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.9884 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c17 | 0.9269 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c1 | 0.8835 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.9908 | The retries parameter of urllib3's request() controls retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.8799 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c9 | 0.4944 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c1 | 0.9693 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.9944 | The retries parameter of urllib3's request() controls retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.964 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.523 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.9834 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9698 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.828 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9308 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c6 | 0.4837 | A pool-level timeout can be overridden by specifying timeout to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | using-timeouts~sonnet-medium | c5 | 0.5554 | A urllib3 Timeout instance lets you specify separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~sonnet-medium | c5 | 0.5854 | A urllib3 Timeout instance lets you specify separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c1 | 0.9367 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c1 | 0.9377 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | configuring-exponential-backoff~haiku-high | c1 | 0.7949 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | configuring-exponential-backoff~haiku-high | c1 | 0.9487 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | configuring-exponential-backoff~opus-high | c1 | 0.9367 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | configuring-exponential-backoff~opus-high | c1 | 0.9377 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | configuring-exponential-backoff~sonnet-medium | c1 | 0.8075 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | configuring-exponential-backoff~sonnet-medium | c1 | 0.9348 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9861 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.6745 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c3 | 0.7094 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.6683 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.955 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9913 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9728 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9861 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.6745 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c3 | 0.7094 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.6683 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.955 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9913 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9728 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.4735 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c4 | 0.5252 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.8567 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c13 | 0.7508 | In urllib3, proxy CA certificates and client certificates should be configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9927 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9592 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.4735 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c4 | 0.5252 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.8567 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c13 | 0.7508 | In urllib3, proxy CA certificates and client certificates should be configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9927 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9592 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9846 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9846 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9853 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c35 | 0.845 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9853 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c35 | 0.845 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.8182 | Retries can be controlled using the retries parameter to request() in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c8 | 0.8136 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.8182 | Retries can be controlled using the retries parameter to request() in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c8 | 0.8136 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.94 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.6239 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c8 | 0.8674 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.603 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.94 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.6239 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c8 | 0.8674 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.603 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.7511 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c10 | 0.5232 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5522 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.7511 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c10 | 0.5232 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5522 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.9638 | The retries parameter of urllib3's request() controls retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.612 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c9 | 0.6195 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.9638 | The retries parameter of urllib3's request() controls retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.612 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c9 | 0.6195 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.9009 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9314 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.9009 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9314 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c1 | 0.8918 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c2 | 0.5357 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c1 | 0.8918 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c2 | 0.5357 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | configuring-exponential-backoff~flash-lite-3.6-high | c1 | 0.7363 | By default, Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | configuring-exponential-backoff~flash-lite-3.6-high | c2 | 0.4633 | The default backoff_factor value for Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | configuring-exponential-backoff~flash-lite-3.6-high | c1 | 0.7363 | By default, Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | configuring-exponential-backoff~flash-lite-3.6-high | c2 | 0.4633 | The default backoff_factor value for Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | configuring-exponential-backoff~haiku-high | c1 | 0.7396 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | configuring-exponential-backoff~haiku-high | c1 | 0.7396 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | configuring-exponential-backoff~opus-high | c1 | 0.8918 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | configuring-exponential-backoff~opus-high | c1 | 0.8918 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | configuring-exponential-backoff~sonnet-medium | c1 | 0.6944 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | configuring-exponential-backoff~sonnet-medium | c1 | 0.6944 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9815 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.6745 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c3 | 0.5906 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.6683 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9403 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9912 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.8666 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.6745 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.6683 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.7762 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.988 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9281 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c4 | 0.5252 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.8567 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c13 | 0.6879 | In urllib3, proxy CA certificates and client certificates should be configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9906 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c4 | 0.4769 | In urllib3 2.8.0, a security issue was fixed where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.8567 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9865 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9146 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9787 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9258 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9795 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c35 | 0.845 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9531 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c35 | 0.845 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.8182 | Retries can be controlled using the retries parameter to request() in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c8 | 0.5221 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.8182 | Retries can be controlled using the retries parameter to request() in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.94 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.6239 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c8 | 0.5334 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.603 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.94 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.6239 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c8 | 0.6922 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.603 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.7511 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c10 | 0.3777 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5522 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.7511 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5522 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.9638 | The retries parameter of urllib3's request() controls retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.612 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c9 | 0.4944 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.9638 | The retries parameter of urllib3's request() controls retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.612 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.9009 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9314 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.828 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9308 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c1 | 0.8918 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c1 | 0.8918 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | configuring-exponential-backoff~haiku-high | c1 | 0.7396 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | configuring-exponential-backoff~haiku-high | c1 | 0.7396 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | configuring-exponential-backoff~opus-high | c1 | 0.8918 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | configuring-exponential-backoff~opus-high | c1 | 0.8918 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | configuring-exponential-backoff~sonnet-medium | c1 | 0.6944 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | configuring-exponential-backoff~sonnet-medium | c1 | 0.6944 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.5056 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.6387 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.8649 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.8227 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.6765 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.7133 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.8938 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.8895 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9237 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.6387 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.8968 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.7738 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.7133 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9105 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.836 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.8817 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.9044 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.9089 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.5732 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c2 | 0.5456 | urllib3's automatic retry mechanism also handles redirects. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.6072 | Retries can be controlled using the retries parameter to request() in urllib3. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.7257 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c2 | 0.5629 | The retry mechanism of urllib3 also handles redirects. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c2 | 0.7619 | The retry mechanism of urllib3 also handles redirects. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c3 | 0.6705 | Retries in urllib3 can be controlled using the retries parameter to request(). |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c2 | 0.5291 | The mechanism that retries requests in urllib3 also handles redirects. |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.5356 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.5106 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c2 | 0.7406 | The mechanism that retries requests in urllib3 also handles redirects. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.6348 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.6619 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.5183 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c2 | 0.576 | The urllib3 mechanism that retries idempotent requests also handles redirects. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c3 | 0.6916 | urllib3 retries can be controlled using the retries parameter to request(). |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.6858 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5042 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| hallucination_evaluation_model | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.6161 | The retries parameter of urllib3's request() controls retries. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c2 | 0.6856 | The urllib3 retry mechanism also handles redirects. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.7261 | The retries parameter of urllib3's request() controls retries. |
| hallucination_evaluation_model | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.5361 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| hallucination_evaluation_model | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.7501 | A Timeout instance allows specifying separate connect and read timeouts. |
| hallucination_evaluation_model | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.8362 | A Timeout instance allows specifying separate connect and read timeouts. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.5134 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.7274 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9162 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.5461 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9422 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.8897 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.5134 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.7274 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9162 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.5461 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9422 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.8897 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.7274 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9284 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.8928 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.8406 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.7274 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9284 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.8928 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.8406 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.5557 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.5557 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.7007 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.6777 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.7007 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.6777 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c2 | 0.5627 | urllib3's automatic retry mechanism also handles redirects. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.629 | Retries can be controlled using the retries parameter to request() in urllib3. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.6796 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c2 | 0.5627 | urllib3's automatic retry mechanism also handles redirects. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.629 | Retries can be controlled using the retries parameter to request() in urllib3. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.6796 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c2 | 0.7226 | The retry mechanism of urllib3 also handles redirects. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c3 | 0.6856 | Retries in urllib3 can be controlled using the retries parameter to request(). |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c2 | 0.7226 | The retry mechanism of urllib3 also handles redirects. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c3 | 0.6856 | Retries in urllib3 can be controlled using the retries parameter to request(). |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.7033 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.5571 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.7033 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.5571 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c3 | 0.6583 | urllib3 retries can be controlled using the retries parameter to request(). |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.6184 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c3 | 0.6583 | urllib3 retries can be controlled using the retries parameter to request(). |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.6184 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c2 | 0.6136 | The urllib3 retry mechanism also handles redirects. |
| hallucination_evaluation_model | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.614 | The retries parameter of urllib3's request() controls retries. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c2 | 0.6136 | The urllib3 retry mechanism also handles redirects. |
| hallucination_evaluation_model | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.614 | The retries parameter of urllib3's request() controls retries. |
| hallucination_evaluation_model | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.6461 | A Timeout instance allows specifying separate connect and read timeouts. |
| hallucination_evaluation_model | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.6461 | A Timeout instance allows specifying separate connect and read timeouts. |
| hallucination_evaluation_model | breadcrumb | local | 128 | retrying-requests | configuring-exponential-backoff~sonnet-medium | c4 | 0.6216 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| hallucination_evaluation_model | breadcrumb | local | 400 | retrying-requests | configuring-exponential-backoff~sonnet-medium | c4 | 0.6216 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.5056 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.6387 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.8649 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.8227 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.5134 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.7133 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.8938 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.8895 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.8897 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.6387 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.8968 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.7738 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.7133 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9105 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.836 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.8406 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| hallucination_evaluation_model | breadcrumb | both | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.7007 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | both | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.7007 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.5732 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c2 | 0.5456 | urllib3's automatic retry mechanism also handles redirects. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c3 | 0.6072 | Retries can be controlled using the retries parameter to request() in urllib3. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.6796 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c2 | 0.5629 | The retry mechanism of urllib3 also handles redirects. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c2 | 0.7226 | The retry mechanism of urllib3 also handles redirects. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c3 | 0.6705 | Retries in urllib3 can be controlled using the retries parameter to request(). |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.5356 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.5106 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.6348 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.5571 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.5183 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c3 | 0.6583 | urllib3 retries can be controlled using the retries parameter to request(). |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.6184 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| hallucination_evaluation_model | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.614 | The retries parameter of urllib3's request() controls retries. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c2 | 0.6136 | The urllib3 retry mechanism also handles redirects. |
| hallucination_evaluation_model | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.614 | The retries parameter of urllib3's request() controls retries. |
| hallucination_evaluation_model | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.6461 | A Timeout instance allows specifying separate connect and read timeouts. |
| hallucination_evaluation_model | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.6461 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9933 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.8749 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9975 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9715 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9902 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9993 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9835 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9945 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c3 | 0.4665 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9988 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9927 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c7 | 0.8174 | In urllib3, proxy CA certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.5522 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c9 | 0.9475 | In urllib3, proxy identity checks are configured with `proxy_assert_hostname` or `proxy_assert_fingerprint`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9982 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9982 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.9236 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9975 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9878 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9993 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.989 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.9794 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c5 | 0.5495 | In urllib3 2.8.0, a security issue was fixed where `read_chunked()` could buffer a chunk-size line of unbounded length in memory. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9988 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.996 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c14 | 0.8417 | In urllib3, proxy identity checks should be configured with `proxy_assert_hostname` or `proxy_assert_fingerprint`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9989 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9986 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c22 | 0.9582 | urllib3 fixed `HTTPSConnection.connect()` overriding `ProxyConfig.ssl_context`'s certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.8785 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c22 | 0.5655 | urllib3 fixed `HTTPSConnection.connect()` overriding `ProxyConfig.ssl_context`'s certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9264 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c26 | 0.5397 | Users on newer Python versions than 3.10, 3.11 and 3.12 should upgrade to Python 3.13.14+ or 3.14.5+ to get the same security fixes as the urllib3 proxy tunneling safeguards. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.9847 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.7389 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c15 | 0.6118 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include hex such as 0x7f000001. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c16 | 0.7751 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c17 | 0.6676 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include decimal integers such as 2130706433. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c26 | 0.6735 | Users on newer Python versions than 3.10, 3.11 and 3.12 should upgrade to Python 3.13.14+ or 3.14.5+ to get the same security fixes as the urllib3 proxy tunneling safeguards. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.9173 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.8722 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c38 | 0.8263 | Using cryptography APIs in urllib3.contrib.pyopenssl avoids a DeprecationWarning raised by pyOpenSSL 26.3.0+. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.9635 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9907 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.9938 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9779 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c6 | 0.6074 | The number of retries in urllib3 can be changed by specifying an integer. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.9738 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c6 | 0.9096 | The number of retries in urllib3 can be changed by specifying an integer. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.9509 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.8581 | The Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.8815 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.9883 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.9941 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.997 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c13 | 0.7566 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9601 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9957 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c17 | 0.6941 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.9691 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.9962 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.8385 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.9742 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9929 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.5505 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9991 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~sonnet-medium | c5 | 0.9074 | A urllib3 Timeout instance lets you specify separate connect and read timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9954 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.8749 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9988 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9711 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9573 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9991 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9987 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9954 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.8749 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9988 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9711 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9573 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9991 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9987 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.9628 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9988 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9914 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9993 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9992 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.9628 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9988 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9914 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9993 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9992 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9913 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9913 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.8782 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9853 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.8782 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9853 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.9939 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9867 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.9939 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9867 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c6 | 0.9053 | The number of retries in urllib3 can be changed by specifying an integer. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.8991 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.9719 | The Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c6 | 0.9053 | The number of retries in urllib3 can be changed by specifying an integer. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.8991 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.9719 | The Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.9893 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.9932 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.9893 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.9932 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9946 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.9641 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9946 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.9641 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.9945 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.9601 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.9945 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.9601 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9952 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9952 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9933 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.8749 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9975 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9711 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9573 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9991 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9835 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9945 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9988 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.9711 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.5522 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9982 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9982 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.9236 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9975 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9878 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9993 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.989 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.9628 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9988 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.9914 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9989 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9986 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.8785 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9264 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.8782 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.7389 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.8782 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.8722 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.9635 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9867 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.9938 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9779 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c6 | 0.6074 | The number of retries in urllib3 can be changed by specifying an integer. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.8991 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c6 | 0.9053 | The number of retries in urllib3 can be changed by specifying an integer. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.8991 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.8581 | The Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.8815 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.9883 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.9893 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.9932 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9601 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9946 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.9691 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.9945 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.8385 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9929 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9952 | A Timeout instance allows specifying separate connect and read timeouts. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.5614 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.5205 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c7 | 0.7085 | In urllib3, proxy CA certificates are configured in `proxy_ssl_context`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9697 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c9 | 0.8521 | In urllib3, proxy identity checks are configured with `proxy_assert_hostname` or `proxy_assert_fingerprint`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.8339 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c13 | 0.5451 | In urllib3, proxy CA certificates and client certificates should be configured in `proxy_ssl_context`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c14 | 0.7479 | In urllib3, proxy identity checks should be configured with `proxy_assert_hostname` or `proxy_assert_fingerprint`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.7776 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.5619 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.6867 | A Retry instance can be used for more granular control of retries in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c6 | 0.9036 | The number of retries in urllib3 can be changed by specifying an integer. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.6336 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.671 | The Retry class allows far greater control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.7804 | A Retry instance gives more granular control over retries in urllib3. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.854 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.5523 | The urllib3 Retry class allows far greater control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.8278 | The retries parameter of urllib3's request() controls retries. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.7167 | The urllib3 Retry class allows far greater control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c2 | 0.9376 | Timeouts are measured in seconds. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | window | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c2 | 0.7342 | Timeouts are measured in seconds. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.8158 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.6411 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.8158 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.6411 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.5097 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.5097 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.5673 | The Retry class allows far greater control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.5673 | The Retry class allows far greater control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.5574 | The urllib3 Retry class allows far greater control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.5574 | The urllib3 Retry class allows far greater control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.5614 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.5205 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.8158 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.6411 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.5097 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.5673 | The Retry class allows far greater control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.5523 | The urllib3 Retry class allows far greater control of how requests are retried. |
| MiniCheck-DeBERTa-v3-Large | breadcrumb | both | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.5574 | The urllib3 Retry class allows far greater control of how requests are retried. |
