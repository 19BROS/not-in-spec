"""Test items, review decisions and golden-set versions, against a real Postgres."""

from dataclasses import replace

import pytest
from sqlalchemy import Engine, func, select, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from notinspec import tasks
from notinspec.adapters.canonical import content_hash
from notinspec.chunking import Document, chunk_document
from notinspec.db import golden, models, rows, save
from notinspec.inventory import Inventory, Parameter, Signature, Source, Symbol
from notinspec.tasks import (
    ExistsReference,
    GenerationContext,
    Subject,
    TaskText,
    generate_l0,
    generate_l1,
)

CHUNKS = chunk_document(Document("api.md", "# API\nDocumentation."), project="pkg")
SIGNATURE = (Source("signature", CHUNKS[0].section_id),)
CHANGELOG = (Source("changelog", CHUNKS[0].section_id),)
SNAPSHOT = content_hash("snapshot")
CONTEXT = GenerationContext("pkg", "2.0", SNAPSHOT)
INVENTORY = Inventory(
    (
        Symbol(
            "pkg.connect",
            "function",
            SIGNATURE,
            (Signature((Parameter("host", "positional_or_keyword", True, SIGNATURE),), SIGNATURE),),
        ),
    ),
    (),
)


def generate(context: GenerationContext = CONTEXT, **kwargs: object) -> list[tasks.TestItem]:
    l0 = generate_l0(INVENTORY, context=context, chunks=CHUNKS, **kwargs)  # type: ignore[arg-type]
    l1 = generate_l1(INVENTORY, context=context, chunks=CHUNKS, **kwargs)  # type: ignore[arg-type]
    found = [*l0.items, *l1.items]
    # Today's generators skip what lacks spec or signature evidence; items from claims and
    # changelogs will not, so one such item stands in for them.
    pending = replace(
        found[0],
        level="L0",
        question_kind="exists",
        reference=ExistsReference(Subject("pkg.old1"), False),
        sources=CHANGELOG,
    )
    return [*found, pending]


def setup(session: Session, *hashes: str) -> models.Project:
    project = save.project(session, "pkg")
    for input_hash in hashes or (SNAPSHOT,):
        session.add(models.InputSnapshot(project_id=project.id, input_hash=input_hash))
    session.flush()
    return project


def test_items_round_trip_and_trusted_ones_are_approved(engine: Engine) -> None:
    items = generate()
    trusted = {i.id for i in items if any(s.type == "signature" for s in i.sources)}
    assert trusted and trusted != {i.id for i in items}  # both kinds in the fixture
    with Session(engine) as session, session.begin():
        project = setup(session)
        stored = golden.store_items(session, project, items)
        assert [s.new for s in stored] == [True] * len(items)
        assert sorted(golden.existing_items(session, project), key=lambda i: i.id) == sorted(
            items, key=lambda i: i.id
        )
        state = golden.states(session, project)
        assert {k for k, v in state.items() if v == "approved"} == trusted
        assert {v for k, v in state.items() if k not in trusted} == {"candidate"}
        decision = session.scalars(select(models.ReviewDecision)).first()
        assert decision is not None and decision.reviewer == golden.AUTO


def test_an_item_with_the_same_identity_is_reused_with_its_text_and_decisions(
    engine: Engine,
) -> None:
    items = generate()
    candidate = next(i for i in items if not any(s.type == "signature" for s in i.sources))
    with Session(engine) as session, session.begin():
        project = setup(session, SNAPSHOT, content_hash("typo fix"))
        golden.store_items(session, project, items)
        golden.review(session, project, candidate.id, "rejected", "jana", "wrong reference")
        # The same reference from new inputs and another wording: the same identity key.
        again = replace(
            candidate,
            input_snapshot_hash=content_hash("typo fix"),
            wording=TaskText("Another text?", ("Other?", "Third?")),
        )
        assert again.id == candidate.id
        (stored,) = golden.store_items(session, project, [again])
        assert not stored.new
        assert golden.states(session, project)[candidate.id] == "rejected"
        (kept,) = (i for i in golden.existing_items(session, project) if i.id == candidate.id)
        assert kept.wording == candidate.wording  # the frozen task text, not the new one
        count = session.scalar(select(func.count()).select_from(models.TestItem))
        assert count == len(items)


def test_the_latest_decision_counts_and_none_is_changed(engine: Engine) -> None:
    (item, *_) = generate()
    with Session(engine) as session, session.begin():
        project = setup(session)
        golden.store_items(session, project, [item])
        golden.review(session, project, item.id, "rejected", "jana")
        golden.review(session, project, item.id, "approved", "figaro112", "checked again")
        assert golden.states(session, project)[item.id] == "approved"
        with pytest.raises(LookupError, match="no test item"):
            golden.review(session, project, "nope", "approved", "jana")
        with pytest.raises(ValueError, match="reviewer"):
            golden.review(session, project, item.id, "approved", " ")
        with pytest.raises(ValueError, match="decision"):
            golden.review(session, project, item.id, "maybe", "jana")  # type: ignore[arg-type]
    with engine.connect() as conn, pytest.raises(DBAPIError, match="append-only"):
        conn.execute(text("UPDATE review_decision SET decision = 'rejected'"))


def test_items_need_their_project_and_a_stored_snapshot(engine: Engine) -> None:
    items = generate()
    other = generate(GenerationContext("other", "2.0", SNAPSHOT))
    with Session(engine) as session, session.begin():
        project = setup(session, content_hash("something else"))
        with pytest.raises(ValueError, match="input snapshots not stored"):
            golden.store_items(session, project, items)
        with pytest.raises(ValueError, match="belongs to other"):
            golden.store_items(session, project, other)


def test_golden_set_versions(engine: Engine) -> None:
    second = content_hash("second inputs")
    items = generate()
    approved = sorted(i.id for i in items if any(s.type == "signature" for s in i.sources))
    pending = next(i.id for i in items if i.id not in approved)
    keys = [i.id for i in items]
    with Session(engine) as session, session.begin():
        project = setup(session, SNAPSHOT, second)
        golden.store_items(session, project, items)

        first, created = golden.golden_set_version(
            session, project, input_hash=SNAPSHOT, generator_version=2, identity_keys=keys,
            commit_sha="a" * 40,
        )  # fmt: skip
        assert created and first.parent_id is None
        assert [i.id for i in golden.version_items(session, first)] == approved

        # A commit that changed only code: same inputs, same version, one more commit.
        golden.review(session, project, pending, "approved", "jana")
        same, created = golden.golden_set_version(
            session, project, input_hash=SNAPSHOT, generator_version=2, identity_keys=keys,
            commit_sha="b" * 40,
        )  # fmt: skip
        assert not created and same.id == first.id
        assert [i.id for i in golden.version_items(session, same)] == approved  # frozen
        commits = session.scalars(
            select(models.GoldenSetCommit.commit_sha).where(
                models.GoldenSetCommit.version_id == first.id
            )
        )
        assert sorted(commits) == ["a" * 40, "b" * 40]

        # New inputs: a child version, now with the item approved meanwhile.
        child, created = golden.golden_set_version(
            session, project, input_hash=second, generator_version=2, identity_keys=keys
        )
        assert created and child.parent_id == first.id
        assert [i.id for i in golden.version_items(session, child)] == sorted([*approved, pending])
        # Unchanged items are referenced, not copied.
        assert session.scalar(select(func.count()).select_from(models.TestItem)) == len(items)

        with pytest.raises(ValueError, match="items not stored"):
            golden.golden_set_version(
                session, project, input_hash=second, generator_version=3, identity_keys=["nope"]
            )


def test_item_rows_are_the_export_shape() -> None:
    """Without a database: the row mapper and its way back."""
    (*_, item) = generate()
    row = rows.test_item(rows.item_doc(item), project_id=1, input_snapshot_id=2, origin_run_id=3)
    assert (row.identity_key, row.chunk_key, row.symbol_path) == (
        item.id,
        item.chunk_id,
        item.reference.subject.symbol,
    )
    assert row.reference["kind"] == item.question_kind
    assert rows.item_from_row(row, project="pkg", input_hash=SNAPSHOT) == item
    row.reference = {**row.reference, "exists": True}  # edited by hand: its key no longer fits
    with pytest.raises(ValueError, match="identity"):
        rows.item_from_row(row, project="pkg", input_hash=SNAPSHOT)
