# NLI runs

One line per run; details in each run's summary.md. Findings across runs: ../FINDINGS.md

| run | date | models | contexts | note |
|---|---|---|---|---|
| [000-first-base-run](000-first-base-run/config.json) | 2026-11-07T13:30 | nli-deberta-v3-base | none | first try, before tracking/labels/negatives (CSV only) |
| [001-baseline](001-baseline/summary.md) | 2026-11-07T13:12 | nli-deberta-v3-xsmall, nli-deberta-v3-base, DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none | window only; 3 models; labels + handmade negatives |
| [002-context](002-context/summary.md) | 2026-11-07T13:51 | nli-deberta-v3-xsmall, nli-deberta-v3-base, DeBERTa-v3-large-mnli-fever-anli-ling-wanli | breadcrumb, sentence | project + breadcrumb in front of the window (2 variants) |
| [003-speed-bench](003-speed-bench/bench.md) | 2026-11-07T15:49 | DeBERTa-v3-large-mnli-fever-anli-ling-wanli, DeBERTa-v3-large-mnli-fever-anli-ling-wanli@int8 | bench | large fp32 (forced) vs int8, threads; fp16 had 159s @10 threads |
| [004-premise-local](004-premise-local/summary.md) | 2026-11-07T15:52 | nli-deberta-v3-xsmall, nli-deberta-v3-base, DeBERTa-v3-base-mnli-fever-anli, DeBERTa-v3-large-mnli-fever-anli-ling-wanli | none, breadcrumb / window, local, both | 4 models (large now fp32); window vs cited sentence +-1 vs both; threshold sweep |
| [005-bench-new-families](005-bench-new-families/bench.md) | 2026-11-07T18:35 | MiniCheck-DeBERTa-v3-Large, hallucination_evaluation_model, DeBERTa-v3-large-mnli-fever-anli-ling-wanli, nli-deberta-v3-base | bench | time MiniCheck + HHEM vs known models before run 006, to keep it under 2 h |
| [006-realistic-negatives](006-realistic-negatives/summary.md) | 2026-11-07T18:37 | nli-deberta-v3-base, DeBERTa-v3-base-mnli-fever-anli, hallucination_evaluation_model, DeBERTa-v3-large-mnli-fever-anli-ling-wanli, MiniCheck-DeBERTa-v3-Large | breadcrumb / window, local, both | 2 extractors (sonnet-medium, flash-3.6-high) on 4 new sections (changelog, long, httpx), outside/beyond + cross-section claims, fact-checkers MiniCheck + HHEM |
| [007-block-premise-new-models](007-block-premise-new-models/summary.md) | 2026-11-08T16:04 | ModernBERT-large-nli, ModernBERT-large-zeroshot-v2.0, deberta-v3-large-zeroshot-v2.0, DeBERTa-v3-large-mnli-fever-anli-ling-wanli, DeBERTa-v3-base-mnli-fever-anli | breadcrumb / local, local-block | local-block premise (+-1 within the cited block + list lead-in) vs local; 3 newer NLI models vs run 006 winners |
