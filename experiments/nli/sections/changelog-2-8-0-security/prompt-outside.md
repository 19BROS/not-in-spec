You are helping to test a documentation-quality tool. The tool extracts claims from one section of software documentation and must reject any claim that the section's prose does not state. Your job is to write realistic claims that it should reject.

## Section

Project: urllib3
Location in the docs: Changelog > 2.8.0 (2026-09-15) > Security

<section>
### Security

Fixed the following security issues:

- The TLS configuration for HTTPS proxies could be ignored or overridden. (High severity, GHSA-8988-9cw3-xx77)

- `HTTPResponse.stream()` and `read_chunked()` could buffer a chunk-size line of unbounded length in memory. (High severity, GHSA-vxq7-64xx-v4gw)

- Chunked Deflate streaming could enter an infinite loop. (Medium severity, GHSA-gh4c-6fx4-qh6g)

> **Caution:** urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. Configurations relying on that behavior may require changes.
>
> Configure proxy CA certificates and client certificates in `proxy_ssl_context`, and proxy identity checks with `proxy_assert_hostname` or `proxy_assert_fingerprint`. Destination client certificates and identity overrides no longer apply to HTTPS forwarding proxy connections.
</section>

## Task

Write 6 claims about urllib3 that a careless claim extractor could plausibly produce from this section, but that the section's **prose** does **not** state:

- 3 claims that are **true for the real urllib3** (from your own knowledge, from another part of its documentation, or only visible in the code blocks) but are not stated in the prose of this section.
- 3 claims that **sound like they come from this section** but subtly go beyond it: an over-generalisation, a stronger or weaker qualifier ("always" for "can", "only" added or dropped), a cause or purpose the text does not give, or a detail merged from two different sentences in a way the text does not say.

Do not write claims that contradict the section outright (no changed numbers, no plain negations). Those are covered elsewhere.

Each claim must look like a normal extractor output: atomic, self-contained (name the subject explicitly), one sentence, no hedging. For each claim give a **citation**: the shortest span of the section's prose that the claim would most plausibly be attributed to, copied character for character (keep backticks and punctuation, fix nothing, no "..."). Add `"kind": "outside"` for the first group and `"kind": "beyond"` for the second.

## Output

Return only the JSON object inside one ```json code block, with no text before or after it. It must be valid JSON: use only straight ASCII quotes (`"` and `'`), never typographic quotes such as “ ” ‘ ’, also inside claims (write `urllib3's`, not `urllib3’s`).

```json
{"claims": [{"id": "o1", "claim": "...", "citation": "...", "type": "fact", "kind": "outside"}]}
