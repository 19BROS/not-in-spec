"""Canonical JSON: the one serialization for anything that is hashed or kept as a golden file."""

import hashlib
from typing import Any

import orjson

_CANONICAL = orjson.OPT_SORT_KEYS
_PRETTY = orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2 | orjson.OPT_APPEND_NEWLINE


def canonical_json(obj: Any, *, pretty: bool = False) -> bytes:
    """Serialize with sorted keys and fixed separators. Dataclasses and tuples are supported."""
    return orjson.dumps(obj, option=_PRETTY if pretty else _CANONICAL)


def content_hash(obj: Any) -> str:
    """sha256 of the canonical JSON, as a hex string."""
    return hashlib.sha256(canonical_json(obj)).hexdigest()
