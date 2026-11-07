# NLI grounding: findings

What we learned, run by run. Raw numbers live in `runs/NNN-*/summary.md`; this file is the narrative. Append new runs at the bottom; don't rewrite old entries (add a "Later:" note instead).

**Caveat for every number below:** gold labels in `labels.csv` are a Claude draft (`annotator=claude-draft`), 139 labelled claims from 2 sections of one library. Treat percentages as directional, not as a benchmark. One claim ≈ 0.7 pp.

Metric meanings (all "keep" = NLI says entailment = claim survives grounding):
- **keep recall**: of the claims that *should* be kept, how many were kept. Low = good claims thrown away.
- **keep precision**: of the claims kept, how many should have been. Low = bad claims let through.
- **false keeps**: count of claims kept that should have been dropped (mostly the hand-made negatives).
- **contra recall**: of the contradiction negatives, how many the model labelled contradiction.

## Setup (shared by all runs)

- Sections: urllib3 user guide, `retrying-requests` and `configuring-exponential-backoff` (@ `d07367d`), simulated Sphinx parse.
- Claims: 5 extractors (flash-3.6-high, flash-lite-3.6-high, haiku-high, opus-high, sonnet-medium) from `prompt.md`, plus 9 hand-made negatives per section.
- Premise = prose-only NLI window(s) containing the citation; hypothesis = the claim. Windows of 400 tokens (SPEC candidate; each section fits in one window) and 128 tokens (forces boundaries).
- Decision rule: argmax label; keep iff entailment.
- Hardware: laptop i5-1235U (2 P + 8 E cores), CPU-only torch.

## 000-first-base-run

`nli-deberta-v3-base`, window only, before labels and negatives existed (CSV only). (The INDEX date is when it was archived, not when it ran.)

- Claims phrased as "urllib3's X …" came out **neutral** even when the window states X, because the window never names the project. Flash's claims, which don't name it, got ≈0.99 entailment.
- Numbers trip the model: flash-lite c6 almost copies the premise ("0.0s, 1.0s, 2.0s …") and was still neutral.
- A fact that only lives in a code block (the backoff formula) is in no window, so a claim about it can never be grounded (sonnet c8 is dropped by the citation check, which is correct).

These motivated labels + negatives (run 001) and the premise context prefix (run 002).

## 001-baseline: 3 models, window only

| model | win | keep recall | keep precision | false keeps | contra recall | time (276 pairs) |
|---|---|---|---|---|---|---|
| xsmall | 128 | 42% | 96% | 2 | 71% | 32 s |
| xsmall | 400 | 58% | 96% | 3 | 71% | |
| base | 128 | 42% | 96% | 2 | 71% | 82 s |
| base | 400 | 50% | 98% | 1 | 71% | |
| large (MoritzLaurer mnli-fever-anli-ling-wanli) | 128 | 69% | 99% | 1 | 100% | 2084 s |
| large | 400 | 87% | 97% | 3 | 86% | |

- **The failure mode is recall, not precision.** Every model rarely lets a bad claim through (precision ≥ 96%) but throws away many good ones. For notinspec, that means grounding would silently delete true documentation facts from the reference set.
- **The SPEC candidate (base) is no better than xsmall** here and drops half of the good claims.
- **Smaller windows hurt every model.** 128-token windows cut away the sentence that names the subject.
- **large is much better but also much slower**: ~25× base for ~2.4× parameters. The large slowdown points at the laptop (2 fast cores, power limits) rather than the model.
  - Later (run 003): the cause was **fp16**, not the laptop. transformers 5 loads the large checkpoint in its stored dtype (fp16), which is very slow on CPU. Forced fp32 is ~9× faster and gives identical metrics (run 004).

## 002-context: project + breadcrumb in front of the window

Two premise prefixes, everything else the same as 001:
- `breadcrumb`: `urllib3 > User Guide > Retrying Requests:\n\n<window>`
- `sentence`: `This text is from the urllib3 documentation, section "User Guide > Retrying Requests".\n\n<window>`

| model | ctx | win | keep recall | keep precision | false keeps | contra recall | Δ recall vs 001 |
|---|---|---|---|---|---|---|---|
| xsmall | breadcrumb | 128 | 78% | 97% | 3 | 57% | +36 |
| xsmall | breadcrumb | 400 | 85% | 96% | 4 | 57% | +27 |
| xsmall | sentence | 128 | 69% | 99% | 1 | 64% | +27 |
| xsmall | sentence | 400 | 66% | 96% | 3 | 57% | +8 |
| base | breadcrumb | 128 | 78% | 98% | 2 | 71% | +36 |
| base | breadcrumb | 400 | 75% | 99% | 1 | 71% | +25 |
| base | sentence | 128 | 76% | 98% | 2 | 71% | +34 |
| base | sentence | 400 | 75% | 99% | 1 | 71% | +25 |
| large | breadcrumb | 128 | 98% | 99% | 1 | 100% | +29 |
| large | breadcrumb | 400 | 100% | 98% | 3 | 86% | +13 |
| large | sentence | 128 | 97% | 99% | 1 | 100% | +28 |
| large | sentence | 400 | 100% | 98% | 3 | 86% | +13 |

Timing: xsmall ~25 s, base ~78 s, large 2166 s / 2307 s per context.

- **Context is the biggest single win so far.** Recall jumps 13–36 pp for every model and window size, with precision unchanged (96–99%). Telling the model which project and section the text is from fixes the "urllib3's X → neutral" problem from run 000.
- **`breadcrumb` ≥ `sentence`.** Equal for base and large; for xsmall the short breadcrumb is clearly better (85% vs 66% at 400). Prefer the breadcrumb: shorter, and no worse anywhere.
- **large + context ≈ solves this set**: 97–100% recall, 1–3 false keeps. With context, 128-token windows no longer hurt large (98% vs 100%).
- **base + context lands at ~75–78% recall**: usable, but still drops ~1 in 4 good claims.
- **Context slightly weakens contradiction detection for xsmall** (71% → 57%): the prefix makes it more willing to say entailment overall.

### What large still gets wrong (run 002)

- **Negation / near-copy negatives at 400 tokens only** (correct at 128):
  - backoff n5 "Retry waits before the second attempt" vs premise "with no delay before the second attempt (the first retry)": entailment 0.98–0.99.
  - retry n4 "redirect=False disables the retrying logic" vs "To disable redirects but keep the retrying logic, specify redirect=False": entailment 0.66–0.70.
  - Premises are ~203 tokens, so this is **not truncation**. A longer premise dilutes the negation: the model sees mostly matching words. Both are exactly the kind of wrong claim a grounding step must catch.
- **sonnet retry c10** "A Retry instance can be passed as the retries parameter …": gold says neutral (the "retries parameter" link is only in code), large says entailment 0.99+. Debatable: the prose says "control the retries… use a Retry instance" right after discussing the `retries` parameter. **Label to review.**
- **haiku backoff c9 / c11 / c12 at 128** (numbers "0.0s, 1.0s, 2.0s"; "backoff_jitter introduces random variance") → neutral. The 128-token window splits these sentences from the ones naming `backoff_factor` / `backoff_jitter`.

## Open questions / next runs (as of run 002; see the end of the file for updates)

1. **Review `labels.csv`** (human annotator), especially sonnet retry c10, the `borderline=yes` rows and backoff n9. Numbers above move by ~0.7 pp per claim.
2. **Does large justify its cost?** At ~36 min per (context × 276 pairs) on this laptop it's impractical for the pipeline as-is. Try: thread limit to P-cores, int8 dynamic quantization or OpenVINO (log as separate runs, since scores change slightly), or score only 400-token windows.
3. **Middle-size option**: test another model between base and large (e.g. `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli`, same size as base but trained on more NLI data than `cross-encoder/nli-deberta-v3-base`).
4. **Negation at long premises**: consider scoring the claim against the cited sentence(s) ± 1 as well as the full window, and require both (or the min) to be entailment. Would catch n4/n5 cheaply.
5. **Threshold instead of argmax**: check whether a p_entailment threshold (e.g. 0.5 / 0.7) trades recall vs false keeps better than argmax; the CSVs in `results/` already have the probabilities.
6. **More data**: two sections and 18 negatives are too few to separate models that are within ~3 pp. Add a section from another library (the formula-in-code and code-only-facts cases look systemic).

## 003-speed-bench: why large was slow

16 long pairs (400-token windows + breadcrumb), large model, batch 8, one warm-up batch.

| variant | 2 threads | 4 | 6 | 10 (torch default) |
|---|---|---|---|---|
| fp16 (what 001/002 ran, transformers 5 default) | 303.5 s | 230.6 s | 196.3 s | 159.4 s |
| **fp32 (forced)** | | 22.8 s | 20.4 s | **17.9 s** |
| int8 dynamic quantization | | 15.0 s | 12.8 s | 11.1 s |

(The fp16 row is from a first bench attempt that crashed on int8 before writing a run folder, so it is not in `runs/003-speed-bench/bench.md`.)

- **The large model was running in fp16.** transformers 5 keeps the checkpoint dtype, and that checkpoint is fp16, which a CPU computes very slowly. Forcing fp32 makes it **~9× faster**. `nli_run.py` now always loads in fp32.
- **Limiting threads makes it slower.** The idea that the 8 efficiency cores hold the 2 performance cores back was wrong: the torch default (10 threads) was fastest at every precision.
- **int8 breaks this model**: 0/16 labels agree with fp32, p_entailment off by up to 0.87. It is ~1.6× faster but useless; it stays in the script for benchmarking only.
- The score cache (`.cache/scores.jsonl`) made run 004 skip the 1 008 pairs (xsmall and base, window premise, none + breadcrumb) already scored in 001/002. The large model's old scores are cached as `fp16`, so they were re-scored in fp32.

## 004-premise-local: new base model, cited-sentence premise, thresholds

4 models × context none/breadcrumb × premise `window` / `local` (cited sentence(s) ± 1) / `both` (keep only if window AND local entail). Large now in fp32: its window metrics are **identical to 001/002**, so fp16 changed only speed, not decisions.

Breadcrumb only (`none` is worse everywhere, ~35–87% recall). `local` doesn't depend on window size, so a single column:

| model | window 128 | window 400 | local | both 400 | time, window 400 + 128 (252 pairs) | time, local (126 pairs) |
|---|---|---|---|---|---|---|
| xsmall | 78% / 3 | 85% / 4 | 90% / 4 | 75% / 3 | (cached) | 4 s |
| base (cross-encoder, SPEC candidate) | 78% / 2 | 75% / 1 | **95% / 3** | 73% / 1 | (cached) | 16 s |
| **base-mnli-fever-anli** (MoritzLaurer) | **99% / 2** | **100% / 3** | **99% / 2** | 99% / 2 | 65 s | 16 s |
| large (fp32) | 98% / 1 | 100% / 3 | 97% / **0** | 97% / 0 | 214 s | 53 s |

Cell = keep recall / false keeps (139 labelled claims; 18 negatives + 2 neutral real claims are the "should drop" set).

- **`MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli` matches large at base size and ~3× its speed.** With breadcrumb it reaches 99–100% recall, 2–3 false keeps, 86–93% contradiction recall. The `cross-encoder/nli-deberta-v3-base` from the SPEC is clearly weaker (75–78% with window premises). **Recommendation: replace the SPEC candidate with this model.**
- **The local premise (cited sentence ± 1) with breadcrumb is as good as or better than the window for every model**, and ~4× cheaper (shorter input):
  - cross-encoder base: 75% → 95% recall. Its window errors were mostly "Specifying retries=False … disables …" claims, whose sentence in the window is a lead-in to a removed code block; the long window confuses it.
  - large: **0 false keeps.** It now rejects the n4/n5 negations it accepted with 400-token windows (run 002), confirming that the long premise was diluting the negation.
  - Without context, local is bad (34–48% recall): the cited sentence alone rarely names the subject. Context and local go together.
- **`both` (window AND local) is never better than `local` alone.** It only adds the window's misses. Drop the idea.
- **Thresholds don't beat argmax** for the good configs. For base-mnli-fever-anli and large, recall stays ≥ 97% up to p ≥ 0.7 and the false keeps don't go away (they are confident, p 0.75–0.99). A threshold helps only xsmall + local (p ≥ 0.9: 82% recall / 0 false keeps). Keep argmax.
- **Remaining errors** (breadcrumb, best configs):
  - backoff n6 "delays grow linearly" (premise says "exponential delays") is kept by base-mnli-fever-anli in every premise mode (p 0.81–0.94). Large rejects it.
  - sonnet retry c10 "a Retry instance can be passed as the retries parameter" is kept by every model with high confidence. This is probably **a wrong gold label** (see run 002), not a model error.
  - Large + local misses haiku backoff c6, c9 and c11 (numbers "0.0s, 1.0s, 2.0s"; "backoff_jitter introduces random variance"): ±1 sentence is sometimes too little context for haiku's long, rephrased claims.

## Status after run 004

Best candidates for SPEC §6.4 grounding, all with the `breadcrumb` prefix:

| option | recall | false keeps | cost (276 pairs, this laptop) |
|---|---|---|---|
| base-mnli-fever-anli + window | 99–100% | 2–3 | ~65 s |
| base-mnli-fever-anli + local | 99% | 2 | ~16 s |
| large + local | 97% | 0 | ~53 s |

Open:
1. **Labels**: human review of `labels.csv`, especially sonnet retry c10 (likely should be entailment → would remove one "false keep" from every model).
2. **More data before deciding** between the three options above: they differ by 1–3 claims out of 139. Add a section from another library, with more negation and number-change negatives.
3. **Local premise radius**: try ±2 or "cited sentence + the paragraph's first sentence" to recover large's misses on long rephrased claims.
4. **Ensemble**: keep only if base-mnli-fever-anli (window) and large (local) both entail. Possibly 0 false keeps at ~99% recall, at the cost of running two models.

## 005-bench-new-families: speed of MiniCheck and HHEM

24 window-400 pairs with breadcrumb, evenly spread by length, 10 threads, batch 8:

| model | pairs/s |
|---|---|
| MiniCheck-DeBERTa-v3-Large | 0.68 |
| HHEM-2.1-open (flan-t5-base) | 2.13 |
| DeBERTa-v3-large-mnli-fever-anli-ling-wanli | 0.62 |
| nli-deberta-v3-base | 1.98 |

MiniCheck-Large costs the same as the large NLI model (same backbone), and HHEM the same as a base model. The estimate for run 006 (571 unique pairs per window size, 5 models, window + local) was ≤ 70 min without the cache, under the 2 h budget.

## 006-realistic-negatives: setup

Goal: test points 1–5 from "Status after run 004", i.e. precision on wrong claims that look realistic, not only hand-made twists.

- **Extractors:** only `sonnet-medium` and `flash-3.6-high` (two vendors, as SPEC §6.4 wants two different extractors).
- **New sections:** `using-timeouts`, `changelog-2-8-0-security`, `changelog-2-8-0-bugfixes` (long, 3 windows @ 400), `httpx-timeouts-fine-tuning` (second library, Markdown).
- **Should-drop claims:**
  - `negative`: 25 new hand-made ones.
  - `outside` / `beyond`: 48 claims from `prompt-outside.md`. 3 of them (sonnet) cite code, so they are `dropped:citation_not_in_prose` before NLI, which is what should happen.
  - `cross`: 259 per window size, each claim checked against the most similar sentence of a related section.
  - `real` claims labelled neutral.
- **Labels:** 186 new drafted ones (142 entailment, 41 neutral, 3 contradiction). Notable: 3 of the "outside" / "beyond" claims are actually supported by the section and were labelled entailment:
  - security sonnet o1 (`proxy_ssl_context`);
  - bugfixes sonnet b2 (gevent);
  - using-timeouts flash b3 (pool-level timeout = default).

  Some httpx "beyond" claims are borderline. An extractor asked to make up unsupported claims does not always manage to.
- **Models:** `cross-encoder/nli-deberta-v3-base` (SPEC reference), `DeBERTa-v3-base-mnli-fever-anli`, `DeBERTa-v3-large-mnli-fever-anli-ling-wanli`, `MiniCheck-DeBERTa-v3-Large`, `HHEM-2.1-open` (code pinned to `de9a5e6`). All with the `breadcrumb` context and `window` + `local` premises.

## 006-realistic-negatives: results

The run took 61 min. All rows are breadcrumb, window 400 (for `local`, 128 and 400 are identical). Recall is over 261 claims that should be kept. "False keeps" is out of 85 should-drop claims (hand-made, outside, beyond, and real claims labelled neutral). Cross pairs (259) are counted separately.

| model + premise | keep recall | false keeps | outside / beyond kept | cross kept | scoring time in this run |
|---|---|---|---|---|---|
| cross-encoder base (SPEC) + window | **60%** | 9 | 1/23, 4/21 | 4 | ~6 min (partly cached) |
| cross-encoder base + local | 92% | 19 | 4/23, 7/21 | 9 | |
| base-mnli-fever-anli + window | 94% | 18 | 6/23, 6/21 | 48 | ~6 min (partly cached) |
| base-mnli-fever-anli + local | 95% | 16 | 5/23, 6/21 | 42 | |
| **large + local** | **98%** | 13 | 4/23, 5/21 | 27 | ~18 min (partly cached) |
| large + window | 100% | 22 | 8/23, 6/21 | 40 | |
| MiniCheck-Large + local | 90% | 14 | **1/23**, 6/21 | **5** | ~24 min (uncached) |
| HHEM + local | 98% | **39** | 6/23, 11/21 | 26 | ~7 min (uncached) |

The per-section numbers, the cross pairs and 2-model ensembles are in `runs/006-realistic-negatives/posthoc/`, computed from the result CSVs.

### What we learned

1. **The SPEC reference setup (cross-encoder base + 400-token window) breaks on changelogs.**
   - It keeps only 33/74 correct claims in Bugfixes, 14/28 in Security and 7/26 in httpx, with p_entailment ≈ 0.00. A window full of unrelated list items drowns out the one sentence that matters.
   - The same model with the `local` premise keeps 73/74 in Bugfixes.
   - The 400-token window as the NLI premise should not be used with a base model.
2. **Large + local is still the best single option:**
   - 98% recall;
   - 13 false keeps, of which 4 have borderline labels;
   - 27 cross pairs kept.
   - Its 6 misses: three haiku paraphrases on the backoff section, security flash c2, httpx sonnet c14, and the borderline httpx flash b1.
3. **Realistic unsupported claims are harder than hand-made ones.**
   - Large + local keeps 4/43 hand-made negatives, but 9/44 outside + beyond claims (20%).
   - Typical kept ones are near-true generalizations of the text:
     - "the timeout passed to request() must be a float";
     - "PoolManager accepts a Timeout object" (only in code);
     - "stream() accepts an amt parameter that controls bytes per chunk";
     - "Destination client certificates no longer apply to HTTPS connections" (drops "forwarding proxy").
4. **Small surface edits of a sentence still pass with p ≈ 1.0.** Large + local keeps:
   - `proxy_ssl_context` → `ssl_context` (security n3);
   - Medium → High severity (n1). The local premise ±1 sentence also contains the neighbouring item's "(High severity)".
   - "will raise an error in v3.0" stated as already happening (bugfixes n2).

   NLI does not reliably check exact identifiers, numbers or tense. A cheap code check would catch these: every identifier, number and version in the claim must appear in the cited span or its sentence.
5. **Cross pairs:** 27 kept by large + local, but about 9 of them are true entailments. The Security and Bugfixes sections describe the same HTTPS-proxy fix, e.g. "destination client certificates no longer apply to forwarding proxy connections" vs "HTTPSConnection no longer applies … client credentials to forwarding proxy handshakes". The others are plausible topic claims judged against the wrong section, e.g. "specifying an integer for retries changes the number of retries" against the backoff prose, p 0.99 for all 5 extractors.
6. **MiniCheck** is the most conservative model:
   - Best on cross (5/259) and outside (1/23).
   - But it drops 10% of correct claims. It refuses claims that carry the version ("In urllib3 2.8.0, … was fixed") when the version is only in the breadcrumb, and it refuses many paraphrases on the backoff section.
   - It still keeps the identifier swaps (n2, n3, n7).
   - Thresholds don't help: ≥ 0.9 gives 5 false keeps but 63% recall.
7. **HHEM keeps 21/43 hand-made negatives.** Not usable as the grounding filter.
8. **Thresholds** still don't help the NLI models (same as run 004).
9. **Ensembles** (keep only if both models say entailment), from the CSVs:

   | ensemble | recall | false keeps | cross |
   |---|---|---|---|
   | large-local alone | 98% | 13 | 27 |
   | large-local + large-window | 97% | 11 | 25 |
   | large-local + base-mnli-local | 94% | 10 | 18 |
   | large-local + MiniCheck-local | 90% | **6** | **5** |

   Each one gives up recall roughly in proportion to the false keeps it removes. None is clearly better. That only changes if a lost correct claim costs much less than a kept wrong one.

## Status after run 006

- **Recommendation for SPEC §6.4:** `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`, with the `breadcrumb` prefix and the **cited sentence ±1** as premise (not the 400-token window), argmax.
  - About 0.6 s per claim on this laptop.
  - Fallback if that's too slow: `DeBERTa-v3-base-mnli-fever-anli` + local (95% recall, slightly more false keeps).
  - Replace `cross-encoder/nli-deberta-v3-base` + window: it fails on list-heavy sections.
- NLI alone lets through about 15% of should-drop claims. Two cheap additions are worth testing before adding a second model:
  - (a) a code check that the claim's identifiers, numbers and versions appear in the cited sentence;
  - (b) for "beyond"-style claims, nothing cheap; accept them or use the K5a claim-vs-claim check between the two extractors.

Open:
1. Human review of `labels.csv`: the 186 new drafts, especially the borderline outside/beyond ones and sonnet retry c10.
2. Re-label the ~9 cross pairs that are true entailments, so cross counts only real errors.
3. Prototype the identifier/number check (a) and measure it on these 85 should-drop claims and 261 correct ones.
4. Breadcrumb into `local` for MiniCheck: the version is in the breadcrumb, but MiniCheck seems to ignore it.
