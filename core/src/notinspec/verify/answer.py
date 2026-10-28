"""The model's answer to a hard task: a structured HTTP request (SPEC §2.5).

Parsing is deterministic and lenient only where stated here: one Markdown code fence around the
whole answer is stripped, the method is upper-cased, and a null `query` / `headers` means empty.
Anything else that doesn't match `ANSWER_SCHEMA` is `malformed-output`. A model that declines
without producing JSON is `refusal`.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Any

from notinspec.verify.causes import FailureCause

# bump when the parsing rules change; recorded with every result, like the generator version
PARSER_VERSION = 1

METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")

type Scalar = str | int | float | bool
type QueryValue = Scalar | list[Scalar]
type Json = None | bool | int | float | str | list[Json] | dict[str, Json]

_SCALAR_SCHEMA: dict[str, Any] = {"type": ["string", "number", "boolean"]}

# sent to the model as the structured-output schema; parse_answer enforces the same shape
ANSWER_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ProposedRequest",
    "type": "object",
    "properties": {
        "method": {"type": "string", "enum": list(METHODS)},
        "path": {"type": "string", "pattern": "^/"},
        "query": {
            "type": "object",
            "additionalProperties": {
                "anyOf": [_SCALAR_SCHEMA, {"type": "array", "items": _SCALAR_SCHEMA}]
            },
        },
        "headers": {"type": "object", "additionalProperties": {"type": "string"}},
        "body": {},
    },
    "required": ["method", "path"],
    "additionalProperties": False,
}

_FIELDS = frozenset(ANSWER_SCHEMA["properties"])
_FENCE = re.compile(r"\A```[A-Za-z]*[ \t]*\n(.*?)\n?```\Z", re.DOTALL)
_REFUSAL = re.compile(
    r"\b(i can(?:not|[’']t)|i(?: am|[’']m) (?:unable|not able)|i do(?: not|n[’']t) know"
    r"|i(?: am|[’']m) sorry|i apologi[sz]e|unable to (?:help|assist|answer))\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ProposedRequest:
    method: str
    path: str
    query: dict[str, QueryValue] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    body: Json = None


@dataclass(frozen=True)
class ParsedAnswer:
    """Exactly one of `request` and `cause` is set."""

    request: ProposedRequest | None
    cause: FailureCause | None = None
    detail: str = ""


class _Invalid(ValueError):
    pass


def parse_answer(content: str | None, *, refusal: str | None = None) -> ParsedAnswer:
    """Parse a model's reply. `refusal` is the provider's own refusal field, if it set one."""
    if refusal:
        return _failed(FailureCause.REFUSAL, refusal)
    text = (content or "").strip()
    if not text:
        return _failed(FailureCause.MALFORMED_OUTPUT, "empty response")
    if fenced := _FENCE.match(text):
        text = fenced.group(1).strip()
    try:
        data = json.loads(text, parse_constant=_reject_constant)
    except (json.JSONDecodeError, _Invalid) as e:
        if _REFUSAL.search(text):
            return _failed(FailureCause.REFUSAL, text[:200])
        detail = e.msg if isinstance(e, json.JSONDecodeError) else str(e)
        return _failed(FailureCause.MALFORMED_OUTPUT, f"not JSON: {detail}")
    try:
        return ParsedAnswer(_to_request(data))
    except _Invalid as e:
        return _failed(FailureCause.MALFORMED_OUTPUT, str(e))


def _failed(cause: FailureCause, detail: str) -> ParsedAnswer:
    return ParsedAnswer(None, cause, detail)


def _reject_constant(name: str) -> None:
    raise _Invalid(f"{name} is not valid JSON")


def _to_request(data: object) -> ProposedRequest:
    if not isinstance(data, dict):
        raise _Invalid(f"expected a JSON object, got {_json_type(data)}")
    if extra := sorted(set(data) - _FIELDS):
        raise _Invalid(f"unknown field(s): {', '.join(extra)}")

    method = data.get("method")
    if not isinstance(method, str) or method.upper() not in METHODS:
        raise _Invalid(f"method must be one of {', '.join(METHODS)}")
    path = data.get("path")
    if not isinstance(path, str) or not path.startswith("/"):
        raise _Invalid("path must be a string starting with '/'")

    query = _or_empty(data.get("query"))
    if not isinstance(query, dict):
        raise _Invalid(f"query must be an object, got {_json_type(query)}")
    for name, value in query.items():
        if not _is_scalar(value) and not (
            isinstance(value, list) and all(_is_scalar(v) for v in value)
        ):
            raise _Invalid(f"query.{name} must be a scalar or a list of scalars")

    headers = _or_empty(data.get("headers"))
    if not isinstance(headers, dict):
        raise _Invalid(f"headers must be an object, got {_json_type(headers)}")
    for name, value in headers.items():
        if not isinstance(value, str):
            raise _Invalid(f"headers.{name} must be a string, got {_json_type(value)}")

    return ProposedRequest(method.upper(), path, query, headers, data.get("body"))


def _or_empty(value: object) -> object:
    return {} if value is None else value


def _is_scalar(value: object) -> bool:
    return isinstance(value, str | int | float | bool)


def _json_type(value: object) -> str:
    match value:
        case None:
            return "null"
        case bool():
            return "boolean"
        case int() | float():
            return "number"
        case str():
            return "string"
        case list():
            return "array"
        case _:
            return "object"
