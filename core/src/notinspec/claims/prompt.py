"""The claim extractor's prompt and answer schema (SPEC §6.4 step 1).

Ported from `experiments/nli/prompt.md`, the prompt the NLI experiments were run on. Changes:
rule 4 also names signatures and tables (SPEC §6.4: a citation found only there is not
checkable), and the output section relies on structured output instead of a code fence.
Bump `PROMPT_VERSION` (model.py) with any change here.
"""

from typing import Any

from notinspec.chunking import Chunk
from notinspec.claims.model import PROMPT_VERSION, ExtractorSpec
from notinspec.runner import ChatRequest, Message

CLAIMS_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ExtractedClaims",
    "type": "object",
    "properties": {
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "claim": {"type": "string"},
                    "citation": {"type": "string"},
                    "type": {"type": "string", "enum": ["fact", "change"]},
                },
                "required": ["id", "claim", "citation", "type"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["claims"],
    "additionalProperties": False,
}

_TEMPLATE = """\
You are a claim extractor for a documentation-quality tool. You read one section of software \
documentation and list the atomic facts its prose states about the software.

## Section

Project: {{PROJECT}}
Location in the docs: {{BREADCRUMB}}

<section>
{{CHUNK}}
</section>

## What a claim is

A claim is one atomic, self-contained statement of fact that the **prose** of the section makes \
about the software: behaviour, defaults, units, value ranges, allowed values, what a parameter \
or option does, when an error is raised, what changed between versions.

## Rules

1. **Atomic.** One fact per claim. "retries 3 times and follows up to 3 redirects" is two claims.
2. **Self-contained.** A claim must be understandable without the section. Name the subject \
explicitly (library, class, function, parameter). No "it", "this", "the class", "the \
parameter". Use the location in the docs to resolve what the section is about.
3. **Faithful.** State only what the prose says. Add nothing from your own knowledge of the \
software, do not generalise, and do not weaken or strengthen the statement. Keep qualifiers \
("can", "by default", "up to", "only"), negations, numbers and units exactly.
4. **Prose only.** Code blocks, signatures and tables are shown for context only. A fact that \
appears only in code, a code comment, a signature or a table is not a claim.
5. **Citation.** For every claim, copy the shortest contiguous span of the section's prose that \
supports it, character for character: keep backticks, punctuation and spelling, fix nothing, \
no "...". It may be part of a sentence but must contain the evidence.
6. **Type.** `change` if the claim says something was added, removed, renamed, replaced or \
deprecated in some version; otherwise `fact`.
7. **Skip** navigation and lead-ins ("see X", "for example:", "the following code"), opinions \
and marketing. An instruction that implies a fact *is* a claim: "To disable redirects, specify \
`redirect=False`" → "Passing redirect=False disables redirects."
8. No duplicates.

## Example (a different project)

Section prose: "`connect()` accepts an optional `timeout` parameter in seconds, default 30. \
Since 2.0, `retries` is replaced by the new `retry_policy`."

```json
{"claims": [
  {"id": "c1", "claim": "The timeout parameter of connect() is optional.", "citation": \
"`connect()` accepts an optional `timeout` parameter", "type": "fact"},
  {"id": "c2", "claim": "The timeout parameter of connect() is given in seconds.", "citation": \
"`timeout` parameter in seconds", "type": "fact"},
  {"id": "c3", "claim": "The default value of the timeout parameter of connect() is 30 \
seconds.", "citation": "in seconds, default 30", "type": "fact"},
  {"id": "c4", "claim": "Since version 2.0, the retries parameter is replaced by the \
retry_policy parameter.", "citation": "Since 2.0, `retries` is replaced by the new \
`retry_policy`", "type": "change"}
]}
```

## Output

Return only one JSON object of this shape, with no text before or after it. If the prose states \
no facts, return {"claims": []}.

{"claims": [{"id": "c1", "claim": "...", "citation": "...", "type": "fact"}]}
"""


def project_of(chunk: Chunk) -> str:
    """The breadcrumb starts with the project, which never contains '>' (config check)."""
    return chunk.breadcrumb.split(" > ", 1)[0]


def render_prompt(chunk: Chunk) -> str:
    # the chunk last, so text inside it that looks like a placeholder is never replaced
    text = _TEMPLATE.replace("{{PROJECT}}", project_of(chunk))
    text = text.replace("{{BREADCRUMB}}", chunk.breadcrumb)
    return text.replace("{{CHUNK}}", chunk.text.strip("\n"))


def build_request(chunk: Chunk, spec: ExtractorSpec) -> ChatRequest:
    if spec.prompt_version != PROMPT_VERSION:
        raise ValueError(
            f"extractor {spec.name}: prompt version {spec.prompt_version} is not available "
            f"(this code has version {PROMPT_VERSION})"
        )
    return ChatRequest(
        model=spec.model,
        messages=(Message("user", render_prompt(chunk)),),
        temperature=0.0,
        max_tokens=spec.max_tokens,
        response_schema=CLAIMS_SCHEMA,
        reasoning_effort=spec.reasoning_effort,
    )
