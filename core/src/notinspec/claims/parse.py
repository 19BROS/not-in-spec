"""Parsing the extractor's answer. Deterministic; lenient only where stated here.

- A Groq schema rejection (`json_validate_failed`) fails the chunk; it is `truncated` when Groq
  says the completion limit was reached.
- One Markdown code fence around the whole answer is stripped (models without structured output
  wrap JSON in one).
- The answer must be a JSON object with a `claims` list. Anything else fails the whole chunk
  (`malformed-output`, or `truncated` when the provider cut the answer off).
- A single invalid claim (missing or empty field, unknown type, repeated id) is skipped with a
  problem; the other claims of the answer are kept. Extra fields in a claim are ignored.
- `type` is matched case-insensitively. Claim text is stripped; the citation is kept exactly as
  returned except for surrounding whitespace, because the citation check needs the model's span.
"""

import json
import re
from dataclasses import dataclass
from typing import Any

from notinspec.claims.model import ClaimType, ExtractionCause, RawClaim
from notinspec.runner.openai_compat import SCHEMA_FAILED

_FENCE = re.compile(r"\A\s*```[A-Za-z]*[ \t]*\n(.*?)\n?```\s*\Z", re.DOTALL)
_TYPES: dict[str, ClaimType] = {"fact": "fact", "change": "change"}


@dataclass(frozen=True)
class ParsedClaims:
    """`cause` is None when the answer parsed; then `claims` may still be empty."""

    claims: tuple[RawClaim, ...]
    problems: tuple[str, ...] = ()
    cause: ExtractionCause | None = None
    detail: str = ""


def parse_claims(
    content: str | None, *, refusal: str | None = None, finish_reason: str | None = None
) -> ParsedClaims:
    if refusal:
        return ParsedClaims((), cause="refusal", detail=refusal[:300])
    if finish_reason == SCHEMA_FAILED:
        # Groq rejected the answer against the schema; `content` is its `failed_generation`,
        # which is either the model's output or Groq's own message
        generation = (content or "").strip()
        cut = "max completion tokens" in generation
        return ParsedClaims(
            (),
            cause="truncated" if cut else "malformed-output",
            detail=f"{SCHEMA_FAILED}: {generation[:200] or 'empty'}",
        )
    if content is None or not content.strip():
        cause: ExtractionCause = "truncated" if finish_reason == "length" else "malformed-output"
        return ParsedClaims((), cause=cause, detail="empty answer")
    text = content.strip()
    if fenced := _FENCE.match(text):
        text = fenced.group(1)
    try:
        data = json.loads(text)
    except ValueError as e:
        cause = "truncated" if finish_reason == "length" else "malformed-output"
        return ParsedClaims((), cause=cause, detail=f"not JSON: {e}")
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        return ParsedClaims((), cause="malformed-output", detail="no `claims` list")
    claims: list[RawClaim] = []
    problems: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(data["claims"]):
        claim, problem = _claim(item)
        if claim is not None and claim.local_id in seen:
            problem = f"repeated id {claim.local_id!r}"
            claim = None
        if claim is None:
            problems.append(f"claim {index + 1}: {problem}")
            continue
        seen.add(claim.local_id)
        claims.append(claim)
    return ParsedClaims(tuple(claims), tuple(problems))


def _claim(item: Any) -> tuple[RawClaim | None, str]:
    if not isinstance(item, dict):
        return None, "not an object"
    fields: dict[str, str] = {}
    for name in ("id", "claim", "citation", "type"):
        value = item.get(name)
        if not isinstance(value, str) or not value.strip():
            return None, f"missing or empty `{name}`"
        fields[name] = value.strip()
    claim_type = _TYPES.get(fields["type"].lower())
    if claim_type is None:
        return None, f"unknown type {fields['type']!r}"
    return RawClaim(
        fields["id"], " ".join(fields["claim"].split()), fields["citation"], claim_type
    ), ""
