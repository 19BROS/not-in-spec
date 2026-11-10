# Bench 005-bench-new-families

- note: time MiniCheck + HHEM vs known models before run 006, to keep it under 2 h
- sample: 24 pairs, evenly spread by length over the largest window size, context `breadcrumb`, premise `window`; one warm-up batch before timing
- torch default threads: 10
- started: `2026-11-07T18:35:00`
- models: `['lytang/MiniCheck-DeBERTa-v3-Large', 'vectara/hallucination_evaluation_model', 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli', 'cross-encoder/nli-deberta-v3-base']`
- contexts: `['breadcrumb']`
- premises: `['window']`
- radius: `1`
- sections: `all`
- batch: `8`
- git: `{'commit': 'e8077b00a58fcaac2cbebef8f3f9dc7762970048', 'branch': 'feat/nli-and-extractors-testing', 'dirty_experiment_files': True}`
- inputs: `{'pairs_windows_sha256': 'a04e136ff451', 'labels_sha256': '44ded39573b9'}`
- versions: `{'python': '3.12.10', 'torch': '2.15.0+cpu', 'transformers': '5.22.2'}`
- finished: `2026-11-07T18:37:18`

| model | threads | batch | seconds | pairs/s | vs first row | max abs dp_ent vs fp32 | label agreement vs fp32 |
|---|---|---|---|---|---|---|---|
| MiniCheck-DeBERTa-v3-Large | 10 | 8 | 35.3 | 0.68 | 1.00x | - | - |
| hallucination_evaluation_model | 10 | 8 | 11.3 | 2.13 | 1.00x | - | - |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | 10 | 8 | 38.9 | 0.62 | 1.00x | - | - |
| nli-deberta-v3-base | 10 | 8 | 12.1 | 1.98 | 1.00x | - | - |
