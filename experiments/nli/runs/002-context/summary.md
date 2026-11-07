# Run 002-context

- note: project + breadcrumb in front of the window (2 variants)
- started: `2026-11-07T13:51:02`
- models: `['cross-encoder/nli-deberta-v3-xsmall', 'cross-encoder/nli-deberta-v3-base', 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli']`
- contexts: `['breadcrumb', 'sentence']`
- sections: `all`
- batch: `16`
- git: `{'commit': 'e8077b00a58fcaac2cbebef8f3f9dc7762970048', 'branch': 'feat/nli-and-extractors-testing', 'dirty_experiment_files': True}`
- inputs: `{'pairs_sha256': '670259280e9d', 'labels_sha256': '0da00b1e7a82'}`
- versions: `{'python': '3.12.10', 'torch': '2.15.0+cpu', 'transformers': '5.22.2'}`
- seconds: `{'cross-encoder/nli-deberta-v3-xsmall': {'breadcrumb': 25.2, 'sentence': 25.9}, 'cross-encoder/nli-deberta-v3-base': {'breadcrumb': 77.6, 'sentence': 79.6}, 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli': {'breadcrumb': 2165.6, 'sentence': 2307.0}}`
- finished: `2026-11-07T15:09:15`

## Metrics vs labels.csv (139 labelled claims, annotator: claude-draft)

Keep = NLI says entailment (claim survives grounding). Dropped by the citation check = not kept. `nb` = without borderline labels.

| model | context | win | n | keep acc | keep recall | keep precision | false keeps | contra recall | keep acc nb |
|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | breadcrumb | 128 | 139 | 79% | 78% | 97% | 3 | 57% | 79% |
| nli-deberta-v3-xsmall | breadcrumb | 400 | 139 | 84% | 85% | 96% | 4 | 57% | 85% |
| nli-deberta-v3-xsmall | sentence | 128 | 139 | 73% | 69% | 99% | 1 | 64% | 72% |
| nli-deberta-v3-xsmall | sentence | 400 | 139 | 69% | 66% | 96% | 3 | 57% | 69% |
| nli-deberta-v3-base | breadcrumb | 128 | 139 | 80% | 78% | 98% | 2 | 71% | 79% |
| nli-deberta-v3-base | breadcrumb | 400 | 139 | 78% | 75% | 99% | 1 | 71% | 78% |
| nli-deberta-v3-base | sentence | 128 | 139 | 78% | 76% | 98% | 2 | 71% | 78% |
| nli-deberta-v3-base | sentence | 400 | 139 | 78% | 75% | 99% | 1 | 71% | 78% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | 139 | 98% | 98% | 99% | 1 | 100% | 98% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | 139 | 98% | 100% | 98% | 3 | 86% | 98% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | 139 | 97% | 97% | 99% | 1 | 100% | 97% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | 139 | 98% | 100% | 98% | 3 | 86% | 98% |

## Labels per extractor

| model | context | win | section | extractor | ent | neu | con | dropped |
|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 5 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | 8 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | negatives-handmade | 2 | 4 | 3 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | 7 | 6 | 1 | 1 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | opus-high | 14 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | negatives-handmade | 2 | 4 | 3 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | sonnet-medium | 11 | 3 | 0 | 1 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | opus-high | 14 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | sonnet-medium | 12 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | flash-3.6-high | 4 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | haiku-high | 8 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 5 | 4 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | opus-high | 6 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | sonnet-medium | 7 | 7 | 0 | 1 |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | flash-lite-3.6-high | 12 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | opus-high | 12 | 5 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 3 | 5 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | haiku-high | 6 | 6 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 5 | 3 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | opus-high | 5 | 4 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | sonnet-medium | 8 | 6 | 0 | 1 |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | flash-3.6-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | flash-lite-3.6-high | 12 | 1 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | haiku-high | 8 | 5 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | opus-high | 11 | 6 | 0 | 0 |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | 9 | 5 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | opus-high | 12 | 5 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | opus-high | 6 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | sonnet-medium | 11 | 3 | 0 | 1 |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | opus-high | 11 | 6 | 0 | 0 |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | flash-3.6-high | 5 | 2 | 0 | 0 |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | haiku-high | 8 | 4 | 0 | 0 |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | opus-high | 8 | 1 | 0 | 0 |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | sonnet-medium | 9 | 5 | 0 | 1 |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | opus-high | 12 | 5 | 0 | 0 |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | sonnet-medium | 11 | 4 | 0 | 0 |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | flash-3.6-high | 6 | 1 | 0 | 0 |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | opus-high | 6 | 3 | 0 | 0 |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | sonnet-medium | 11 | 3 | 0 | 1 |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | opus-high | 11 | 6 | 0 | 0 |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |

## Wrong keep / drop decisions

| model | context | win | section | extractor | id | gold | NLI | p_ent | claim |
|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.2447 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c1 | entailment | neutral | 0.4527 | By default, Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c2 | entailment | neutral | 0.4553 | The default backoff_factor value for Retry is 0. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.1388 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.3273 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0205 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0513 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.3714 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.4322 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.1326 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | c4 | entailment | neutral | 0.1864 | In production systems, retrying immediately without backoff can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | c5 | entailment | neutral | 0.2917 | In production systems, retrying immediately without backoff can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3735 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.5827 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.398 | Retrying immediately without backoff is recommended for production systems. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | negatives-handmade | n2 | contradiction | entailment | 0.939 | The default backoff_factor of Retry is 0.5. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | negatives-handmade | n9 | contradiction (borderline) | entailment | 0.5288 | Retrying immediately without backoff is recommended for production systems. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.147 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.1873 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.3866 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.064 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.2032 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.3731 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.298 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.1773 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | contradiction | 0.256 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.409 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.3361 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.1757 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.3765 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.4843 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0863 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.3548 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.4465 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.2799 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.6832 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.3794 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.3032 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.4115 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.3814 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.4335 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.1343 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.3417 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0591 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0892 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.1897 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | breadcrumb | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.963 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.4348 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.2294 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.1942 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | breadcrumb | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9468 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.2946 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.1931 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.4036 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c1 | entailment | neutral | 0.2345 | By default, Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c2 | entailment | neutral | 0.2301 | The default backoff_factor value for Retry is 0. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0739 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.4123 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c2 | entailment | neutral | 0.3864 | The default backoff_factor value for Retry is 0. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.2226 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0302 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0721 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.2752 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.2564 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.1188 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | haiku-high | c4 | entailment | neutral | 0.089 | In production systems, retrying immediately without backoff can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | haiku-high | c5 | entailment | neutral | 0.165 | In production systems, retrying immediately without backoff can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.3888 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | haiku-high | c4 | entailment | neutral | 0.4209 | In production systems, retrying immediately without backoff can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | haiku-high | c5 | entailment | neutral | 0.4692 | In production systems, retrying immediately without backoff can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.279 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.4366 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.4401 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | negatives-handmade | n2 | contradiction | entailment | 0.7828 | The default backoff_factor of Retry is 0.5. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.267 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.4507 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0548 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.3675 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.2595 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.1452 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.4791 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.2954 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.267 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0668 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.1321 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.2104 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.189 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.1065 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.3675 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.3624 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.2381 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.3509 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.1664 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | sentence | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.4546 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.3161 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.227 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.2009 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | flash-3.6-high | c4 | entailment | neutral | 0.454 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.3185 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | flash-lite-3.6-high | c10 | entailment | neutral | 0.0699 | The Retry class allows far greater control of how requests are retried. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | flash-lite-3.6-high | c4 | entailment | neutral | 0.454 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.1925 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.1559 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.036 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | haiku-high | c4 | entailment | neutral | 0.4805 | By default, urllib3 retries requests 3 times. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.2525 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.255 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.1994 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | haiku-high | c13 | entailment | neutral | 0.3459 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.408 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.204 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.2138 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.1235 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.2204 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.3565 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | opus-high | c4 | entailment | neutral | 0.454 | By default, urllib3 will retry requests 3 times. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.2685 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.4163 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.3755 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.2924 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.14 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.1834 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0334 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0468 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.088 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | sentence | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.7774 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | sonnet-medium | c4 | entailment | neutral | 0.4805 | By default, urllib3 retries requests 3 times. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.2903 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.1907 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.1739 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.3678 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | sentence | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.7928 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0012 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.4994 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0006 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0374 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0007 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0008 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.0016 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0321 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0994 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0042 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0156 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0239 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8397 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0475 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0661 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0664 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.1975 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0475 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0026 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0008 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.3992 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-base | breadcrumb | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.0686 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0661 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.131 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | breadcrumb | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.3101 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0011 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0028 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0025 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0008 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0021 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0059 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0005 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0045 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0015 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0006 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0023 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0036 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0004 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0113 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0097 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0006 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0044 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0125 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0012 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0246 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0013 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0039 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9973 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | sonnet-medium | c3 | entailment | neutral | 0.0072 | The retries parameter of urllib3's request() controls retries. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0007 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0015 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0008 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | breadcrumb | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9971 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.1679 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0026 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.3911 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0008 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0477 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0009 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0015 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.0039 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0027 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | haiku-high | c5 | entailment | neutral | 0.3057 | In production systems, retrying immediately without backoff can quickly exhaust API rate limits. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0185 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0034 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0112 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0275 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.8329 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0032 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0392 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.083 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.3061 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0032 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0042 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0011 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.1468 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-base | sentence | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.0311 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0392 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0832 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | sentence | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.2893 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0013 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0025 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0021 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0009 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.002 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0051 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0007 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0037 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0021 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0008 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0019 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0042 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0005 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0181 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0286 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0007 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0007 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0037 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0117 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0012 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0013 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0209 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.002 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0049 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0006 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | sentence | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9972 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | sonnet-medium | c3 | entailment | neutral | 0.0032 | The retries parameter of urllib3's request() controls retries. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0009 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0015 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0008 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0011 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | sentence | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9966 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3008 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0216 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9883 | With exponential backoff, Retry waits before the second attempt. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.6968 | Specifying redirect=False disables the retrying logic of urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9966 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.999 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.1278 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0078 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.4429 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9805 | With exponential backoff, Retry waits before the second attempt. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.6606 | Specifying redirect=False disables the retrying logic of urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9941 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | sentence | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9985 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
