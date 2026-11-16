"""Parse an OpenAPI 3.x file and check it against the OpenAPI schema.

Validation problems are collected, not raised: real specs are rarely perfect, and one bad
corner must not stop the whole target.
"""

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import orjson
import yaml
from openapi_spec_validator import (
    OpenAPIV30SpecValidator,
    OpenAPIV31SpecValidator,
    OpenAPIV32SpecValidator,
)
from openapi_spec_validator.validation.validators import SpecValidator

MAX_PROBLEMS = 100
_MAX_MESSAGE = 300

_VALIDATORS: dict[str, type[SpecValidator]] = {
    "3.0": OpenAPIV30SpecValidator,
    "3.1": OpenAPIV31SpecValidator,
    "3.2": OpenAPIV32SpecValidator,
}


class SpecLoadError(Exception):
    """The file can't be used at all: not parseable, not a mapping, or not OpenAPI 3.x."""


class _Loader(yaml.CSafeLoader):
    """libyaml-backed safe loader that reads scalars the way JSON would.

    PyYAML follows YAML 1.1, where `2024-01-01` becomes a date and `on` / `yes` become booleans.
    That silently changes enum values and examples, so dates stay strings and only
    true / false are booleans (YAML 1.2 behaviour).
    """


_TIMESTAMP_TAG = "tag:yaml.org,2002:timestamp"
_BOOL_TAG = "tag:yaml.org,2002:bool"
_YAML12_BOOL = re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$")

_Loader.yaml_implicit_resolvers = {
    first: [
        (tag, _YAML12_BOOL if tag == _BOOL_TAG else regexp)
        for tag, regexp in resolvers
        if tag != _TIMESTAMP_TAG
    ]
    for first, resolvers in yaml.CSafeLoader.yaml_implicit_resolvers.items()
}


@dataclass(frozen=True)
class LoadedSpec:
    document: dict[str, Any]
    openapi_version: str  # as written in the file, e.g. "3.1.0"
    problems: tuple[str, ...]  # first MAX_PROBLEMS validation problems, sorted
    problem_count: int  # all problems, including the ones not kept


def parse_spec(data: bytes, name: str = "") -> dict[str, Any]:
    """Parse JSON or YAML bytes into a dict with string keys.

    `name` is only used to pick the parser (`.json` → orjson, `.yaml` / `.yml` → YAML);
    without a known suffix, content starting with `{` is parsed as JSON.
    """
    suffix = Path(name).suffix.lower()
    as_json = suffix == ".json" or (suffix not in (".yaml", ".yml") and data.lstrip()[:1] == b"{")
    try:
        doc = orjson.loads(data) if as_json else yaml.load(data, Loader=_Loader)
    except (orjson.JSONDecodeError, yaml.YAMLError) as exc:
        raise SpecLoadError(f"cannot parse {name or 'spec'}: {exc}") from exc
    if not isinstance(doc, dict):
        raise SpecLoadError(f"{name or 'spec'}: top level is not a mapping")
    result: dict[str, Any] = _stringify_keys(doc)
    return result


def load_spec_bytes(data: bytes, name: str = "", *, validate: bool = True) -> LoadedSpec:
    """Parse and (optionally) validate a spec held in memory, e.g. from `git show`."""
    document = parse_spec(data, name)
    if "swagger" in document:
        raise SpecLoadError(f"{name or 'spec'}: Swagger 2.0 is not supported, only OpenAPI 3.x")
    version = document.get("openapi")
    if not isinstance(version, str) or version[:3] not in _VALIDATORS:
        raise SpecLoadError(f"{name or 'spec'}: unsupported openapi version {version!r}")
    problems: list[str] = validate_spec(document, version) if validate else []
    return LoadedSpec(
        document=document,
        openapi_version=version,
        problems=tuple(problems[:MAX_PROBLEMS]),
        problem_count=len(problems),
    )


def load_spec(path: str | Path, *, validate: bool = True) -> LoadedSpec:
    """Read, parse and (optionally) validate one spec file.

    Validation of very large specs (GitHub) is slow; pass `validate=False` to skip it.
    """
    path = Path(path)
    return load_spec_bytes(path.read_bytes(), path.name, validate=validate)


def validate_spec(document: Mapping[str, Any], version: str) -> list[str]:
    """Return all validation problems as sorted `pointer: message` lines. Never raises."""
    validator = _VALIDATORS[version[:3]](document)
    problems: list[str] = []
    try:
        for error in validator.iter_errors():
            pointer = "#" + "".join("/" + _escape(str(p)) for p in error.path)
            problems.append(f"{pointer}: {_short(error.message)}")
    except Exception as exc:  # the validator itself crashes on some broken specs
        problems.append(f"#: validator stopped: {type(exc).__name__}: {_short(str(exc))}")
    return sorted(set(problems))


def _escape(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def _short(message: str) -> str:
    return message if len(message) <= _MAX_MESSAGE else message[:_MAX_MESSAGE] + "…"


def _stringify_keys(node: Any) -> Any:
    """YAML allows non-string keys (`200:` is an int). JSON and OpenAPI don't, so convert them."""
    if isinstance(node, dict):
        return {_key(k): _stringify_keys(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_stringify_keys(v) for v in node]
    return node


def _key(key: Any) -> str:
    if isinstance(key, str):
        return key
    if isinstance(key, bool):
        return "true" if key else "false"
    if key is None:
        return "null"
    return str(key)
