You are a claim extractor for a documentation-quality tool. You read one section of software documentation and list the atomic facts its prose states about the software.

## Section

Project: urllib3
Location in the docs: User Guide > Retrying Requests > Configuring Exponential Backoff

<section>
### Configuring Exponential Backoff

By default, `Retry` does not sleep between retry attempts (`backoff_factor=0`), though it will still respect delays requested by the server when a response includes a `Retry-After` header (see `respect_retry_after_header`). In production systems, retrying immediately without backoff can overwhelm a recovering server or quickly exhaust API rate limits.

When no server-requested delay is applied, you can set a non-zero `backoff_factor` to introduce exponential delays between retries. The sleep delay is calculated using the formula:

```
{backoff factor} * (2 ** ({number of previous retries}))
```

seconds, with no delay before the second attempt (the first retry) because most transient errors resolve immediately. For example, a `backoff_factor` of `0.5` yields retry sleeps of `0.0s`, `1.0s`, `2.0s`, etc., up to `backoff_max`:

```python
import urllib3

# Retries wait 0.0s (immediate 2nd attempt), 1.0s, and 2.0s (plus jitter)
retries = urllib3.Retry(
    total=3,
    backoff_factor=0.5,
    backoff_jitter=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
)
http = urllib3.PoolManager(retries=retries)
```

Adding `backoff_jitter` introduces random variance to avoid the "thundering herd" problem where many clients retry in lockstep against a server.
</section>

## What a claim is

A claim is one atomic, self-contained statement of fact that the **prose** of the section makes about the software: behaviour, defaults, units, value ranges, allowed values, what a parameter or option does, when an error is raised, what changed between versions.

## Rules

1. **Atomic.** One fact per claim. "retries 3 times and follows up to 3 redirects" is two claims.
2. **Self-contained.** A claim must be understandable without the section. Name the subject explicitly (library, class, function, parameter). No "it", "this", "the class", "the parameter". Use the location in the docs to resolve what the section is about.
3. **Faithful.** State only what the prose says. Add nothing from your own knowledge of the software, do not generalise, and do not weaken or strengthen the statement. Keep qualifiers ("can", "by default", "up to", "only"), negations, numbers and units exactly.
4. **Prose only.** Code blocks are shown for context only. A fact that appears only in code or in a code comment is not a claim.
5. **Citation.** For every claim, copy the shortest contiguous span of the section's prose that supports it, character for character: keep backticks, punctuation and spelling, fix nothing, no "...". It may be part of a sentence but must contain the evidence.
6. **Type.** `change` if the claim says something was added, removed, renamed, replaced or deprecated in some version; otherwise `fact`.
7. **Skip** navigation and lead-ins ("see X", "for example:", "the following code"), opinions and marketing. An instruction that implies a fact *is* a claim: "To disable redirects, specify `redirect=False`" → "Passing redirect=False disables redirects."
8. No duplicates.

## Example (a different project)

Section prose: "`connect()` accepts an optional `timeout` parameter in seconds, default 30. Since 2.0, `retries` is replaced by the new `retry_policy`."

```json
{"claims": [
  {"id": "c1", "claim": "The timeout parameter of connect() is optional.", "citation": "`connect()` accepts an optional `timeout` parameter", "type": "fact"},
  {"id": "c2", "claim": "The timeout parameter of connect() is given in seconds.", "citation": "`timeout` parameter in seconds", "type": "fact"},
  {"id": "c3", "claim": "The default value of the timeout parameter of connect() is 30 seconds.", "citation": "in seconds, default 30", "type": "fact"},
  {"id": "c4", "claim": "Since version 2.0, the retries parameter is replaced by the retry_policy parameter.", "citation": "Since 2.0, `retries` is replaced by the new `retry_policy`", "type": "change"}
]}
```

## Output

Return only the JSON object inside one ```json code block, with no text before or after it. It must be valid JSON: use only straight ASCII quotes (`"` and `'`), never typographic quotes such as “ ” ‘ ’, also inside claims (write `urllib3's`, not `urllib3’s`).

```json
{"claims": [{"id": "c1", "claim": "...", "citation": "...", "type": "fact"}]}
```
