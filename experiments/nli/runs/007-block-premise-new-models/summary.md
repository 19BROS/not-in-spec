# Run 007-block-premise-new-models

- note: local-block premise (+-1 within the cited block + list lead-in) vs local; 3 newer NLI models vs run 006 winners
- started: `2026-11-08T16:04:59`
- models: `['tasksource/ModernBERT-large-nli', 'MoritzLaurer/ModernBERT-large-zeroshot-v2.0', 'MoritzLaurer/deberta-v3-large-zeroshot-v2.0', 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli', 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli']`
- contexts: `['breadcrumb']`
- premises: `['local', 'local-block']`
- radius: `1`
- sections: `all`
- batch: `8`
- git: `{'commit': '9efe448da3e514550a516cd3ba5b8353ef9e249d', 'branch': 'feat/nli-and-extractors-testing', 'dirty_experiment_files': True}`
- inputs: `{'pairs_windows_sha256': 'a13612126a3f', 'labels_sha256': '44ded39573b9'}`
- versions: `{'python': '3.12.6', 'torch': '2.15.0+cpu', 'transformers': '5.22.2'}`
- threads: `6`
- seconds: `{'tasksource/ModernBERT-large-nli': {'revision': '', 'breadcrumb/local': {'seconds': 290.7, 'scored': 571, 'unique': 571}, 'breadcrumb/local-block': {'seconds': 88.4, 'scored': 422, 'unique': 571}}, 'MoritzLaurer/ModernBERT-large-zeroshot-v2.0': {'revision': '', 'breadcrumb/local': {'seconds': 184.3, 'scored': 571, 'unique': 571}, 'breadcrumb/local-block': {'seconds': 108.2, 'scored': 422, 'unique': 571}}, 'MoritzLaurer/deberta-v3-large-zeroshot-v2.0': {'revision': '', 'breadcrumb/local': {'seconds': 234.4, 'scored': 571, 'unique': 571}, 'breadcrumb/local-block': {'seconds': 103.1, 'scored': 422, 'unique': 571}}, 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli': {'revision': '', 'breadcrumb/local': {'seconds': 192.2, 'scored': 571, 'unique': 571}, 'breadcrumb/local-block': {'seconds': 85.8, 'scored': 422, 'unique': 571}}, 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli': {'revision': '', 'breadcrumb/local': {'seconds': 60.7, 'scored': 571, 'unique': 571}, 'breadcrumb/local-block': {'seconds': 30.5, 'scored': 422, 'unique': 571}}}`
- hub_sha: `{'tasksource/ModernBERT-large-nli': 'ca476cb923a8637073d4ceb0f19f7fc236e260d4', 'MoritzLaurer/ModernBERT-large-zeroshot-v2.0': 'a51e07b524299e309dd2b88d48b0cfa2bd9ec598', 'MoritzLaurer/deberta-v3-large-zeroshot-v2.0': 'cf44676c28ba7312e5c5f8f8d2c22b3e0c9cdae2', 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli': 'b3546ea6b0346eb6f8d5d68b13c7dc6d0376b3d7', 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli': '6f5cf0a2b59cabb106aca4c287eed12e357e90eb'}`
- finished: `2026-11-08T16:28:03`

## Metrics vs labels.csv (609 labelled claims, annotator: claude-draft)

Keep = NLI says entailment (claim survives grounding). Dropped by the citation check = not kept. `nb` = without borderline labels. Premise `window` = NLI window, `local` = cited sentence(s) +-1, `local-block` = the same but within the cited block (+ the list's lead-in), `both` = kept only if window and local say entailment.

| model | context | premise | win | n | keep acc | keep recall | keep precision | false keeps | contra recall | keep acc nb |
|---|---|---|---|---|---|---|---|---|---|---|
| ModernBERT-large-nli | breadcrumb | local | 128 | 350 | 92% | 98% | 92% | 21 | 83% | 94% |
| ModernBERT-large-nli | breadcrumb | local | 400 | 350 | 92% | 98% | 92% | 21 | 83% | 94% |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | 350 | 94% | 98% | 93% | 18 | 86% | 95% |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | 350 | 94% | 98% | 93% | 18 | 86% | 95% |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | 350 | 93% | 96% | 95% | 14 | n/a | 94% |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | 350 | 93% | 96% | 95% | 14 | n/a | 94% |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | 350 | 95% | 98% | 95% | 13 | n/a | 96% |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | 350 | 95% | 98% | 95% | 13 | n/a | 96% |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | 350 | 93% | 97% | 94% | 16 | n/a | 94% |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | 350 | 93% | 97% | 94% | 16 | n/a | 94% |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | 350 | 95% | 97% | 96% | 11 | n/a | 96% |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | 350 | 95% | 97% | 96% | 11 | n/a | 96% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | 350 | 95% | 98% | 95% | 13 | 89% | 96% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | 350 | 95% | 98% | 95% | 13 | 89% | 96% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | 350 | 95% | 98% | 96% | 11 | 86% | 97% |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | 350 | 95% | 98% | 96% | 11 | 86% | 97% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | 350 | 92% | 95% | 94% | 16 | 86% | 94% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | 350 | 92% | 95% | 94% | 16 | 86% | 94% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | 350 | 93% | 95% | 95% | 14 | 83% | 95% |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | 350 | 93% | 95% | 95% | 14 | 83% | 95% |

## Should-drop claims kept, by source (argmax)

Claims whose gold label is not entailment, split by where they come from. Cell = kept / total (lower is better). `cross` = a claim scored against a related section's prose (gold neutral by default, not part of the metrics above; some may truly be entailed, review the list at the end).

| model | context | premise | win | real | negative | outside | beyond | cross |
|---|---|---|---|---|---|---|---|---|
| ModernBERT-large-nli | breadcrumb | local | 128 | 1/2 | 6/43 | 6/23 | 8/21 | 13/259 |
| ModernBERT-large-nli | breadcrumb | local | 400 | 1/2 | 6/43 | 6/23 | 8/21 | 13/259 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | 1/2 | 5/43 | 5/23 | 7/21 | 12/259 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | 1/2 | 5/43 | 5/23 | 7/21 | 12/259 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | 1/2 | 2/43 | 5/23 | 6/21 | 15/259 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | 1/2 | 2/43 | 5/23 | 6/21 | 15/259 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | 0/2 | 2/43 | 5/23 | 6/21 | 15/259 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | 0/2 | 2/43 | 5/23 | 6/21 | 15/259 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | 1/2 | 5/43 | 5/23 | 5/21 | 11/259 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | 1/2 | 5/43 | 5/23 | 5/21 | 11/259 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | 0/2 | 4/43 | 3/23 | 4/21 | 8/259 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | 0/2 | 4/43 | 3/23 | 4/21 | 8/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | 0/2 | 4/43 | 4/23 | 5/21 | 27/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | 0/2 | 4/43 | 4/23 | 5/21 | 27/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | 0/2 | 3/43 | 3/23 | 5/21 | 24/259 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | 0/2 | 3/43 | 3/23 | 5/21 | 24/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | 1/2 | 4/43 | 5/23 | 6/21 | 42/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | 1/2 | 4/43 | 5/23 | 6/21 | 42/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | 0/2 | 3/43 | 5/23 | 6/21 | 28/259 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | 0/2 | 3/43 | 5/23 | 6/21 | 28/259 |

## Threshold sweep

Keep if p_entailment >= threshold (argmax = keep if entailment is the top label). Cell = keep recall / false keeps.

| model | context | premise | win | argmax | >= 0.3 | >= 0.5 | >= 0.7 | >= 0.9 |
|---|---|---|---|---|---|---|---|---|
| ModernBERT-large-nli | breadcrumb | local | 128 | 98% / 21 | 98% / 22 | 97% / 19 | 97% / 11 | 92% / 4 |
| ModernBERT-large-nli | breadcrumb | local | 400 | 98% / 21 | 98% / 22 | 97% / 19 | 97% / 11 | 92% / 4 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | 98% / 18 | 99% / 19 | 98% / 17 | 97% / 8 | 90% / 2 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | 98% / 18 | 99% / 19 | 98% / 17 | 97% / 8 | 90% / 2 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | 96% / 14 | 96% / 15 | 96% / 14 | 95% / 13 | 92% / 11 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | 96% / 14 | 96% / 15 | 96% / 14 | 95% / 13 | 92% / 11 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | 98% / 13 | 98% / 14 | 98% / 13 | 97% / 10 | 93% / 7 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | 98% / 13 | 98% / 14 | 98% / 13 | 97% / 10 | 93% / 7 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | 97% / 16 | 98% / 16 | 97% / 16 | 95% / 12 | 89% / 7 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | 97% / 16 | 98% / 16 | 97% / 16 | 95% / 12 | 89% / 7 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | 97% / 11 | 97% / 15 | 97% / 11 | 96% / 10 | 90% / 6 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | 97% / 11 | 97% / 15 | 97% / 11 | 96% / 10 | 90% / 6 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 128 | 98% / 13 | 98% / 14 | 98% / 13 | 97% / 13 | 95% / 12 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local | 400 | 98% / 13 | 98% / 14 | 98% / 13 | 97% / 13 | 95% / 12 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | 98% / 11 | 99% / 13 | 98% / 11 | 97% / 10 | 96% / 8 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | 98% / 11 | 99% / 13 | 98% / 11 | 97% / 10 | 96% / 8 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 128 | 95% / 16 | 96% / 16 | 95% / 15 | 93% / 13 | 88% / 12 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local | 400 | 95% / 16 | 96% / 16 | 95% / 15 | 93% / 13 | 88% / 12 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | 95% / 14 | 97% / 14 | 95% / 14 | 95% / 11 | 94% / 10 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | 95% / 14 | 97% / 14 | 95% / 14 | 95% / 11 | 94% / 10 |

## Labels per extractor

| model | context | premise | win | section | extractor | ent | neu | con | dropped |
|---|---|---|---|---|---|---|---|---|---|
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 3 | 0 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 37 | 0 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 4 | 1 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 5 | 6 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | 10 | 1 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 2 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 19 | 13 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 26 | 12 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 9 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 10 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 11 | 2 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 11 | 6 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 12 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 10 | 1 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 1 | 2 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 6 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 7 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 11 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 8 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 14 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 13 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 3 | 0 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 37 | 0 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 4 | 1 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 5 | 6 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | 10 | 1 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 2 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 19 | 13 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 26 | 12 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 9 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 10 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 11 | 2 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 11 | 6 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 12 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 10 | 1 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 1 | 2 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 1 | 3 | 5 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 6 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 7 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 11 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 8 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 14 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | sonnet-medium-outside | 0 | 2 | 2 | 2 |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 13 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 3 | 0 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 38 | 0 | 2 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 2 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 4 | 6 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 9 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 1 | 2 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 25 | 7 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 35 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 8 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 10 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 10 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 10 | 7 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 12 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 1 | 2 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 6 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 7 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 10 | 2 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 8 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 14 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium-outside | 0 | 3 | 1 | 2 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 10 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 13 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 3 | 0 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 38 | 0 | 2 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 2 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 4 | 6 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 9 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 1 | 2 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 25 | 7 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 35 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 8 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 0 | 10 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 10 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 10 | 7 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 12 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 1 | 2 | 3 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 6 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 7 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 10 | 2 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 8 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 14 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium-outside | 0 | 3 | 1 | 2 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 10 | 1 | 0 |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 13 | 1 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 38 | 2 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 4 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | 15 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 32 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 38 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 38 | 2 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 4 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | 8 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | 15 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 32 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 38 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | opus-high | 16 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 5 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 32 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 38 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | negatives-handmade | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 5 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 32 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 38 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 0 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 0 | 13 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 0 | 17 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 1 | 14 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | negatives-handmade | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | 3 | 3 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 3 | 8 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 3 | 13 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | 15 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 1 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 16 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 6 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | negatives-handmade | 1 | 8 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 3 | 8 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 3 | 13 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | 15 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 1 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 16 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 6 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | haiku-high | 13 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | negatives-handmade | 1 | 8 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | sonnet-medium | 15 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | 4 | 2 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 3 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 2 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 1 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | sonnet-medium | 13 | 1 | 0 | 1 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 1 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 16 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 6 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | negatives-handmade | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 32 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 3 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 2 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 1 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 0 | 33 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 0 | 40 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | 10 | 2 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | sonnet-medium | 13 | 1 | 0 | 1 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 1 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 1 | 16 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 0 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 6 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 5 | 0 | 1 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | negatives-handmade | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | sonnet-medium | 14 | 1 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | negatives-handmade | 0 | 6 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
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
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 3 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 1 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 5 | 5 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 5 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 38 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 2 | 13 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 6 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 1 | 3 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 2 | 1 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 40 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 5 | 5 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 5 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 38 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | negatives-handmade | 0 | 1 | 8 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | sonnet-medium | 14 | 0 | 0 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 2 | 10 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 2 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 2 | 13 | 2 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 0 | 4 | 1 | 1 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 1 | 5 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 6 | 1 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | flash-3.6-high | 12 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 0 | 7 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 0 | 9 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium | 7 | 0 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium-outside | 0 | 4 | 0 | 2 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 14 | 0 | 0 |
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
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 6 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 11 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 36 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | sonnet-medium | 13 | 1 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 4 | 9 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~opus-high | 3 | 14 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 3 | 3 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 3 | 1 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 4 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | flash-3.6-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 1 | 5 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium | 6 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium-outside | 0 | 3 | 1 | 2 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 11 | 3 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | 33 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | 1 | 1 | 5 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium | 39 | 0 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | 2 | 4 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~flash-3.6-high | 6 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | x-changelog-2-8-0-security~sonnet-medium | 4 | 11 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | 1 | 1 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium | 16 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | 3 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~flash-3.6-high | 1 | 31 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | x-changelog-2-8-0-bugfixes~sonnet-medium | 2 | 36 | 2 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-3.6-high | 7 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | flash-lite-3.6-high | 8 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | 9 | 3 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | negatives-handmade | 1 | 1 | 7 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | opus-high | 9 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | sonnet-medium | 13 | 1 | 0 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-3.6-high | 1 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~flash-lite-3.6-high | 1 | 12 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~haiku-high | 4 | 9 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~opus-high | 3 | 14 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | x-retrying-requests~sonnet-medium | 2 | 13 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | 11 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | 1 | 4 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | negatives-handmade | 0 | 3 | 3 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | 13 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | 1 | 3 | 1 | 1 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~flash-3.6-high | 2 | 4 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | x-using-timeouts~sonnet-medium | 0 | 7 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | flash-3.6-high | 11 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | flash-lite-3.6-high | 13 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | haiku-high | 12 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | negatives-handmade | 0 | 3 | 6 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | opus-high | 17 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | sonnet-medium | 13 | 2 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-3.6-high | 1 | 5 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~flash-lite-3.6-high | 0 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~haiku-high | 0 | 12 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~opus-high | 1 | 8 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | x-configuring-exponential-backoff~sonnet-medium | 0 | 15 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high | 6 | 0 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | 2 | 3 | 1 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | negatives-handmade | 0 | 2 | 4 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium | 6 | 1 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium-outside | 0 | 3 | 1 | 2 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~flash-3.6-high | 0 | 11 | 0 | 0 |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | x-httpx-timeouts-fine-tuning~sonnet-medium | 0 | 11 | 3 | 0 |

## Wrong keep / drop decisions (argmax)

| model | context | premise | win | section | extractor | id | gold | NLI | p_ent | claim |
|---|---|---|---|---|---|---|---|---|---|---|
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.893 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9753 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.893 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9753 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.5104 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.7527 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.4088 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.5104 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.7527 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.4088 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.4577 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.8192 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b3 | neutral | entailment | 0.6022 | urllib3 fixed the SOCKS proxy credential bug so that percent-encoded passwords no longer cause authentication failures with the proxy server. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.4577 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.8192 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | b3 | neutral | entailment | 0.6022 | urllib3 fixed the SOCKS proxy credential bug so that percent-encoded passwords no longer cause authentication failures with the proxy server. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | contradiction | 0.0086 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c19 | entailment | contradiction | 0.1431 | In urllib3 2.8.0, HTTPConnectionPool.urlopen was fixed so that it no longer raises a misleading FullPoolError instead of ValueError when called with an invalid timeout argument on a pool created with block=True. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.4504 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | contradiction | 0.0086 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c19 | entailment | contradiction | 0.1431 | In urllib3 2.8.0, HTTPConnectionPool.urlopen was fixed so that it no longer raises a misleading FullPoolError instead of ValueError when called with an invalid timeout argument on a pool created with block=True. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.4504 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.6773 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.8285 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.886 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.6773 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.8285 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.886 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.3588 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.3588 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.7626 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.7626 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.6985 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.5019 | urllib3 supports decoding deflate-encoded response bodies. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.6985 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.5019 | urllib3 supports decoding deflate-encoded response bodies. |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9417 | The limits argument is used to configure pool timeouts in HTTPX. |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9417 | The limits argument is used to configure pool timeouts in HTTPX. |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | neutral | 0.2971 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high | c6 | entailment | neutral | 0.2971 | If HTTPX is unable to receive data within the read timeout time frame, a ReadTimeout exception is raised. |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n1 | contradiction | entailment | 0.9207 | httpx has three different types of timeouts: connect, read, and write. |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n1 | contradiction | entailment | 0.9207 | httpx has three different types of timeouts: connect, read, and write. |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.2545 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.2545 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.5547 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | negatives-handmade | n3 | contradiction | entailment | 0.5547 | Specifying retries=False keeps the redirect logic of urllib3 enabled. |
| ModernBERT-large-nli | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.8554 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| ModernBERT-large-nli | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.8554 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.6871 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.6938 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| ModernBERT-large-nli | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9595 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.6871 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.6938 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| ModernBERT-large-nli | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9595 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.8238 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.977 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.8238 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.977 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.6796 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.5998 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.5948 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.6796 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.5998 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.5948 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.6282 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.6651 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.6282 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.6651 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | contradiction | 0.0236 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.3942 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | contradiction | 0.0236 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.3942 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.6773 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.8285 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.886 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.6773 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.8285 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.886 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.7626 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.7626 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.4777 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.4777 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.8975 | The limits argument is used to configure pool timeouts in HTTPX. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.8975 | The limits argument is used to configure pool timeouts in HTTPX. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | negatives-handmade | n1 | contradiction | entailment | 0.7354 | httpx has three different types of timeouts: connect, read, and write. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | negatives-handmade | n1 | contradiction | entailment | 0.7354 | httpx has three different types of timeouts: connect, read, and write. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.1141 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.1141 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.638 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.638 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5256 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.5085 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9501 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.2701 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5256 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.5085 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9501 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.2701 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.7107 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9839 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.7107 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9839 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.0119 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.0119 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9351 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9351 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9501 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.9024 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.9501 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.9024 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | neutral | 0.0123 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c19 | entailment | neutral | 0.0291 | In urllib3 2.8.0, HTTPConnectionPool.urlopen was fixed so that it no longer raises a misleading FullPoolError instead of ValueError when called with an invalid timeout argument on a pool created with block=True. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | neutral | 0.0123 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c19 | entailment | neutral | 0.0291 | In urllib3 2.8.0, HTTPConnectionPool.urlopen was fixed so that it no longer raises a misleading FullPoolError instead of ValueError when called with an invalid timeout argument on a pool created with block=True. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.8801 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.946 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9601 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.8801 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.946 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9601 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.1856 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.1941 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0116 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c2 | entailment | neutral | 0.1856 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c3 | entailment | neutral | 0.1941 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high | c4 | entailment | neutral | 0.0116 | In urllib3 2.8.0, an issue where Chunked Deflate streaming could enter an infinite loop was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9511 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9511 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9104 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9104 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.2508 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c8 | entailment | neutral | 0.2508 | In urllib3 2.8.0, a security issue was fixed where chunked Deflate streaming could enter an infinite loop. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0262 | HTTPX supports only four types of timeouts. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9836 | The limits argument is used to configure pool timeouts in HTTPX. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0262 | HTTPX supports only four types of timeouts. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9836 | The limits argument is used to configure pool timeouts in HTTPX. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0295 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0295 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | opus-high | c8 | entailment | neutral | 0.2307 | Specifying retries=False in urllib3 disables all redirect logic. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | opus-high | c8 | entailment | neutral | 0.2307 | Specifying retries=False in urllib3 disables all redirect logic. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.4835 | Specifying redirect=False in urllib3's request() disables redirects. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.6853 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.4835 | Specifying redirect=False in urllib3's request() disables redirects. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.6853 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9666 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.991 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9666 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.991 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.6467 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9831 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.6467 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9831 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.0468 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.0468 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.7202 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.7202 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.8396 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.8396 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | neutral | 0.0027 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c16 | entailment | neutral | 0.0027 | The non-standard IPv4 forms detected by urllib3's is_ipaddress() include octal such as 0177.0.0.1. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.8801 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.946 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9601 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.8801 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.946 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9601 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9511 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9511 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9372 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.5875 | urllib3 supports decoding deflate-encoded response bodies. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9372 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.5875 | urllib3 supports decoding deflate-encoded response bodies. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0559 | HTTPX supports only four types of timeouts. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9816 | The limits argument is used to configure pool timeouts in HTTPX. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0559 | HTTPX supports only four types of timeouts. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9816 | The limits argument is used to configure pool timeouts in HTTPX. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0067 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0067 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | haiku-high | c13 | entailment | neutral | 0.3176 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | haiku-high | c13 | entailment | neutral | 0.3176 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.397 | Specifying redirect=False in urllib3's request() disables redirects. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | sonnet-medium | c8 | entailment | neutral | 0.397 | Specifying redirect=False in urllib3's request() disables redirects. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5666 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9915 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.5666 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9915 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o3 | neutral | entailment | 0.5102 | UnrewindableBodyError is an exception class defined in the urllib3.exceptions module. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9415 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o3 | neutral | entailment | 0.5102 | UnrewindableBodyError is an exception class defined in the urllib3.exceptions module. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9415 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.0648 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.0648 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.8338 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.8977 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.8338 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.8977 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.5931 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o2 | neutral | entailment | 0.5931 | In urllib3, UnrewindableBodyError is raised when a request body cannot be rewound for a retry or redirect. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.8705 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9933 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.8705 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9933 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9683 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9883 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n1 | contradiction | entailment | 0.9683 | The Chunked Deflate streaming infinite loop fixed in urllib3 2.8.0 was a high severity issue. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9883 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.8013 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.8013 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | sonnet-medium | c9 | entailment | neutral | 0.0299 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop has Medium severity. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | sonnet-medium | c9 | entailment | neutral | 0.0299 | The security issue in urllib3 where chunked Deflate streaming could enter an infinite loop has Medium severity. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.405 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.1097 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1334 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.405 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.1097 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1334 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0095 | HTTPX supports only four types of timeouts. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.956 | The limits argument is used to configure pool timeouts in HTTPX. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0095 | HTTPX supports only four types of timeouts. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.956 | The limits argument is used to configure pool timeouts in HTTPX. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0092 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0092 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.8892 | Specifying redirect=False disables the retrying logic of urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | negatives-handmade | n4 | contradiction | entailment | 0.8892 | Specifying redirect=False disables the retrying logic of urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.629 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | retrying-requests | sonnet-medium | c10 | neutral | entailment | 0.629 | A urllib3 Retry instance can be passed as the retries parameter for more granular control over retries. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9908 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.6118 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9669 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.9908 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.6118 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9669 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9295 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9295 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.3864 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high | c21 | entailment | neutral | 0.3864 | Users on newer Python versions should upgrade to Python 3.13.14+ or 3.14.5+ to get the standard library security fixes. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.6487 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.7859 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.9288 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.6487 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n6 | neutral | entailment | 0.7859 | Since urllib3 2.8.0, HTTP 303 redirects are no longer followed for requests with chunked bodies. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n7 | contradiction | entailment | 0.9288 | In urllib3 2.8.0, assert_fingerprint() raises binascii.Error when a fingerprint contains non-hexadecimal characters. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.8705 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9933 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.8705 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9933 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9883 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9883 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.7534 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.7534 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.2529 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1537 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.2529 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | c11 | entailment | neutral | 0.1537 | Adding the backoff_jitter parameter to urllib3's Retry class introduces random variance. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0176 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.0176 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.006 | HTTPX supports only four types of timeouts. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9095 | The limits argument is used to configure pool timeouts in HTTPX. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.006 | HTTPX supports only four types of timeouts. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9095 | The limits argument is used to configure pool timeouts in HTTPX. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0023 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0023 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | retrying-requests | haiku-high | c13 | entailment | neutral | 0.0672 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | retrying-requests | haiku-high | c13 | entailment | neutral | 0.0672 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.7584 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9673 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.0449 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.7584 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9673 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.0449 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
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
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9936 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9936 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9944 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.6491 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9944 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n4 | contradiction (borderline) | entailment | 0.6491 | The proxy tunneling safeguards added in urllib3 2.8.0 affect users of Python 3.13. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.7388 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9974 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | o1 | neutral | entailment | 0.7388 | urllib3's ProxyManager class accepts the proxy_ssl_context parameter for configuring HTTPS proxy TLS settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9974 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9988 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9988 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9965 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.9768 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.9965 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.9768 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0041 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9955 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0041 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.9955 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0007 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0007 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | haiku-high | c13 | entailment | neutral | 0.0408 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | haiku-high | c13 | entailment | neutral | 0.0408 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.4921 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | retrying-requests | sonnet-medium | c9 | entailment | neutral | 0.4921 | Specifying redirect=False in urllib3's request() keeps the retrying logic. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.8151 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.995 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.42 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b1 | neutral | entailment | 0.8151 | In simple cases, the timeout parameter passed to urllib3's request() function must be a float. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.995 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.42 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
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
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.9542 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9678 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o4 | neutral | entailment | 0.9542 | HTTPResponse.drain_conn() discards unread response data by invoking HTTPResponse.stream() with a 64 KiB chunk size. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | flash-3.6-high-outside | o6 | neutral | entailment | 0.9678 | assert_fingerprint() raises an SSLError whenever a fingerprint contains non-hexadecimal characters. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9793 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | negatives-handmade | n2 | contradiction | entailment | 0.9793 | In urllib3 2.8.0, passing ssl_context instead of proxy_ssl_context for HTTPS proxies with use_forwarding_for_https=True raises an error. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.936 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium-outside | o1 | neutral (borderline) | entailment | 0.936 | urllib3's HTTPResponse.stream() method accepts an amt parameter that controls how many bytes are read per chunk. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0215 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | sonnet-medium | c27 | entailment | contradiction | 0.0215 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9944 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9764 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b2 | neutral | entailment | 0.9944 | Destination client certificates no longer apply to HTTPS connections in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | flash-3.6-high-outside | b3 | contradiction (borderline) | entailment | 0.9764 | urllib3 requires configuring both proxy_assert_hostname and proxy_assert_fingerprint for proxy identity checks. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9935 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | negatives-handmade | n3 | contradiction | entailment | 0.9935 | In urllib3 2.8.0, proxy CA certificates are configured in ssl_context. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.5604 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.8682 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | o2 | neutral (borderline) | entailment | 0.5604 | urllib3's HTTPResponse.stream() method can read response bodies that use chunked transfer encoding. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | sonnet-medium-outside | o3 | neutral (borderline) | entailment | 0.8682 | urllib3 supports decoding deflate-encoded response bodies. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.1812 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3674 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.3775 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | c6 | entailment | neutral | 0.1812 | When no server-requested delay is applied, urllib3's Retry class can be configured with a non-zero backoff_factor to introduce exponential delays between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | c9 | entailment | neutral | 0.3674 | With a backoff_factor of 0.5, urllib3's Retry class yields retry sleeps of 0.0s, 1.0s, 2.0s, and so on. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | haiku-high | c10 | entailment | neutral | 0.3775 | With urllib3's Retry class, retry sleeps go up to the backoff_max value. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.6479 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | negatives-handmade | n6 | contradiction | entailment | 0.6479 | The backoff delays of Retry grow linearly between retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.4487 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | sonnet-medium | c14 | entailment (borderline) | neutral | 0.4487 | Adding backoff_jitter to urllib3's Retry introduces random variance to the retry delays. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0378 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.991 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b1 | entailment (borderline) | neutral | 0.0378 | HTTPX supports only four types of timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | flash-3.6-high-outside | b3 | neutral (borderline) | entailment | 0.991 | The limits argument is used to configure pool timeouts in HTTPX. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.524 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium-outside | o3 | neutral | entailment | 0.524 | The httpx.Limits class configures the maximum number of connections in the connection pool through its max_connections parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0028 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | sonnet-medium | c14 | entailment | neutral | 0.0028 | HTTPX allows configuring the timeout behavior for any of the connect, read, write, and pool timeout values. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0682 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | flash-3.6-high | c12 | entailment | neutral | 0.0682 | A PoolManager pool-level retry policy in urllib3 can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | haiku-high | c13 | entailment | neutral | 0.0679 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | haiku-high | c13 | entailment | neutral | 0.0679 | A pool-level retry policy set on PoolManager can be overridden by specifying retries for request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.4065 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | sonnet-medium | c15 | entailment | neutral | 0.4065 | A pool-level retry policy set on a urllib3 PoolManager can be overridden by specifying retries to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.96 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9791 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.1376 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | o3 | neutral | entailment | 0.96 | A urllib3 PoolManager instance accepts a Timeout object for its timeout parameter. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b2 | neutral (borderline) | entailment | 0.9791 | To configure separate connect and read timeouts in urllib3, you must instantiate a Timeout object. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | flash-3.6-high-outside | b3 | entailment (borderline) | neutral | 0.1376 | Specifying a timeout at the PoolManager level sets a default timeout for all requests made by that pool. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | using-timeouts | sonnet-medium | c7 | entailment | neutral | 0.4482 | A pool-level timeout set on a urllib3 PoolManager can be overridden by specifying timeout to request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | using-timeouts | sonnet-medium | c7 | entailment | neutral | 0.4482 | A pool-level timeout set on a urllib3 PoolManager can be overridden by specifying timeout to request(). |

## Cross-section pairs kept (argmax)

| model | context | premise | win | premise section | claim from | id | p_ent | claim |
|---|---|---|---|---|---|---|---|---|
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.852 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.4619 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9357 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.8698 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.6636 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.852 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.4619 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9357 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.8698 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.6636 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.6596 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9357 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.8987 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.7002 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.6596 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9357 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.8987 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.7002 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.4301 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.4301 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.6764 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-nli | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.3959 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.6764 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-nli | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.3959 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-nli | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.7003 | A Timeout instance allows specifying separate connect and read timeouts. |
| ModernBERT-large-nli | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.7003 | A Timeout instance allows specifying separate connect and read timeouts. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.7477 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.903 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.8148 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.6832 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.7477 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.903 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.8148 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.6832 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.6196 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.903 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.8004 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.6917 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.6196 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.903 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.8004 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.6917 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.4301 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.4301 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.6764 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.3959 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.6764 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.3959 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-nli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.7443 | A Timeout instance allows specifying separate connect and read timeouts. |
| ModernBERT-large-nli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.7443 | A Timeout instance allows specifying separate connect and read timeouts. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9015 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9566 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9488 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9463 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9015 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9566 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9488 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9463 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9566 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.6989 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.8589 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9494 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9566 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.6989 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.8589 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9494 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.924 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.924 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.7841 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.883 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.7841 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.883 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.5894 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.5894 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.8051 | The retries parameter of urllib3's request() controls retries. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.8051 | The retries parameter of urllib3's request() controls retries. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.9147 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9416 | A Timeout instance allows specifying separate connect and read timeouts. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.9147 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9416 | A Timeout instance allows specifying separate connect and read timeouts. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.7867 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9023 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.7343 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9802 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.966 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.7867 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9023 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.7343 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9802 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.966 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9023 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.5955 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9661 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9522 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9023 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.5955 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9661 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9522 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.924 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.924 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.7841 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.883 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.7841 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.883 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.5894 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.5894 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.6729 | The retries parameter of urllib3's request() controls retries. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.6729 | The retries parameter of urllib3's request() controls retries. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.7621 | A Timeout instance allows specifying separate connect and read timeouts. |
| ModernBERT-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.7621 | A Timeout instance allows specifying separate connect and read timeouts. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.6987 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.7484 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.6395 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.6987 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c6 | 0.7484 | Configurations relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.6395 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.6987 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.8206 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.5252 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.6987 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.8206 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.5252 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.836 | A Retry instance can be used for more granular control of retries in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.836 | A Retry instance can be used for more granular control of retries in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.7426 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.7426 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.7672 | A Retry instance gives more granular control over retries in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.7672 | A Retry instance gives more granular control over retries in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5068 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5068 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9166 | A Timeout instance allows specifying separate connect and read timeouts. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9166 | A Timeout instance allows specifying separate connect and read timeouts. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.7896 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.6368 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.7896 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.6368 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.7896 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.7896 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.836 | A Retry instance can be used for more granular control of retries in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.836 | A Retry instance can be used for more granular control of retries in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.7426 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.7426 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.7672 | A Retry instance gives more granular control over retries in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.7672 | A Retry instance gives more granular control over retries in urllib3. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5068 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5068 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9006 | A Timeout instance allows specifying separate connect and read timeouts. |
| deberta-v3-large-zeroshot-v2.0 | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.9006 | A Timeout instance allows specifying separate connect and read timeouts. |
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
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9937 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9986 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9902 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9993 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9987 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9937 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c5 | 0.9986 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9902 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9993 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9987 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.9267 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9986 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.7693 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9993 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9989 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.9267 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c11 | 0.9986 | urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c12 | 0.7693 | Configurations of urllib3 relying on HTTPS proxy TLS configuration being ignored or overridden by destination settings may require changes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9993 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.9989 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9913 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9913 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.8782 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9853 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c27 | 0.8782 | In urllib3 2.8.0, HTTPSConnection.connect() was fixed so that it no longer overrides ProxyConfig.ssl_context's certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9853 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.9876 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9867 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c6 | 0.9876 | Specifying an integer for the retries parameter changes the number of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c9 | 0.9867 | A Retry instance can be used for more granular control of retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.8991 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.9719 | The Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c9 | 0.8991 | A Retry instance can be used in urllib3 for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c10 | 0.9719 | The Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.975 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.9932 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c6 | 0.975 | Specifying an integer for the retries parameter of request() changes the number of retries urllib3 performs. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.9932 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9897 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.9641 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.9897 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.9641 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.9898 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.9601 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c6 | 0.9898 | Specifying an integer as the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c11 | 0.9601 | The urllib3 Retry class allows far greater control of how requests are retried. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.996 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.996 | A Timeout instance allows specifying separate connect and read timeouts. |
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
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9876 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.8164 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c3 | 0.5318 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9403 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9912 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9595 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c1 | 0.9876 | In urllib3 2.8.0, an issue where the TLS configuration for HTTPS proxies could be ignored or overridden was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c2 | 0.8164 | In urllib3 2.8.0, an issue where `HTTPResponse.stream()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c3 | 0.5318 | In urllib3 2.8.0, an issue where `read_chunked()` could buffer a chunk-size line of unbounded length in memory was fixed. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c8 | 0.9403 | In urllib3, proxy client certificates are configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c10 | 0.9912 | In urllib3, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~flash-3.6-high | c11 | 0.9595 | In urllib3, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.5505 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c13 | 0.6879 | In urllib3, proxy CA certificates and client certificates should be configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9906 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.938 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c1 | 0.5505 | In urllib3 2.8.0, a security issue was fixed where the TLS configuration for HTTPS proxies could be ignored or overridden. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c13 | 0.6879 | In urllib3, proxy CA certificates and client certificates should be configured in `proxy_ssl_context`. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c15 | 0.9906 | In urllib3 2.8.0, destination client certificates no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-bugfixes | changelog-2-8-0-security~sonnet-medium | c16 | 0.938 | In urllib3 2.8.0, destination identity overrides no longer apply to HTTPS forwarding proxy connections. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9846 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~flash-3.6-high | c23 | 0.9846 | `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9853 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c35 | 0.8245 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c28 | 0.9853 | HTTPSConnection no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | changelog-2-8-0-security | changelog-2-8-0-bugfixes~sonnet-medium | c35 | 0.8245 | urllib3 host normalization uppercases the hexadecimal digits of retained percent-encoded octets. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~flash-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~flash-lite-3.6-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.7854 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c8 | 0.6594 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.603 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c3 | 0.7854 | The number of retries in urllib3 can be controlled using the retries parameter of request(). |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c8 | 0.6594 | Specifying redirect=False for request() disables redirects while keeping the retrying logic. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~haiku-high | c9 | 0.603 | A Retry instance gives more granular control over retries in urllib3. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.5835 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5522 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c6 | 0.5835 | Specifying an integer for the retries parameter of urllib3's request() changes the number of retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~opus-high | c11 | 0.5522 | A urllib3 Retry instance can be used for more granular control of how requests are retried. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.9215 | The retries parameter of urllib3's request() controls retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c1 | 0.4637 | urllib3 can automatically retry idempotent requests. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | configuring-exponential-backoff | retrying-requests~sonnet-medium | c3 | 0.9215 | The retries parameter of urllib3's request() controls retries. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.5335 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.6555 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c1 | 0.5335 | Timeouts allow controlling how long requests are allowed to run before being aborted. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | httpx-timeouts-fine-tuning | using-timeouts~flash-3.6-high | c4 | 0.6555 | A Timeout instance allows specifying separate connect and read timeouts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c1 | 0.6098 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | configuring-exponential-backoff~flash-3.6-high | c1 | 0.6098 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 128 | retrying-requests | configuring-exponential-backoff~opus-high | c1 | 0.6098 | By default, urllib3's Retry does not sleep between retry attempts. |
| DeBERTa-v3-base-mnli-fever-anli | breadcrumb | local-block | 400 | retrying-requests | configuring-exponential-backoff~opus-high | c1 | 0.6098 | By default, urllib3's Retry does not sleep between retry attempts. |
