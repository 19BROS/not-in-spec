# Run 001-baseline

- note: window only; 3 models; labels + handmade negatives
- started: `2026-11-07T13:12:05`
- models: `['cross-encoder/nli-deberta-v3-xsmall', 'cross-encoder/nli-deberta-v3-base', 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli']`
- contexts: `['none']`
- sections: `all`
- batch: `16`
- git: `{'commit': 'e8077b00a58fcaac2cbebef8f3f9dc7762970048', 'branch': 'feat/nli-and-extractors-testing', 'dirty_experiment_files': True}`
- inputs: `{'pairs_sha256': '670259280e9d', 'labels_sha256': '0da00b1e7a82'}`
- versions: `{'python': '3.12.10', 'torch': '2.15.0+cpu', 'transformers': '5.22.2'}`
- seconds: `{'cross-encoder/nli-deberta-v3-xsmall': {'none': 32.1}, 'cross-encoder/nli-deberta-v3-base': {'none': 81.7}, 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli': {'none': 2083.7}}`
- finished: `2026-11-07T13:50:56`

## Metrics vs labels.csv (139 labelled claims, annotator: claude-draft)

Keep = NLI says entailment (claim survives grounding). Dropped by the citation check = not kept. `nb` = without borderline labels.

| model | context | win | n | keep acc | keep recall | keep precision | false keeps | contra recall | keep acc nb |
|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | none | 128 | 139 | 49% | 42% | 96% | 2 | 71% | 49% |
| nli-deberta-v3-xsmall | none | 400 | 139 | 62% | 58% | 96% | 3 | 71% | 62% |
| nli-deberta-v3-base | none | 128 | 139 | 49% | 42% | 96% | 2 | 71% | 50% |
| nli-deberta-v3-base | none | 400 | 139 | 57% | 50% | 98% | 1 | 71% | 56% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | 139 | 73% | 69% | 99% | 1 | 100% | 72% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | 139 | 87% | 87% | 97% | 3 | 86% | 87% |

## Labels per extractor

| model | context | win | section | extractor | ent | neu | con | dropped |
|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 5 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | 0 | 12 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | 0 | 14 | 0 | 1 |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | flash-lite-3.6-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | 8 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | sonnet-medium | 9 | 6 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 5 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | opus-high | 14 | 3 | 0 | 0 |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | sonnet-medium | 12 | 3 | 0 | 0 |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 7 | 1 | 0 | 0 |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 3 | 5 | 0 |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | 1 | 13 | 0 | 1 |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-3.6-high | 6 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-lite-3.6-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | none | 128 | retrying-requests | haiku-high | 9 | 4 | 0 | 0 |
| nli-deberta-v3-base | none | 128 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | 7 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | 128 | retrying-requests | sonnet-medium | 9 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-3.6-high | 0 | 7 | 0 | 0 |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 4 | 4 | 0 | 0 |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | 2 | 10 | 0 | 0 |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | 0 | 9 | 0 | 0 |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | 2 | 12 | 0 | 1 |
| nli-deberta-v3-base | none | 400 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| nli-deberta-v3-base | none | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| nli-deberta-v3-base | none | 400 | retrying-requests | haiku-high | 10 | 3 | 0 | 0 |
| nli-deberta-v3-base | none | 400 | retrying-requests | negatives-handmade | 0 | 4 | 5 | 0 |
| nli-deberta-v3-base | none | 400 | retrying-requests | opus-high | 11 | 6 | 0 | 0 |
| nli-deberta-v3-base | none | 400 | retrying-requests | sonnet-medium | 10 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | flash-3.6-high | 1 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | haiku-high | 7 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | opus-high | 3 | 6 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | sonnet-medium | 6 | 8 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | flash-3.6-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | flash-lite-3.6-high | 10 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | opus-high | 15 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | sonnet-medium | 12 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | flash-3.6-high | 3 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | haiku-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | opus-high | 5 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | sonnet-medium | 8 | 6 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |

## Wrong keep / drop decisions

| model | context | win | section | extractor | id | gold | NLI | p_ent | claim |
|---|---|---|---|---|---|---|---|---|---|
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0025 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0027 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0042 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0029 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0187 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0234 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0029 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0024 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0039 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0079 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0033 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0072 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0142 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0027 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c1 | entailment | neutral | 0.1501 | By default, Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c2 | entailment | neutral | 0.3113 | The default backoff_factor value for Retry is 0. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0521 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0086 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0306 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.2338 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0023 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0047 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0035 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c4 | entailment | neutral | 0.0622 | In production systems, retrying immediately without backoff can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c5 | entailment | neutral | 0.1168 | In production systems, retrying immediately without backoff can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0036 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0071 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0079 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0028 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0076 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0017 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0044 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0023 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0068 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0074 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0052 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0094 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0051 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0034 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0055 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0025 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0048 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.4501 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | negatives-handmade | n2 | contradiction | entailment | 0.939 | The default backoff_factor of Retry is 0.5. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0025 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0047 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0056 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0022 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.0646 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0021 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0043 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0032 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.01 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0024 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0081 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0097 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.003 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.006 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0024 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0058 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0031 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0081 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0025 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0047 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0053 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0063 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c5 | entailment | neutral | 0.2617 | Retrying immediately without backoff in production systems can overwhelm a recovering server. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.1442 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0028 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0024 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0113 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.014 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0021 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.016 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0032 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-xsmall | none | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0075 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0023 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0081 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0087 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0104 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0035 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0032 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0058 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.007 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0024 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0219 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0029 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-xsmall | none | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0069 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0345 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0071 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0169 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.1204 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.15 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0816 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.2944 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.3429 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.035 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.3319 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.4338 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.2362 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.7185 | Specifying redirect=False disables the retrying logic of urllib3. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.2662 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.3794 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.1931 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.3992 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.3707 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.0312 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0261 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0068 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0958 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.3261 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | opus-high | c14 | entailment (borderline) | neutral | 0.3879 | When a urllib3 Retry instance disables exceptions for too many redirects, urllib3 just returns the 302 response. |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0963 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.2309 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.034 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0535 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.1133 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9696 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0103 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| nli-deberta-v3-xsmall | none | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.0078 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.3773 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.223 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.1936 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-xsmall | none | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9481 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0006 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0006 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0002 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.0008 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0015 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0046 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0002 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0008 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.0012 | The default backoff_factor setting in urllib3's Retry is 0. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0009 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.001 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0021 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-3.6-high | c6 | entailment | neutral | 0.0015 | Exponential backoff sleep delays in urllib3's Retry are capped up to backoff_max. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0003 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0005 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c3 | entailment | neutral | 0.0739 | Retry respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c6 | entailment | neutral | 0.0007 | A backoff_factor of 0.5 yields retry sleeps of 0.0s, 1.0s, 2.0s, etc., up to backoff_max. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c7 | entailment | neutral | 0.0015 | Adding backoff_jitter introduces random variance. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | flash-lite-3.6-high | c8 | entailment | neutral | 0.0084 | backoff_jitter avoids the "thundering herd" problem where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0007 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0004 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.001 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0027 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.001 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0005 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0003 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0002 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0002 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c1 | entailment | neutral | 0.0009 | By default, urllib3's Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c2 | entailment | neutral | 0.0008 | The default value of the backoff_factor parameter of urllib3's Retry class is 0. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c3 | entailment | neutral | 0.0012 | urllib3's Retry class will still respect delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.0011 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c7 | entailment | neutral | 0.0046 | The sleep delay between retries in urllib3's Retry class, when backoff is used, is measured in seconds. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c8 | entailment | neutral | 0.0027 | With urllib3's Retry class, there is no delay before the second attempt, which is the first retry. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0007 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0007 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0003 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.0006 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | negatives-handmade | n4 | contradiction | entailment | 0.7011 | A backoff_factor of 0.5 yields retry sleeps of 0.5s, 1.0s, 2.0s. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0006 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0105 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0005 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.176 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0019 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0002 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0006 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0008 | By default, urllib3's Retry does not sleep between retry attempts. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | c2 | entailment | neutral | 0.0007 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | c3 | entailment | neutral | 0.0237 | With the default backoff_factor of 0, urllib3's Retry still respects delays requested by the server when a response includes a Retry-After header. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0006 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | c5 | entailment | neutral | 0.0053 | With a non-zero backoff_factor, urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.001 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0003 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0006 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0008 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0004 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0008 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0003 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c6 | entailment | neutral | 0.0428 | Retrying immediately without backoff in production systems can quickly exhaust API rate limits. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0008 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0008 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0005 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0005 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0003 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0012 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0003 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | none | 128 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0005 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c1 | entailment | neutral | 0.0014 | By default, the urllib3 Retry class does not sleep between retry attempts. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c2 | entailment | neutral | 0.0007 | The default value of the backoff_factor parameter of urllib3's Retry is 0. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.0025 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c4 | entailment (borderline) | neutral | 0.0016 | The respect_retry_after_header parameter of urllib3's Retry relates to respecting server-requested delays given in a Retry-After header. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0012 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.001 | The sleep delay in urllib3's Retry is calculated in seconds. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0006 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0004 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0004 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.001 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0003 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| nli-deberta-v3-base | none | 400 | configuring-exponential-backoff | sonnet-medium | c15 | entailment | neutral | 0.0009 | The backoff_jitter parameter of urllib3's Retry helps avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0012 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0035 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0025 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.0015 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0003 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0062 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | 400 | retrying-requests | flash-3.6-high | c6 | entailment | neutral | 0.0008 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| nli-deberta-v3-base | none | 400 | retrying-requests | flash-3.6-high | c7 | entailment | neutral | 0.0023 | Specifying retries=False disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | 400 | retrying-requests | flash-3.6-high | c8 | entailment | neutral | 0.0066 | Specifying redirect=False disables redirects while keeping the retrying logic in urllib3. |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0092 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0027 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| nli-deberta-v3-base | none | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0051 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | 128 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0005 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | none | 128 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0059 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | 128 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.0012 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | none | 128 | retrying-requests | haiku-high | c11 | entailment | neutral | 0.0135 | urllib3 can be configured to disable exceptions for too many redirects and return the 302 response. |
| nli-deberta-v3-base | none | 400 | retrying-requests | haiku-high | c6 | entailment | neutral | 0.0007 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| nli-deberta-v3-base | none | 400 | retrying-requests | haiku-high | c7 | entailment | neutral | 0.0024 | Specifying retries=False for request() disables all retry and redirect logic in urllib3. |
| nli-deberta-v3-base | none | 400 | retrying-requests | haiku-high | c8 | entailment | neutral | 0.003 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0004 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0132 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0112 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0006 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c12 | entailment (borderline) | neutral | 0.0165 | A urllib3 Retry instance can be configured to do a total of 3 retries but limit to only 2 redirects. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c13 | entailment (borderline) | neutral | 0.0109 | A urllib3 Retry instance can disable exceptions for too many redirects. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.0021 | In urllib3, the retry policy can be specified at the PoolManager level. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0058 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | none | 128 | retrying-requests | opus-high | c17 | entailment | neutral | 0.0128 | A urllib3 PoolManager-level retry policy can be overridden by specifying retries to request(). |
| nli-deberta-v3-base | none | 400 | retrying-requests | opus-high | c6 | entailment | neutral | 0.0006 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | 400 | retrying-requests | opus-high | c7 | entailment | neutral | 0.0036 | Specifying retries=False in urllib3 disables all retry logic. |
| nli-deberta-v3-base | none | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.0127 | Specifying retries=False in urllib3 disables all redirect logic. |
| nli-deberta-v3-base | none | 400 | retrying-requests | opus-high | c9 | entailment | neutral | 0.0011 | Specifying redirect=False in urllib3 disables redirects. |
| nli-deberta-v3-base | none | 400 | retrying-requests | opus-high | c10 | entailment | neutral | 0.0012 | Specifying redirect=False in urllib3 keeps the retrying logic. |
| nli-deberta-v3-base | none | 400 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0239 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| nli-deberta-v3-base | none | 128 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.002 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | 128 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0059 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | none | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0004 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | none | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.0005 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | none | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9974 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| nli-deberta-v3-base | none | 128 | retrying-requests | sonnet-medium | c12 | entailment (borderline) | neutral | 0.0062 | A urllib3 Retry instance can be used to do a total of 3 retries while limiting redirects to only 2. |
| nli-deberta-v3-base | none | 128 | retrying-requests | sonnet-medium | c13 | entailment | neutral | 0.014 | urllib3 can be configured to not raise exceptions for too many redirects and instead return the 302 response. |
| nli-deberta-v3-base | none | 400 | retrying-requests | sonnet-medium | c3 | entailment | neutral | 0.0063 | The retries parameter of urllib3's request() controls retries. |
| nli-deberta-v3-base | none | 400 | retrying-requests | sonnet-medium | c6 | entailment | neutral | 0.0008 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| nli-deberta-v3-base | none | 400 | retrying-requests | sonnet-medium | c7 | entailment | neutral | 0.0014 | Specifying retries=False in urllib3's request() disables all retry and redirect logic. |
| nli-deberta-v3-base | none | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.0007 | Specifying redirect=False in urllib3's request() disables redirects. |
| nli-deberta-v3-base | none | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.001 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| nli-deberta-v3-base | none | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.9974 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.0242 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | flash-3.6-high | c2 | entailment | neutral | 0.1562 | The default backoff_factor setting in urllib3's Retry is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0208 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.1259 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | flash-3.6-high | c5 | entailment | neutral | 0.0424 | Exponential backoff in urllib3's Retry includes no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0009 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | flash-3.6-high | c1 | entailment | neutral | 0.4709 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | flash-3.6-high | c3 | entailment | neutral | 0.0337 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | flash-3.6-high | c4 | entailment | neutral | 0.3706 | Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | flash-3.6-high | c7 | entailment | neutral | 0.0102 | Adding backoff_jitter in urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.2113 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.0026 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.0034 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.0015 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | haiku-high | c12 | entailment | neutral | 0.3438 | The backoff_jitter parameter of urllib3's Retry class is used to avoid the thundering herd problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.2761 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | negatives-handmade | n5 | contradiction | entailment | 0.9839 | With exponential backoff, Retry waits before the second attempt. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.0242 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.0093 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.0008 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | opus-high | c7 | entailment | neutral | 0.0038 | The backoff retry sleeps of urllib3's Retry grow up to backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.0021 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | opus-high | c9 | entailment | neutral | 0.0129 | The random variance introduced by backoff_jitter in urllib3's Retry is intended to avoid the 'thundering herd' problem, where many clients retry in lockstep against a server. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | opus-high | c1 | entailment | neutral | 0.4736 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | opus-high | c4 | entailment | neutral | 0.004 | When no server-requested delay is applied, setting a non-zero backoff_factor on urllib3's Retry can introduce exponential delays between retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | opus-high | c6 | entailment | neutral | 0.002 | A backoff_factor of 0.5 on urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | opus-high | c8 | entailment | neutral | 0.3586 | Adding the backoff_jitter parameter to urllib3's Retry introduces random variance. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | sonnet-medium | c3 | entailment | neutral | 0.1251 | urllib3's Retry respects delays requested by the server when a response includes a Retry-After header, even when backoff_factor is 0. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0507 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | sonnet-medium | c9 | entailment | neutral | 0.0025 | The sleep delay in urllib3's Retry is calculated in seconds. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.0072 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.1876 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0011 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.0249 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0018 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | sonnet-medium | c7 | entailment | neutral | 0.0992 | Setting a non-zero backoff_factor on urllib3's Retry introduces exponential delays between retries when no server-requested delay is applied. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | sonnet-medium | c10 | entailment | neutral | 0.01 | urllib3's Retry applies no delay before the second attempt (the first retry). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | sonnet-medium | c11 | entailment | neutral | 0.0209 | urllib3's Retry applies no delay before the first retry because most transient errors resolve immediately. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | sonnet-medium | c12 | entailment | neutral | 0.0039 | A backoff_factor of 0.5 in urllib3's Retry yields retry sleeps of 0.0s, 1.0s, 2.0s, etc. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | sonnet-medium | c13 | entailment | neutral | 0.3401 | The retry sleep delays in urllib3's Retry are capped at backoff_max. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0406 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | flash-3.6-high | c10 | entailment | neutral | 0.001 | Exceptions for too many redirects can be disabled to return the 302 response in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | flash-3.6-high | c11 | entailment | neutral | 0.0023 | A retry policy can be specified at the PoolManager level to apply to all requests in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0831 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | flash-lite-3.6-high | c11 | entailment | neutral | 0.0161 | Exceptions for too many redirects in urllib3 can be disabled to return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | flash-lite-3.6-high | c12 | entailment | neutral | 0.0078 | All requests in urllib3 can be subjected to the same retry policy by specifying the retry at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | flash-lite-3.6-high | c13 | entailment | neutral | 0.0077 | The pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | haiku-high | c11 | entailment | neutral | 0.035 | urllib3 can be configured to disable exceptions for too many redirects and return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.8203 | Specifying redirect=False disables the retrying logic of urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | opus-high | c15 | entailment | neutral | 0.014 | In urllib3, the retry policy can be specified at the PoolManager level. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | opus-high | c16 | entailment | neutral | 0.0064 | Specifying the retry policy at the urllib3 PoolManager level makes all requests subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.998 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | sonnet-medium | c13 | entailment | neutral | 0.0692 | urllib3 can be configured to not raise exceptions for too many redirects and instead return the 302 response. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | sonnet-medium | c14 | entailment | neutral | 0.0767 | A retry policy can be specified at the urllib3 PoolManager level so that all requests are subject to the same retry policy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.2869 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.999 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
