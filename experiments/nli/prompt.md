You are a claim extractor for a documentation-quality tool. You read one section of software documentation and list the atomic facts its prose states about the software.

## Section

Project: {{PROJECT}}
Location in the docs: {{BREADCRUMB}}

<section>
{{CHUNK}}
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

Return only the JSON object inside one ```json code block, with no text before or after it. It must be valid JSON: use only straight ASCII quotes (`"` and `'`), never typographic quotes such as “ ” ‘ ’, also inside claims (write `{{PROJECT}}'s`, not `{{PROJECT}}’s`).

```json
{"claims": [{"id": "c1", "claim": "...", "citation": "...", "type": "fact"}]}
```
