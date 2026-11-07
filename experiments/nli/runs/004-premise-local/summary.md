# Run 004-premise-local

- note: 4 models (large now fp32); window vs cited sentence +-1 vs both; threshold sweep
- started: `2026-11-07T15:52:15`
- models: `['cross-encoder/nli-deberta-v3-xsmall', 'cross-encoder/nli-deberta-v3-base', 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli', 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli']`
- contexts: `['none', 'breadcrumb']`
- premises: `['window', 'local']`
- radius: `1`
- sections: `all`
- batch: `8`
- git: `{'commit': 'e8077b00a58fcaac2cbebef8f3f9dc7762970048', 'branch': 'feat/nli-and-extractors-testing', 'dirty_experiment_files': True}`
- inputs: `{'pairs_windows_sha256': '785dc17026be', 'labels_sha256': '0da00b1e7a82'}`
- versions: `{'python': '3.12.10', 'torch': '2.15.0+cpu', 'transformers': '5.22.2'}`
- threads: `10`
- seconds: `{'cross-encoder/nli-deberta-v3-xsmall': {'revision': '', 'none/window': {'seconds': 0.0, 'scored': 0, 'unique': 252}, 'none/local': {'seconds': 8.4, 'scored': 126, 'unique': 126}, 'breadcrumb/window': {'seconds': 0.0, 'scored': 0, 'unique': 252}, 'breadcrumb/local': {'seconds': 4.3, 'scored': 126, 'unique': 126}}, 'cross-encoder/nli-deberta-v3-base': {'revision': '', 'none/window': {'seconds': 0.0, 'scored': 0, 'unique': 252}, 'none/local': {'seconds': 15.8, 'scored': 126, 'unique': 126}, 'breadcrumb/window': {'seconds': 0.0, 'scored': 0, 'unique': 252}, 'breadcrumb/local': {'seconds': 16.2, 'scored': 126, 'unique': 126}}, 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli': {'revision': '', 'none/window': {'seconds': 91.1, 'scored': 252, 'unique': 252}, 'none/local': {'seconds': 14.0, 'scored': 126, 'unique': 126}, 'breadcrumb/window': {'seconds': 64.7, 'scored': 252, 'unique': 252}, 'breadcrumb/local': {'seconds': 16.3, 'scored': 126, 'unique': 126}}, 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli': {'revision': '', 'none/window': {'seconds': 198.6, 'scored': 252, 'unique': 252}, 'none/local': {'seconds': 46.8, 'scored': 126, 'unique': 126}, 'breadcrumb/window': {'seconds': 213.9, 'scored': 252, 'unique': 252}, 'breadcrumb/local': {'seconds': 53.3, 'scored': 126, 'unique': 126}}}`
- finished: `2026-11-07T16:04:42`

## Metrics vs labels.csv (139 labelled claims, annotator: claude-draft)

Keep = NLI says entailment (claim survives grounding). Dropped by the citation check = not kept. `nb` = without borderline labels. Premise `window` = NLI window, `local` = cited sentence(s) +-1, `both` = kept only if both say entailment.

| model | context | premise | win | n | keep acc | keep recall | keep precision | false keeps | contra recall | keep acc nb |
|---|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | none | window | 128 | 139 | 49% | 42% | 96% | 2 | 71% | 49% |
| nli-deberta-v3-xsmall | none | window | 400 | 139 | 62% | 58% | 96% | 3 | 71% | 62% |
| nli-deberta-v3-xsmall | none | local | 128 | 139 | 43% | 34% | 98% | 1 | 64% | 44% |
| nli-deberta-v3-xsmall | none | local | 400 | 139 | 43% | 34% | 98% | 1 | 64% | 44% |
| nli-deberta-v3-xsmall | none | both | 128 | 139 | 35% | 25% | 97% | 1 | 64% | 35% |
| nli-deberta-v3-xsmall | none | both | 400 | 139 | 39% | 29% | 100% | 0 | 64% | 39% |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | 139 | 79% | 78% | 97% | 3 | 57% | 79% |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | 139 | 84% | 85% | 96% | 4 | 57% | 85% |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | 139 | 88% | 90% | 96% | 4 | 64% | 89% |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | 139 | 88% | 90% | 96% | 4 | 64% | 89% |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | 139 | 73% | 71% | 97% | 3 | 64% | 73% |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | 139 | 76% | 75% | 97% | 3 | 64% | 77% |
| nli-deberta-v3-base | none | window | 128 | 139 | 49% | 42% | 96% | 2 | 71% | 50% |
| nli-deberta-v3-base | none | window | 400 | 139 | 57% | 50% | 98% | 1 | 71% | 56% |
| nli-deberta-v3-base | none | local | 128 | 139 | 49% | 41% | 98% | 1 | 64% | 49% |
| nli-deberta-v3-base | none | local | 400 | 139 | 49% | 41% | 98% | 1 | 64% | 49% |
| nli-deberta-v3-base | none | both | 128 | 139 | 45% | 36% | 98% | 1 | 64% | 45% |
| nli-deberta-v3-base | none | both | 400 | 139 | 45% | 36% | 100% | 0 | 64% | 45% |
| nli-deberta-v3-base | breadcrumb | window | 128 | 139 | 80% | 78% | 98% | 2 | 71% | 79% |
| nli-deberta-v3-base | breadcrumb | window | 400 | 139 | 78% | 75% | 99% | 1 | 71% | 78% |
| nli-deberta-v3-base | breadcrumb | local | 128 | 139 | 94% | 95% | 97% | 3 | 71% | 93% |
| nli-deberta-v3-base | breadcrumb | local | 400 | 139 | 94% | 95% | 97% | 3 | 71% | 93% |
| nli-deberta-v3-base | breadcrumb | both | 128 | 139 | 78% | 76% | 98% | 2 | 71% | 78% |
| nli-deberta-v3-base | breadcrumb | both | 400 | 139 | 76% | 73% | 99% | 1 | 71% | 76% |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | 139 | 72% | 69% | 98% | 2 | 93% | 71% |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | 139 | 86% | 87% | 97% | 3 | 86% | 86% |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | 139 | 55% | 47% | 100% | 0 | 86% | 53% |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | 139 | 55% | 47% | 100% | 0 | 86% | 53% |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | 139 | 53% | 45% | 100% | 0 | 86% | 51% |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | 139 | 53% | 45% | 100% | 0 | 86% | 51% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | 139 | 98% | 99% | 98% | 2 | 93% | 98% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | 139 | 98% | 100% | 98% | 3 | 86% | 98% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | 139 | 98% | 99% | 98% | 2 | 93% | 98% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | 139 | 98% | 99% | 98% | 2 | 93% | 98% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | 139 | 97% | 98% | 98% | 2 | 93% | 97% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | 139 | 98% | 99% | 98% | 2 | 93% | 98% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | 139 | 73% | 69% | 99% | 1 | 100% | 72% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | 139 | 87% | 87% | 97% | 3 | 86% | 87% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | 139 | 55% | 48% | 98% | 1 | 79% | 53% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | 139 | 55% | 48% | 98% | 1 | 79% | 53% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | 139 | 55% | 47% | 100% | 0 | 86% | 53% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | 139 | 54% | 47% | 98% | 1 | 79% | 53% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | 139 | 98% | 98% | 99% | 1 | 100% | 98% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | 139 | 98% | 100% | 98% | 3 | 86% | 98% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | 139 | 98% | 97% | 100% | 0 | 100% | 98% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | 139 | 98% | 97% | 100% | 0 | 100% | 98% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | 139 | 98% | 97% | 100% | 0 | 100% | 98% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | 139 | 98% | 97% | 100% | 0 | 100% | 98% |

## Threshold sweep

Keep if p_entailment >= threshold (argmax = keep if entailment is the top label). Cell = keep recall / false keeps.

| model | context | premise | win | argmax | >= 0.3 | >= 0.5 | >= 0.7 | >= 0.9 |
|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | none | window | 128 | 42% / 2 | 46% / 3 | 42% / 1 | 33% / 1 | 24% / 1 |
| nli-deberta-v3-xsmall | none | window | 400 | 58% / 3 | 62% / 3 | 57% / 3 | 52% / 3 | 31% / 2 |
| nli-deberta-v3-xsmall | none | local | 128 | 34% / 1 | 37% / 1 | 34% / 1 | 34% / 1 | 30% / 0 |
| nli-deberta-v3-xsmall | none | local | 400 | 34% / 1 | 37% / 1 | 34% / 1 | 34% / 1 | 30% / 0 |
| nli-deberta-v3-xsmall | none | both | 128 | 25% / 1 | 29% / 1 | 25% / 0 | 21% / 0 | 18% / 0 |
| nli-deberta-v3-xsmall | none | both | 400 | 29% / 0 | 34% / 0 | 28% / 0 | 24% / 0 | 17% / 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | 78% / 3 | 87% / 4 | 76% / 2 | 67% / 1 | 50% / 1 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | 85% / 4 | 93% / 4 | 85% / 4 | 70% / 2 | 36% / 2 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | 90% / 4 | 90% / 4 | 90% / 4 | 90% / 3 | 82% / 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | 90% / 4 | 90% / 4 | 90% / 4 | 90% / 3 | 82% / 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | 71% / 3 | 80% / 4 | 69% / 2 | 61% / 0 | 48% / 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | 75% / 3 | 83% / 3 | 75% / 3 | 65% / 0 | 36% / 0 |
| nli-deberta-v3-base | none | window | 128 | 42% / 2 | 42% / 2 | 42% / 2 | 41% / 2 | 38% / 1 |
| nli-deberta-v3-base | none | window | 400 | 50% / 1 | 50% / 1 | 50% / 1 | 50% / 1 | 49% / 1 |
| nli-deberta-v3-base | none | local | 128 | 41% / 1 | 41% / 1 | 41% / 1 | 39% / 0 | 38% / 0 |
| nli-deberta-v3-base | none | local | 400 | 41% / 1 | 41% / 1 | 41% / 1 | 39% / 0 | 38% / 0 |
| nli-deberta-v3-base | none | both | 128 | 36% / 1 | 36% / 1 | 36% / 1 | 34% / 0 | 32% / 0 |
| nli-deberta-v3-base | none | both | 400 | 36% / 0 | 36% / 0 | 36% / 0 | 34% / 0 | 33% / 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | 78% / 2 | 79% / 2 | 78% / 2 | 76% / 2 | 76% / 1 |
| nli-deberta-v3-base | breadcrumb | window | 400 | 75% / 1 | 76% / 1 | 75% / 1 | 73% / 1 | 68% / 1 |
| nli-deberta-v3-base | breadcrumb | local | 128 | 95% / 3 | 95% / 3 | 95% / 3 | 92% / 3 | 91% / 2 |
| nli-deberta-v3-base | breadcrumb | local | 400 | 95% / 3 | 95% / 3 | 95% / 3 | 92% / 3 | 91% / 2 |
| nli-deberta-v3-base | breadcrumb | both | 128 | 76% / 2 | 77% / 2 | 76% / 2 | 75% / 2 | 73% / 1 |
| nli-deberta-v3-base | breadcrumb | both | 400 | 73% / 1 | 75% / 1 | 73% / 1 | 71% / 1 | 66% / 1 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | 69% / 2 | 74% / 2 | 69% / 2 | 69% / 1 | 66% / 1 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | 87% / 3 | 89% / 4 | 87% / 3 | 83% / 3 | 80% / 1 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | 47% / 0 | 50% / 0 | 47% / 0 | 46% / 0 | 42% / 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | 47% / 0 | 50% / 0 | 47% / 0 | 46% / 0 | 42% / 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | 45% / 0 | 46% / 0 | 45% / 0 | 45% / 0 | 42% / 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | 45% / 0 | 49% / 0 | 45% / 0 | 45% / 0 | 42% / 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | 99% / 2 | 100% / 2 | 99% / 2 | 98% / 2 | 94% / 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | 100% / 3 | 100% / 3 | 100% / 3 | 99% / 3 | 99% / 2 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | 99% / 2 | 100% / 2 | 99% / 2 | 98% / 2 | 93% / 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | 99% / 2 | 100% / 2 | 99% / 2 | 98% / 2 | 93% / 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | 98% / 2 | 100% / 2 | 98% / 2 | 97% / 2 | 92% / 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | 99% / 2 | 100% / 2 | 99% / 2 | 97% / 2 | 92% / 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | 69% / 1 | 70% / 1 | 69% / 1 | 66% / 1 | 62% / 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | 87% / 3 | 92% / 3 | 87% / 3 | 83% / 3 | 82% / 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | 48% / 1 | 51% / 1 | 48% / 1 | 45% / 0 | 42% / 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | 48% / 1 | 51% / 1 | 48% / 1 | 45% / 0 | 42% / 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | 47% / 0 | 49% / 0 | 47% / 0 | 45% / 0 | 41% / 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | 47% / 1 | 50% / 1 | 47% / 1 | 44% / 0 | 42% / 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | 98% / 1 | 99% / 1 | 98% / 1 | 98% / 1 | 97% / 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | 100% / 3 | 100% / 3 | 100% / 3 | 99% / 2 | 99% / 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | 97% / 0 | 98% / 0 | 97% / 0 | 97% / 0 | 94% / 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | 97% / 0 | 98% / 0 | 97% / 0 | 97% / 0 | 94% / 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | 97% / 0 | 98% / 0 | 97% / 0 | 97% / 0 | 93% / 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | 97% / 0 | 98% / 0 | 97% / 0 | 96% / 0 | 93% / 0 |

## Labels per extractor

| model | context | premise | win | section | extractor | ent | neu | con | dropped |
|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 5 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | 0 | 14 | 0 | 1 |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | flash-lite-3.6-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | 8 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | sonnet-medium | 9 | 6 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 5 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | opus-high | 14 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | sonnet-medium | 12 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-3.6-high | 4 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-lite-3.6-high | 5 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | 4 | 13 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | sonnet-medium | 7 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-3.6-high | 4 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-lite-3.6-high | 5 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | 4 | 13 | 0 | 0 |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | sonnet-medium | 7 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | 0 | 14 | 0 | 1 |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-3.6-high | 4 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-lite-3.6-high | 5 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | haiku-high | 8 | 5 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | 3 | 14 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | sonnet-medium | 6 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-3.6-high | 4 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-lite-3.6-high | 5 | 8 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | haiku-high | 8 | 5 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | 3 | 14 | 0 | 0 |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | sonnet-medium | 6 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 5 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | 8 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | 2 | 4 | 3 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | 7 | 6 | 1 | 1 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | opus-high | 14 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | 2 | 4 | 3 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | 11 | 3 | 0 | 1 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | opus-high | 14 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | sonnet-medium | 12 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 2 | 3 | 4 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 12 | 1 | 1 | 1 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 11 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | opus-high | 15 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 2 | 3 | 4 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 12 | 1 | 1 | 1 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 11 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | opus-high | 15 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 5 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | 7 | 5 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | 2 | 3 | 4 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | 7 | 6 | 1 | 1 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | 11 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | haiku-high | 9 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | opus-high | 12 | 5 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 4 | 4 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | 7 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | 9 | 4 | 1 | 1 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | 11 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | haiku-high | 9 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | opus-high | 12 | 5 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | 1 | 13 | 0 | 1 |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-lite-3.6-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | haiku-high | 9 | 4 | 0 | 0 |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | 7 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | sonnet-medium | 9 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | opus-high | 11 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | 7 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | sonnet-medium | 8 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | 7 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | sonnet-medium | 8 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | 1 | 13 | 0 | 1 |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-3.6-high | 5 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | haiku-high | 8 | 5 | 0 | 0 |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | 6 | 11 | 0 | 0 |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | sonnet-medium | 7 | 8 | 0 | 0 |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-3.6-high | 5 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | haiku-high | 9 | 4 | 0 | 0 |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | 7 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | sonnet-medium | 7 | 8 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | 9 | 5 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | opus-high | 12 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 128 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | 6 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | 11 | 3 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | opus-high | 11 | 6 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | window | 400 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 1 | 2 | 6 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 1 | 2 | 6 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | 7 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | 9 | 5 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | opus-high | 12 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 128 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | 8 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | 6 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | 11 | 3 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | opus-high | 11 | 6 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | both | 400 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | haiku-high | 5 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | opus-high | 3 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | 5 | 9 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | flash-lite-3.6-high | 10 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | opus-high | 15 | 2 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | 3 | 4 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | opus-high | 5 | 4 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | 9 | 5 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | 4 | 10 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | negatives-handmade | 0 | 5 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | opus-high | 9 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | sonnet-medium | 8 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | 4 | 10 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | negatives-handmade | 0 | 5 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | opus-high | 9 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | sonnet-medium | 8 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | 3 | 11 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | negatives-handmade | 0 | 5 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | opus-high | 9 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | sonnet-medium | 8 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | 3 | 11 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | negatives-handmade | 0 | 5 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | opus-high | 9 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | sonnet-medium | 8 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | haiku-high | 7 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | opus-high | 3 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | 6 | 8 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | flash-lite-3.6-high | 10 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | opus-high | 15 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | sonnet-medium | 12 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | 3 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | opus-high | 5 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | 8 | 6 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | haiku-high | 5 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | 5 | 9 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | haiku-high | 9 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | negatives-handmade | 0 | 5 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | 8 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | sonnet-medium | 7 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | haiku-high | 5 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | 5 | 9 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | haiku-high | 9 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | negatives-handmade | 0 | 5 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | 8 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | sonnet-medium | 7 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | haiku-high | 5 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | 4 | 10 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | haiku-high | 9 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | negatives-handmade | 0 | 5 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | 8 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | sonnet-medium | 7 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | haiku-high | 5 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | 4 | 10 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-lite-3.6-high | 7 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | haiku-high | 9 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | negatives-handmade | 0 | 5 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | 8 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | sonnet-medium | 7 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |

## Wrong keep / drop decisions (argmax)

| model | context | premise | win | section | extractor | id | gold | NLI | p_ent | claim |
|---|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0025 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0027 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0042 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0029 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0187 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0234 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0029 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0024 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0039 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0079 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0033 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0072 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0142 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0027 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c1 | entailment | neutral | 0.1501 | By default, Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c2 | entailment | neutral | 0.3113 | The default backoff_factor value for Retry is 0. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0521 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0086 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0306 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.2338 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0023 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0047 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0035 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c4 | entailment | neutral | 0.0622 | In production systems, retrying immediately without backoff can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c5 | entailment | neutral | 0.1168 | In production systems, retrying immediately without backoff can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0036 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0071 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0079 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0028 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0076 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0017 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0044 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0023 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0068 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0074 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0052 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0094 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0051 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0034 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0055 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0025 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0048 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.4501 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | negatives-handmade | n2 | contradiction | entailment | 0.939 | The default backoff_factor of Retry is 0.5. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0025 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0047 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0056 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0022 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.0646 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0021 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0043 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0032 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.01 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0024 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0081 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0097 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.003 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.006 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0024 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0058 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0031 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0081 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0025 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0047 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0053 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0063 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.2617 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.1442 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0028 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0024 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0113 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.014 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0021 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.016 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0032 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-xsmall | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0075 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0023 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0081 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0087 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0104 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0035 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0032 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0058 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.007 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0024 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0219 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0029 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-xsmall | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0069 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0345 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0071 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0169 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.1204 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.15 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0816 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.2944 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.3429 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.035 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.3319 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.4338 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.2362 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.7185 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.2662 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.3794 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.1931 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.3992 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.3707 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.0312 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0261 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0068 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0958 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.3261 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.3879 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0963 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.2309 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.034 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0535 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.1133 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9696 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0103 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | window | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0078 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.3773 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.223 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.1936 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | none | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9481 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0012 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0023 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0068 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0045 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0211 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0676 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0045 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0012 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0023 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0068 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0045 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0211 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0676 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0045 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c5 | entailment | neutral | 0.343 | There is no delay before the second attempt (the first retry) in Retry. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c5 | entailment | neutral | 0.343 | There is no delay before the second attempt (the first retry) in Retry. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0013 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0055 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0043 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0086 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0093 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0031 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0218 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0022 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0111 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0013 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0055 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0043 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0086 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0093 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0031 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0218 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0022 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0111 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8166 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8166 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0012 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0065 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0033 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.2991 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0026 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0072 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0051 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0205 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0012 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0065 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0033 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.2991 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0026 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0072 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0051 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0205 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.001 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0133 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0079 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0048 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.002 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0251 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0755 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0027 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0614 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0051 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-xsmall | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0173 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.001 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0133 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0079 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0048 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.002 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0251 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0755 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0027 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0614 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0051 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-xsmall | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0173 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-3.6-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-3.6-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0011 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0014 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0017 | A Retry instance can be used for more granular control of retries in urllib3. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0049 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0024 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0021 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-3.6-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-3.6-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0011 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0014 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0017 | A Retry instance can be used for more granular control of retries in urllib3. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0049 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0024 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0021 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-lite-3.6-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-lite-3.6-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0023 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0028 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0014 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0416 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0029 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.004 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-lite-3.6-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-lite-3.6-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0023 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0028 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0014 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0416 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0029 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.004 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | haiku-high | c5 | entailment | neutral | 0.3316 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0015 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0015 | A Retry instance gives more granular control over retries in urllib3. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | haiku-high | c5 | entailment | neutral | 0.3316 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0015 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0015 | A Retry instance gives more granular control over retries in urllib3. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0018 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0013 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.002 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.002 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c11 | entailment | neutral | 0.0033 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.1687 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.2507 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.0215 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0016 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.003 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0075 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0018 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0013 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.002 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.002 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c11 | entailment | neutral | 0.0033 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.1687 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.2507 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.0215 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0016 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.003 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0075 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | sonnet-medium | c5 | entailment | neutral | 0.3316 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0017 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0023 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0023 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0186 | The urllib3 Retry class allows far greater control of how requests are retried. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0025 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | local | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0039 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | sonnet-medium | c5 | entailment | neutral | 0.3316 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0017 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0023 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0023 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0186 | The urllib3 Retry class allows far greater control of how requests are retried. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0025 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | local | 400 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0039 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0012 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0023 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0042 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0029 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0187 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0234 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0029 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0012 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0023 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0068 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0033 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0072 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0142 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0027 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c1 | entailment | neutral | 0.1501 | By default, Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c2 | entailment | neutral | 0.3113 | The default backoff_factor value for Retry is 0. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0521 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c5 | entailment | neutral | 0.343 | There is no delay before the second attempt (the first retry) in Retry. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c5 | entailment | neutral | 0.343 | There is no delay before the second attempt (the first retry) in Retry. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0086 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0306 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.2338 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0013 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0035 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c4 | entailment | neutral | 0.0622 | In production systems, retrying immediately without backoff can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c5 | entailment | neutral | 0.1168 | In production systems, retrying immediately without backoff can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0036 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0071 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0079 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0028 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0076 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0017 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0044 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0013 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0055 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0043 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0086 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0051 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0031 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0055 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0022 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0048 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.4501 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0012 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0056 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0022 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.0646 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0021 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0043 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0032 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.01 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0012 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0065 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.003 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.006 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0024 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0058 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0031 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0081 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.001 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0053 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0063 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.2617 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.1442 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0028 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.002 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0113 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.014 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0021 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.016 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0032 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-xsmall | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0075 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.001 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0037 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0087 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0079 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0035 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.002 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0058 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.007 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0024 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0219 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0029 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-xsmall | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0069 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-3.6-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-3.6-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0011 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0014 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0017 | A Retry instance can be used for more granular control of retries in urllib3. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0049 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0024 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0021 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-3.6-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-3.6-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0011 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0014 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0017 | A Retry instance can be used for more granular control of retries in urllib3. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0049 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0024 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0021 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-lite-3.6-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-lite-3.6-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0023 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0028 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0014 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0416 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0029 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.004 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-lite-3.6-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-lite-3.6-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0023 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0028 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0014 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0416 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0029 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.004 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | haiku-high | c5 | entailment | neutral | 0.3316 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.2944 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0015 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.035 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0015 | A Retry instance gives more granular control over retries in urllib3. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | haiku-high | c5 | entailment | neutral | 0.3316 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.3319 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0015 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.2362 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0015 | A Retry instance gives more granular control over retries in urllib3. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.2662 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0018 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0013 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.002 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.002 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c11 | entailment | neutral | 0.0033 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.1687 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.2507 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.0215 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0016 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.003 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0075 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c4 | entailment | neutral | 0.0154 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c5 | entailment | neutral | 0.1009 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.3261 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0018 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0013 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.002 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.002 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c11 | entailment | neutral | 0.0033 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.1687 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.2507 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.0215 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0016 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.003 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0075 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | sonnet-medium | c5 | entailment | neutral | 0.3316 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.2309 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0017 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0023 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0023 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0186 | The urllib3 Retry class allows far greater control of how requests are retried. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0025 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | both | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0039 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | sonnet-medium | c5 | entailment | neutral | 0.3316 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.3773 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0017 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0023 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0023 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0186 | The urllib3 Retry class allows far greater control of how requests are retried. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0025 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | both | 400 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0039 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.2447 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c1 | entailment | neutral | 0.4527 | By default, Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c2 | entailment | neutral | 0.4553 | The default backoff_factor value for Retry is 0. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.1388 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.3273 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0205 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0513 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.3714 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.4322 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.1326 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c4 | entailment | neutral | 0.1864 | In production systems, retrying immediately without backoff can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c5 | entailment | neutral | 0.2917 | In production systems, retrying immediately without backoff can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3735 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.5827 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.398 | Retrying immediately without backoff is recommended for production systems. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n2 | contradiction | entailment | 0.939 | The default backoff_factor of Retry is 0.5. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.5288 | Retrying immediately without backoff is recommended for production systems. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.147 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.1873 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.3866 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.064 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.2032 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.3731 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.298 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.1773 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | contradiction | 0.256 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.409 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.3361 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.1757 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.3765 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.4843 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0863 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.3548 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.4465 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.2799 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.6832 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.3794 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.3032 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.4115 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.3814 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.4335 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.1343 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.3417 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0591 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0892 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.1897 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.963 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.4348 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.2294 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.1942 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9468 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.292 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.292 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8188 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.8166 | Retrying immediately without backoff is recommended for production systems. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8188 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.8166 | Retrying immediately without backoff is recommended for production systems. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.1436 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.1436 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.2179 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | contradiction | 0.2558 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.2179 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | contradiction | 0.2558 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | haiku-high | c5 | entailment | neutral | 0.2983 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | haiku-high | c5 | entailment | neutral | 0.2983 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.8442 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.8442 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | opus-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | opus-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | opus-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | opus-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c5 | entailment | neutral | 0.2983 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.6792 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c5 | entailment | neutral | 0.2983 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.6792 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.2447 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c1 | entailment | neutral | 0.4527 | By default, Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c2 | entailment | neutral | 0.4553 | The default backoff_factor value for Retry is 0. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.1388 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.3273 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0205 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0513 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.3714 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.4322 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.1326 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c4 | entailment | neutral | 0.1864 | In production systems, retrying immediately without backoff can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c5 | entailment | neutral | 0.2917 | In production systems, retrying immediately without backoff can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.292 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.292 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3735 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.5827 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.398 | Retrying immediately without backoff is recommended for production systems. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.5288 | Retrying immediately without backoff is recommended for production systems. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.1436 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.1436 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.1873 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.3866 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.064 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.2032 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.3731 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.298 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.1773 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | contradiction | 0.2558 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.409 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.3361 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.2179 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.1757 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | contradiction | 0.2558 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | flash-3.6-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | flash-3.6-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | flash-lite-3.6-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | flash-lite-3.6-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | haiku-high | c5 | entailment | neutral | 0.2983 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.3765 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.4843 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0863 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | haiku-high | c5 | entailment | neutral | 0.2983 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.3548 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.4465 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.2799 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.6832 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | opus-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | opus-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.3794 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.3032 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.4115 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | opus-high | c4 | entailment | neutral | 0.0424 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | opus-high | c5 | entailment | neutral | 0.0768 | By default, urllib3 will follow up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.3814 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.4335 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.1343 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c5 | entailment | neutral | 0.2983 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.3417 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0591 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0892 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.1897 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.6792 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c5 | entailment | neutral | 0.2983 | By default, urllib3 follows up to 3 redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.4348 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.2294 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.1942 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.6792 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0006 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0006 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0002 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0008 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0015 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0046 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0002 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0008 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0012 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0009 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.001 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0021 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0015 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0003 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0005 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0739 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0007 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0015 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.0084 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0007 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0004 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.001 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0027 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.001 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0005 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0003 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0002 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0002 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0009 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0008 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0012 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0011 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0046 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0027 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0007 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0007 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0003 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0006 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.7011 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0006 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0105 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0005 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.176 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0019 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0002 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0006 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0008 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0007 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0237 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0006 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.0053 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.001 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0003 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0006 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0008 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0008 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0003 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.0428 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0008 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0008 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0005 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0005 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0012 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0003 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0005 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0014 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0007 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0025 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0016 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0012 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.001 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0006 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0004 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0004 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.001 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0003 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0009 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0012 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0035 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0025 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0015 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0003 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0062 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0008 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0023 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0066 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0092 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0027 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0051 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0005 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0059 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0012 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | haiku-high | c11 | entailment | neutral | 0.0135 | urllib3 can be configured to disable exceptions for too many redirects and return the 302 response. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0007 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0024 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.003 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0004 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0132 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0112 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0006 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.0165 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.0109 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0021 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0058 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0128 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0006 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0036 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0127 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0011 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0012 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0239 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.002 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0059 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9974 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | sonnet-medium | c12 | entailment (borderline) | neutral | 0.0062 | A urllib3 Retry instance can be used to do a total of 3 retries while limiting redirects to only 2. |
| nli-deberta-v3-base | none | window | 128 | retrying-requests | sonnet-medium | c13 | entailment | neutral | 0.014 | urllib3 can be configured to not raise exceptions for too many redirects and instead return the 302 response. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | sonnet-medium | c3 | entailment | neutral | 0.0063 | The retries parameter of urllib3's request() controls retries. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0008 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0014 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0007 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | none | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9974 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0005 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0008 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0005 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0005 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0011 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0057 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0003 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0005 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0008 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0005 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0005 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0011 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0057 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0003 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0469 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0469 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0008 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0008 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0005 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0014 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0007 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0005 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0007 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0003 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0003 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0008 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0008 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0005 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0014 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0007 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0005 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0007 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0003 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0003 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.6758 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.6758 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0005 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0005 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0015 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0003 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.016 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0025 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0004 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0009 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0005 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0005 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0015 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0003 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.016 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0025 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0004 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0009 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0009 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0005 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0013 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0007 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0005 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0004 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0012 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0073 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0004 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0029 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0004 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0007 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0009 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0005 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0013 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0007 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0005 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0004 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0012 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0073 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0004 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0029 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0004 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0007 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0002 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0002 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0003 | A Retry instance can be used for more granular control of retries in urllib3. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0018 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0003 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0047 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0002 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0002 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0003 | A Retry instance can be used for more granular control of retries in urllib3. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0018 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0003 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0047 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0005 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0009 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0003 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0118 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0023 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.006 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0005 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0009 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0003 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0118 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0023 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.006 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0003 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0031 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0003 | A Retry instance gives more granular control over retries in urllib3. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0003 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0031 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0003 | A Retry instance gives more granular control over retries in urllib3. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0653 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0005 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0004 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0006 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c11 | entailment | neutral | 0.0008 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.0081 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0024 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0094 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0055 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0653 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0005 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0004 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0006 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c11 | entailment | neutral | 0.0008 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.0081 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0024 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0094 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0055 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.2369 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0003 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0006 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0003 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0004 | The urllib3 Retry class allows far greater control of how requests are retried. |
| nli-deberta-v3-base | none | local | 128 | retrying-requests | sonnet-medium | c12 | entailment (borderline) | neutral | 0.0036 | A urllib3 Retry instance can be used to do a total of 3 retries while limiting redirects to only 2. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.2369 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0003 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0006 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0003 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0004 | The urllib3 Retry class allows far greater control of how requests are retried. |
| nli-deberta-v3-base | none | local | 400 | retrying-requests | sonnet-medium | c12 | entailment (borderline) | neutral | 0.0036 | A urllib3 Retry instance can be used to do a total of 3 retries while limiting redirects to only 2. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0005 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0006 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0002 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0005 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0011 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0046 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0002 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0005 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0008 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0005 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0005 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0011 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0015 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0003 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0005 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0469 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0007 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0015 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.0084 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0007 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0004 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0005 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0014 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0007 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0005 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0003 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0002 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0002 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0008 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0008 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0005 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0014 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0007 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0005 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0007 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0003 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0003 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.6758 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0005 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0015 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0003 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.016 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0019 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0002 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0006 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0005 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0005 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0015 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0003 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.0053 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.001 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0003 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0006 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0008 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0008 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0003 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.0428 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0005 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0004 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0005 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0005 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0012 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0003 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0005 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0009 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0005 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0013 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0007 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0005 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0004 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0006 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0004 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0004 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.001 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0003 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0007 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0012 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0002 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0002 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0003 | A Retry instance can be used for more granular control of retries in urllib3. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0015 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0003 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0047 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0008 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0002 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0002 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0003 | A Retry instance can be used for more granular control of retries in urllib3. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0018 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0003 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0047 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0005 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0009 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0003 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0092 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0023 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0051 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0005 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0009 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0003 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0118 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0023 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.006 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0005 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0003 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0012 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0003 | A Retry instance gives more granular control over retries in urllib3. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | haiku-high | c11 | entailment | neutral | 0.0135 | urllib3 can be configured to disable exceptions for too many redirects and return the 302 response. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0007 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0003 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.003 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0003 | A Retry instance gives more granular control over retries in urllib3. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0004 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0005 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0004 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c11 | entailment | neutral | 0.0008 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.0081 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.0109 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0021 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0058 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0055 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0006 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0005 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0004 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0006 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c11 | entailment | neutral | 0.0008 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.0081 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0024 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0094 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0055 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.002 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0003 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0003 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0004 | The urllib3 Retry class allows far greater control of how requests are retried. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | sonnet-medium | c12 | entailment (borderline) | neutral | 0.0036 | A urllib3 Retry instance can be used to do a total of 3 retries while limiting redirects to only 2. |
| nli-deberta-v3-base | none | both | 128 | retrying-requests | sonnet-medium | c13 | entailment | neutral | 0.014 | urllib3 can be configured to not raise exceptions for too many redirects and instead return the 302 response. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | sonnet-medium | c3 | entailment | neutral | 0.0063 | The retries parameter of urllib3's request() controls retries. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0008 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0003 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0006 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0003 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0004 | The urllib3 Retry class allows far greater control of how requests are retried. |
| nli-deberta-v3-base | none | both | 400 | retrying-requests | sonnet-medium | c12 | entailment (borderline) | neutral | 0.0036 | A urllib3 Retry instance can be used to do a total of 3 retries while limiting redirects to only 2. |
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
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0209 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0209 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.011 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0169 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.011 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0169 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.7985 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.7985 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
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
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.004 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.4431 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0287 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.1832 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.3525 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0079 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0075 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0232 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.3404 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0113 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.1405 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.3027 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0934 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0108 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0199 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0064 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0116 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3528 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0209 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.2582 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.5176 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.89 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.004 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0965 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0108 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.1025 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0126 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.2692 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0075 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0178 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0167 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.008 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.307 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0286 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0204 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0532 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0567 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0157 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0471 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.008 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0215 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.025 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0533 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0995 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.014 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.3868 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0253 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0274 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.1482 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.4312 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0366 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0582 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.7465 | Specifying redirect=False disables the retrying logic of urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.2724 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.045 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9608 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.306 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9888 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0022 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0443 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0115 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0147 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.3264 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0163 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0022 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0443 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0115 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0147 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.3264 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0163 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0083 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.2286 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.075 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0171 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.268 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0378 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0122 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0737 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0122 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0158 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0083 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.2286 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.075 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0171 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.268 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0378 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0122 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0737 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0122 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0158 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0022 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.1444 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.147 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0137 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0096 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.2088 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0235 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.2211 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0022 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.1444 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.147 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0137 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0096 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.2088 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0235 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.2211 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0267 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.1444 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.1141 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0242 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0114 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.4187 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0143 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.409 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0107 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0245 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0267 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.1444 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.1141 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0242 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0114 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.4187 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0143 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.409 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0107 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0245 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0027 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.002 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0066 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0164 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0131 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.011 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0027 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.002 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0066 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0164 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0131 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.011 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0048 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0048 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0074 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.1139 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0079 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0125 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0048 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0048 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0074 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.1139 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0079 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0125 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0039 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0118 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0055 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0039 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0118 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0055 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0064 | Specifying retries=False in urllib3 disables all retry logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0049 | Specifying retries=False in urllib3 disables all redirect logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0054 | Specifying redirect=False in urllib3 disables redirects. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.003 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | opus-high | c11 | entailment | neutral | 0.018 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.1063 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0181 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.1089 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0064 | Specifying retries=False in urllib3 disables all retry logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0049 | Specifying retries=False in urllib3 disables all redirect logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0054 | Specifying redirect=False in urllib3 disables redirects. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.003 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | opus-high | c11 | entailment | neutral | 0.018 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | opus-high | c15 | entailment | neutral | 0.1063 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0181 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | opus-high | c17 | entailment | neutral | 0.1089 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0126 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0156 | Specifying redirect=False in urllib3's request() disables redirects. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0095 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.011 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.2809 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0387 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0126 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0156 | Specifying redirect=False in urllib3's request() disables redirects. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0095 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.011 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.2809 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-base-mnli-fever-anli | none | local | 400 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0387 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0022 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0443 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0115 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0147 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.1832 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.3525 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0079 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0022 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0443 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0115 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0147 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.3264 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.3404 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0113 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0083 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.2286 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.075 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0171 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.268 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0378 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0108 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0199 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0064 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0116 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0083 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.2286 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.075 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0171 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.268 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0378 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0122 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0737 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0122 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0158 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0022 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.1444 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.147 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0137 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0096 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.1025 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0126 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.2211 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0022 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.1444 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.147 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0137 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0096 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.2088 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.008 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.2211 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0267 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.1444 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.1141 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0242 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0114 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0532 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0567 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0143 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0471 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.008 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0215 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0267 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.1444 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.1141 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0242 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0114 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.4187 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0533 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0143 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.409 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0107 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0245 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0027 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.002 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0066 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0164 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0131 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.011 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0027 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.002 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0066 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0164 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0131 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.011 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0048 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0048 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0074 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.1139 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0079 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0125 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0048 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0048 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0074 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.1139 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0079 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0125 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0039 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0118 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0055 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0039 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0118 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0055 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0064 | Specifying retries=False in urllib3 disables all retry logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0049 | Specifying retries=False in urllib3 disables all redirect logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0054 | Specifying redirect=False in urllib3 disables redirects. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.003 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | opus-high | c11 | entailment | neutral | 0.018 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.1063 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0181 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.1089 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0064 | Specifying retries=False in urllib3 disables all retry logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0049 | Specifying retries=False in urllib3 disables all redirect logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0054 | Specifying redirect=False in urllib3 disables redirects. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.003 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | opus-high | c11 | entailment | neutral | 0.018 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | opus-high | c15 | entailment | neutral | 0.1063 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0181 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | opus-high | c17 | entailment | neutral | 0.1089 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0126 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0156 | Specifying redirect=False in urllib3's request() disables redirects. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0095 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.011 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.2809 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0387 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0126 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0156 | Specifying redirect=False in urllib3's request() disables redirects. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0095 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.011 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.2809 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-base-mnli-fever-anli | none | both | 400 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0387 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.4451 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8055 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.9405 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.7512 | Specifying redirect=False disables the retrying logic of urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9776 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9917 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.4268 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.4268 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8964 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8964 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9906 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9906 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.4268 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.4451 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.4268 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8055 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.8964 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9776 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | both | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9906 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0241 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.1554 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0208 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.1255 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0421 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0009 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.4702 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0343 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.3692 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0102 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.2109 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0026 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0034 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0015 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.3455 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.2745 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9836 | With exponential backoff, Retry waits before the second attempt. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0241 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0093 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0008 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0038 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0021 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0128 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.4702 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.004 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.002 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.3534 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.1254 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0515 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0025 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0071 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.1853 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0011 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.025 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0018 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.1002 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.01 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0206 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0039 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.3396 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0411 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.001 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0023 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0827 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0162 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0078 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0077 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | haiku-high | c11 | entailment | neutral | 0.0351 | urllib3 can be configured to disable exceptions for too many redirects and return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.8196 | Specifying redirect=False disables the retrying logic of urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0139 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0064 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9983 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | sonnet-medium | c13 | entailment | neutral | 0.0686 | urllib3 can be configured to not raise exceptions for too many redirects and instead return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0759 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.2846 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9992 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0078 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0087 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0044 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0071 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.2587 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.001 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0078 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0087 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0044 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0071 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.2587 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.001 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0416 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0517 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0016 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3575 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0694 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0016 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.458 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0416 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0517 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0016 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3575 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0694 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0016 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.458 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.5706 | With exponential backoff, Retry waits before the second attempt. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.5706 | With exponential backoff, Retry waits before the second attempt. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0078 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0476 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0222 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.001 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.2718 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.1638 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0016 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0088 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0078 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0476 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0222 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.001 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.2718 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.1638 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0016 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0088 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.101 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0476 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0102 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0029 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0295 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0642 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.281 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.3559 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0018 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.101 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0476 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0102 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0029 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0295 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0642 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.281 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.3559 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0018 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0006 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0003 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0004 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0009 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0021 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0042 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0006 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0003 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0004 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0009 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0021 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0042 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0009 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0052 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0009 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0073 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0059 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0064 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0009 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0052 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0009 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0073 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0059 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0064 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0007 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0269 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0004 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | haiku-high | c11 | entailment | neutral | 0.0254 | urllib3 can be configured to disable exceptions for too many redirects and return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0007 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0269 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0004 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | haiku-high | c11 | entailment | neutral | 0.0254 | urllib3 can be configured to disable exceptions for too many redirects and return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0016 | Specifying retries=False in urllib3 disables all retry logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0012 | Specifying retries=False in urllib3 disables all redirect logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0008 | Specifying redirect=False in urllib3 disables redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0007 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | c11 | entailment | neutral | 0.004 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.3917 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0289 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0046 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0166 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0016 | Specifying retries=False in urllib3 disables all retry logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0012 | Specifying retries=False in urllib3 disables all redirect logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0008 | Specifying redirect=False in urllib3 disables redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0007 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | c11 | entailment | neutral | 0.004 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.3917 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0289 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0046 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0166 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0026 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0011 | Specifying redirect=False in urllib3's request() disables redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0018 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | sonnet-medium | c13 | entailment | neutral | 0.0584 | urllib3 can be configured to not raise exceptions for too many redirects and instead return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0147 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0035 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0026 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0011 | Specifying redirect=False in urllib3's request() disables redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0018 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | sonnet-medium | c13 | entailment | neutral | 0.0584 | urllib3 can be configured to not raise exceptions for too many redirects and instead return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0147 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | local | 400 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0035 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0078 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0087 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0044 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0071 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0421 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0009 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0078 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0087 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0044 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0071 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.2587 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.001 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0416 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0517 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0016 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0026 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0034 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0015 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.3455 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0416 | By default, urllib3's Retry class does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0517 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0016 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.2745 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0694 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0016 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.458 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.5706 | With exponential backoff, Retry waits before the second attempt. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0078 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0476 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0222 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.001 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0008 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0038 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0016 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0088 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0078 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0476 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0222 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.001 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.002 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.1638 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0016 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0088 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.101 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0476 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0102 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0029 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0025 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0071 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.1853 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0011 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.025 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0018 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.101 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0476 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0102 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0029 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0295 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.01 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0206 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0039 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.3396 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0018 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0006 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0003 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0004 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0009 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0021 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0042 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0006 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0003 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-3.6-high | c9 | entailment | neutral | 0.0004 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0009 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0021 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0042 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0009 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0052 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0009 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0073 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0059 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0064 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c7 | entailment | neutral | 0.0009 | All retry and redirect logic in urllib3 can be disabled by specifying retries=False. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c8 | entailment | neutral | 0.0052 | Redirects in urllib3 can be disabled while keeping the retrying logic by specifying redirect=False. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c9 | entailment | neutral | 0.0009 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0073 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0059 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0064 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0007 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0269 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0004 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | haiku-high | c11 | entailment | neutral | 0.0254 | urllib3 can be configured to disable exceptions for too many redirects and return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0007 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0269 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | haiku-high | c9 | entailment | neutral | 0.0004 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | haiku-high | c11 | entailment | neutral | 0.0254 | urllib3 can be configured to disable exceptions for too many redirects and return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0016 | Specifying retries=False in urllib3 disables all retry logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0012 | Specifying retries=False in urllib3 disables all redirect logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0008 | Specifying redirect=False in urllib3 disables redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0007 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | c11 | entailment | neutral | 0.004 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.3917 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0139 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0046 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0166 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0016 | Specifying retries=False in urllib3 disables all retry logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0012 | Specifying retries=False in urllib3 disables all redirect logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0008 | Specifying redirect=False in urllib3 disables redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0007 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | c11 | entailment | neutral | 0.004 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.3917 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0289 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0046 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0166 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0026 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0011 | Specifying redirect=False in urllib3's request() disables redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0018 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | sonnet-medium | c13 | entailment | neutral | 0.0584 | urllib3 can be configured to not raise exceptions for too many redirects and instead return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0147 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0035 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0026 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0011 | Specifying redirect=False in urllib3's request() disables redirects. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | sonnet-medium | c11 | entailment | neutral | 0.0018 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | sonnet-medium | c13 | entailment | neutral | 0.0584 | urllib3 can be configured to not raise exceptions for too many redirects and instead return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0147 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | both | 400 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0035 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3038 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0217 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9882 | With exponential backoff, Retry waits before the second attempt. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.6964 | Specifying redirect=False disables the retrying logic of urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9965 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | window | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9991 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.3904 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0946 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1422 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.3904 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0946 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1422 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.3904 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0946 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0217 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.3904 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0946 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | both | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1422 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
