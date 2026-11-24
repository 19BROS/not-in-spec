"""SPEC §10 identity; tagged references also identify the question's subject and choices."""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

from notinspec.adapters.canonical import content_hash

if TYPE_CHECKING:
    from notinspec.tasks.models import Reference, TestItem


def identity_key(
    project: str, chunk_id: str, level: str, operator_version: int, reference: Reference
) -> dict[str, object]:
    return {
        "project": project,
        "chunk_id": chunk_id,
        "level": level,
        "operator": None,
        "operator_version": operator_version,
        "format": "python",
        "difficulty": "explicit-single-step",
        "source_example_id": None,
        "reference": asdict(reference),
    }


def item_id(item: TestItem) -> str:
    return content_hash(
        identity_key(item.project, item.chunk_id, item.level, item.operator_version, item.reference)
    )
