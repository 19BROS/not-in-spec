"""Versioned local candidate exports, not a golden-set approval or a database store."""

import json
from dataclasses import asdict, fields
from pathlib import Path
from typing import Any

from notinspec.adapters.canonical import canonical_json
from notinspec.inventory import Source
from notinspec.tasks.models import (
    ChoiceReference,
    ClaimReference,
    DefaultReference,
    ExistsReference,
    GenerationResult,
    Option,
    PathReference,
    Reference,
    RequiredParametersReference,
    SkippedTask,
    Subject,
    TaskText,
    TestItem,
)

SCHEMA_VERSION = 3
_REFERENCES: dict[str, type[Reference]] = {
    "exists": ExistsReference,
    "choice": ChoiceReference,
    "required-parameters": RequiredParametersReference,
    "default": DefaultReference,
    "path": PathReference,
    "claim": ClaimReference,
}


def reference_json(reference: Reference) -> bytes:
    # orjson's native dataclass path omits class-level init=False defaults (kind tags).
    return canonical_json(asdict(reference))


def _record(value: Any, cls: Any, extra: tuple[str, ...] = ()) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {f.name for f in fields(cls)} | set(extra):
        raise ValueError(f"invalid {cls.__name__} fields")
    return dict(value)


def _array(value: Any) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError("expected a JSON array")
    return value


def _reference(value: Any) -> Reference:
    if not isinstance(value, dict) or not isinstance(value.get("kind"), str):
        raise ValueError("reference needs a kind tag")
    cls = _REFERENCES.get(value["kind"])
    if cls is None:
        raise ValueError("unknown reference kind")
    data = _record(value, cls)
    data.pop("kind")
    data["subject"] = Subject(**_record(data["subject"], Subject))
    if cls is ChoiceReference:
        data["options"] = tuple(Option(**_record(o, Option)) for o in _array(data["options"]))
    if cls is RequiredParametersReference:
        data["names"] = tuple(_array(data["names"]))
    return cls(**data)


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reference_from_json(data: bytes | str) -> Reference:
    return _reference(json.loads(data, object_pairs_hook=_unique_pairs))


def _source(value: Any) -> Source:
    data = _record(value, Source)
    if data["type"] not in ("spec", "signature", "example", "changelog", "claim"):
        raise ValueError("invalid source type")
    for key in ("section_id", "pointer"):
        if data[key] is not None and (not isinstance(data[key], str) or not data[key].strip()):
            raise ValueError("invalid source location")
    return Source(**data)


def _item(value: Any) -> TestItem:
    data = _record(value, TestItem, ("id",))
    expected_id = data.pop("id")
    data["reference"] = _reference(data["reference"])
    data["sources"] = tuple(_source(s) for s in _array(data["sources"]))
    data["chunk_ids"] = tuple(_array(data["chunk_ids"]))
    wording = _record(data["wording"], TaskText)
    wording["paraphrases"] = tuple(_array(wording["paraphrases"]))
    data["wording"] = TaskText(**wording)
    item = TestItem(**data)
    if item.id != expected_id:
        raise ValueError("item identity does not match its deterministic fields")
    return item


def dumps(result: GenerationResult) -> bytes:
    return canonical_json(
        {
            "schema_version": SCHEMA_VERSION,
            "items": [
                {**asdict(item), "id": item.id} for item in sorted(result.items, key=lambda i: i.id)
            ],
            "skipped": sorted(result.skipped, key=canonical_json),
        },
        pretty=True,
    )


def loads(data: bytes | str) -> GenerationResult:
    value = json.loads(data, object_pairs_hook=_unique_pairs)
    if not isinstance(value, dict) or set(value) != {"schema_version", "items", "skipped"}:
        raise ValueError("invalid task export")
    if type(value["schema_version"]) is not int or value["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported task schema version")
    items = tuple(_item(item) for item in _array(value["items"]))
    if len({item.id for item in items}) != len(items):
        raise ValueError("duplicate item identity")
    skipped = tuple(SkippedTask(**_record(s, SkippedTask)) for s in _array(value["skipped"]))
    return GenerationResult(
        tuple(sorted(items, key=lambda i: i.id)), tuple(sorted(skipped, key=canonical_json))
    )


def save(path: Path, result: GenerationResult) -> None:
    payload = dumps(result)
    with path.open("xb") as stream:  # never replace an existing task export
        stream.write(payload)


def load(path: Path) -> GenerationResult:
    return loads(path.read_bytes())
