# Bench 003-speed-bench

- note: large fp32 (forced) vs int8, threads; fp16 had 159s @10 threads
- sample: 16 pairs, evenly spread by length over the largest window size, context `breadcrumb`, premise `window`; one warm-up batch before timing
- torch default threads: 10
- started: `2026-11-07T15:49:14`
- models: `['MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli', 'MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli@int8']`
- contexts: `['breadcrumb']`
- premises: `['window']`
- radius: `1`
- sections: `all`
- batch: `8`
- git: `{'commit': 'e8077b00a58fcaac2cbebef8f3f9dc7762970048', 'branch': 'feat/nli-and-extractors-testing', 'dirty_experiment_files': True}`
- inputs: `{'pairs_windows_sha256': '785dc17026be', 'labels_sha256': '0da00b1e7a82'}`
- versions: `{'python': '3.12.10', 'torch': '2.15.0+cpu', 'transformers': '5.22.2'}`
- finished: `2026-11-07T15:51:58`

| model | threads | batch | seconds | pairs/s | vs first row | max abs dp_ent vs fp32 | label agreement vs fp32 |
|---|---|---|---|---|---|---|---|
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | 4 | 8 | 22.8 | 0.70 | 1.00x | - | - |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | 6 | 8 | 20.4 | 0.79 | 1.12x | - | - |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | 10 | 8 | 17.9 | 0.89 | 1.27x | - | - |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli@int8 | 4 | 8 | 15.0 | 1.07 | 1.52x | 0.868 | 0/16 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli@int8 | 6 | 8 | 12.8 | 1.25 | 1.79x | 0.868 | 0/16 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli@int8 | 10 | 8 | 11.1 | 1.44 | 2.05x | 0.868 | 0/16 |
