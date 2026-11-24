"""Test items, review decisions and golden-set versions in the database (SPEC §2.5, §10).

Everything here only inserts: `test_item`, `review_decision` and the three golden-set tables are
append-only. An item's state is its latest review decision, derived on read; an item without
one is a candidate. The functions work inside the caller's session (one transaction).

Concurrent writers are safe: inserts use `ON CONFLICT DO NOTHING` on the unique keys, then read
the row that won.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Literal

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import distinct_on, insert
from sqlalchemy.orm import Session

from notinspec.db import models, rows
from notinspec.tasks import TestItem
from notinspec.tasks.generation import trusted

AUTO = "auto"  # reviewer of an automatic approval
PR_CLOSED = "pr-closed"  # reviewer of a candidate whose PR was closed without merging

type State = Literal["candidate", "approved", "rejected"]


@dataclass(frozen=True)
class Stored:
    """What `store_items` did with one item."""

    identity_key: str
    test_item_id: int
    new: bool  # False: an item with this identity key existed and was reused


def store_items(
    session: Session,
    project: models.Project,
    items: Iterable[TestItem],
    *,
    run: models.Run | None = None,
) -> list[Stored]:
    """Store generated items; an item whose identity key exists is reused, not stored again.

    A reused item keeps its stored task text and its review decisions (SPEC §10). A new item
    whose reference comes from a spec or a signature is approved automatically (SPEC §2.5); the
    rest wait for review. Each item's `input_snapshot_hash` must name a stored input snapshot of
    the project.
    """
    items = list(items)
    for item in items:
        if item.project != project.slug:
            raise ValueError(f"item {item.id} belongs to {item.project}, not {project.slug}")
    snapshots = _snapshots(session, project, {i.input_snapshot_hash for i in items})
    stored: dict[str, Stored] = {}
    for item in items:
        if item.id in stored:
            continue
        row = rows.test_item(
            rows.item_doc(item),
            project_id=project.id,
            input_snapshot_id=snapshots[item.input_snapshot_hash],
            origin_run_id=run.id if run is not None else None,
        )
        new_id = session.scalar(
            insert(models.TestItem)
            .values(_values(row))
            .on_conflict_do_nothing(index_elements=["project_id", "identity_key"])
            .returning(models.TestItem.id)
        )
        if new_id is not None:
            if trusted(item.sources):
                session.add(
                    models.ReviewDecision(
                        test_item_id=new_id,
                        decision="approved",
                        reviewer=AUTO,
                        reason="reference from a spec or a signature",
                    )
                )
            stored[item.id] = Stored(item.id, new_id, True)
        else:
            stored[item.id] = Stored(item.id, _item_id(session, project, item.id), False)
    session.flush()
    return list(stored.values())


def existing_items(session: Session, project: models.Project) -> list[TestItem]:
    """Every stored item of the project, for the generators' `existing` (reuse of task text)."""
    found = session.execute(
        select(models.TestItem, models.InputSnapshot.input_hash)
        .join(models.InputSnapshot, models.InputSnapshot.id == models.TestItem.input_snapshot_id)
        .where(models.TestItem.project_id == project.id)
        .order_by(models.TestItem.id)
    )
    return [
        rows.item_from_row(row, project=project.slug, input_hash=input_hash)
        for row, input_hash in found
    ]


def review(
    session: Session,
    project: models.Project,
    identity_key: str,
    decision: Literal["approved", "rejected"],
    reviewer: str,
    reason: str | None = None,
) -> models.ReviewDecision:
    """Record a decision; an earlier one is never changed, the latest one counts."""
    if decision not in models.DECISIONS:
        raise ValueError(f"decision must be one of {', '.join(models.DECISIONS)}: {decision!r}")
    if not reviewer.strip():
        raise ValueError("a decision needs a reviewer")
    row = models.ReviewDecision(
        test_item_id=_item_id(session, project, identity_key),
        decision=decision,
        reviewer=reviewer.strip(),
        reason=reason,
    )
    session.add(row)
    session.flush()
    return row


def states(session: Session, project: models.Project) -> dict[str, State]:
    """Identity key → state of every item of the project: its latest decision, or candidate.

    Latest is the highest row ID: `created_at` is the same for every row of one transaction.
    """
    latest = (
        select(models.ReviewDecision.test_item_id, models.ReviewDecision.decision)
        .ext(distinct_on(models.ReviewDecision.test_item_id))
        .order_by(models.ReviewDecision.test_item_id, models.ReviewDecision.id.desc())
        .subquery()
    )
    found = session.execute(
        select(models.TestItem.identity_key, latest.c.decision)
        .outerjoin(latest, latest.c.test_item_id == models.TestItem.id)
        .where(models.TestItem.project_id == project.id)
    )
    return {key: decision or "candidate" for key, decision in found}


def golden_set_version(
    session: Session,
    project: models.Project,
    *,
    input_hash: str,
    generator_version: int,
    identity_keys: Iterable[str],
    commit_sha: str | None = None,
) -> tuple[models.GoldenSetVersion, bool]:
    """The golden-set version of these inputs and generator; True when it was created now.

    `identity_keys` are the items generated for these inputs; the approved ones form the
    version, the others join a later one. A version is frozen once created: called again for
    the same inputs and generator (a commit that changed only code), it only records the
    commit. The parent is the project's latest version before it.
    """
    snapshot_id = _snapshots(session, project, {input_hash})[input_hash]
    key = {
        "project_id": project.id,
        "input_snapshot_id": snapshot_id,
        "generator_version": generator_version,
    }
    found = session.scalar(select(models.GoldenSetVersion).filter_by(**key))
    created = found is None
    if found is None:
        keys = set(identity_keys)
        current = states(session, project)
        unknown = sorted(keys - current.keys())
        if unknown:
            raise ValueError(f"items not stored for {project.slug}: {', '.join(unknown)}")
        parent = session.scalar(
            select(models.GoldenSetVersion.id)
            .where(models.GoldenSetVersion.project_id == project.id)
            .order_by(models.GoldenSetVersion.id.desc())
            .limit(1)
        )
        new_id = session.scalar(
            insert(models.GoldenSetVersion)
            .values(**key, parent_id=parent)
            .on_conflict_do_nothing()
            .returning(models.GoldenSetVersion.id)
        )
        if new_id is None:  # another transaction created it meanwhile
            created = False
        else:
            approved = sorted(k for k in keys if current[k] == "approved")
            ids = _item_ids(session, project, approved)
            session.add_all(
                models.GoldenSetItem(version_id=new_id, test_item_id=ids[k]) for k in approved
            )
        session.flush()
        found = session.scalars(select(models.GoldenSetVersion).filter_by(**key)).one()
    if commit_sha is not None:
        session.execute(
            insert(models.GoldenSetCommit)
            .values(version_id=found.id, commit_sha=commit_sha)
            .on_conflict_do_nothing()
        )
        session.flush()
    return found, created


def version_items(session: Session, version: models.GoldenSetVersion) -> list[TestItem]:
    """The items of a golden-set version, as `tasks.TestItem`, ordered by identity key."""
    project = session.get_one(models.Project, version.project_id)
    found = session.execute(
        select(models.TestItem, models.InputSnapshot.input_hash)
        .join(models.GoldenSetItem, models.GoldenSetItem.test_item_id == models.TestItem.id)
        .join(models.InputSnapshot, models.InputSnapshot.id == models.TestItem.input_snapshot_id)
        .where(models.GoldenSetItem.version_id == version.id)
        .order_by(models.TestItem.identity_key)
    )
    return [
        rows.item_from_row(row, project=project.slug, input_hash=input_hash)
        for row, input_hash in found
    ]


def _values(row: models.TestItem) -> dict[str, object]:
    """The row's columns for a Core insert; unset ones are left to their server default."""
    values = {c.key: getattr(row, c.key) for c in models.TestItem.__table__.columns}
    return {k: v for k, v in values.items() if v is not None or k not in _DEFAULTED}


_DEFAULTED = {c.key for c in models.TestItem.__table__.columns if c.server_default is not None}
_DEFAULTED |= {"id"}


def _snapshots(session: Session, project: models.Project, hashes: set[str]) -> Mapping[str, int]:
    result = session.execute(
        select(models.InputSnapshot.input_hash, models.InputSnapshot.id).where(
            models.InputSnapshot.project_id == project.id,
            models.InputSnapshot.input_hash.in_(hashes),
        )
    )
    found = {input_hash: row_id for input_hash, row_id in result}
    missing = sorted(hashes - found.keys())
    if missing:
        raise ValueError(f"input snapshots not stored for {project.slug}: {', '.join(missing)}")
    return found


def _item_ids(session: Session, project: models.Project, keys: Iterable[str]) -> dict[str, int]:
    found = session.execute(
        select(models.TestItem.identity_key, models.TestItem.id).where(
            models.TestItem.project_id == project.id,
            models.TestItem.identity_key.in_(list(keys)),
        )
    )
    return {key: row_id for key, row_id in found}


def _item_id(session: Session, project: models.Project, identity_key: str) -> int:
    found = _item_ids(session, project, [identity_key]).get(identity_key)
    if found is None:
        raise LookupError(f"no test item {identity_key} in {project.slug}")
    return found
