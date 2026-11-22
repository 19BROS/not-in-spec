"""Migrations against a real Postgres (TEST_DATABASE_URL): schema, append-only guard, downgrade."""

import pytest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import Engine, inspect, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from notinspec.db import migrate, models


def test_upgrade_creates_every_table_of_the_models(engine: Engine) -> None:
    tables = set(inspect(engine).get_table_names())
    assert set(models.Base.metadata.tables) <= tables
    assert "alembic_version" in tables


def test_migrations_match_the_models(engine: Engine) -> None:
    """A change in models.py needs a migration (`notinspec db revision`)."""
    with engine.connect() as conn:
        context = MigrationContext.configure(conn, opts={"compare_type": True})
        diff = compare_metadata(context, models.Base.metadata)
    assert diff == []


def test_every_append_only_table_has_the_trigger(engine: Engine) -> None:
    with engine.connect() as conn:
        found = conn.execute(
            text(
                "SELECT c.relname FROM pg_trigger t JOIN pg_class c ON c.oid = t.tgrelid "
                "WHERE t.tgname = 'append_only' AND c.relnamespace = "
                "(SELECT oid FROM pg_namespace WHERE nspname = current_schema())"
            )
        ).scalars()
        assert set(found) == set(models.APPEND_ONLY)


def _review(engine: Engine) -> int:
    with Session(engine) as session, session.begin():
        project = models.Project(slug="lib", name="lib")
        session.add(project)
        session.flush()
        snapshot = models.InputSnapshot(project_id=project.id, input_hash="ih")
        session.add(snapshot)
        session.flush()
        item = models.TestItem(
            project_id=project.id,
            identity_key="key",
            level="L1",
            operator_version=1,
            format="python",
            difficulty="explicit-single-step",
            chunk_key="k1",
            reference={"kind": "default"},
            wording={"text": "What is the default?"},
            generator_version=1,
            input_snapshot_id=snapshot.id,
        )
        session.add(item)
        session.flush()
        decision = models.ReviewDecision(test_item_id=item.id, decision="approved", reviewer="auto")
        session.add(decision)
        session.flush()
        return decision.id


@pytest.mark.parametrize(
    "statement",
    [
        "UPDATE review_decision SET decision = 'rejected'",
        "DELETE FROM review_decision",
        "TRUNCATE review_decision CASCADE",
        "UPDATE test_item SET wording = '{}'",
        "DELETE FROM test_item",
    ],
)
def test_append_only_rows_cannot_change(engine: Engine, statement: str) -> None:
    _review(engine)
    with pytest.raises(DBAPIError, match="append-only"), engine.begin() as conn:
        conn.execute(text(statement))
    with engine.connect() as conn:  # still there, unchanged
        assert conn.execute(text("SELECT decision FROM review_decision")).scalar() == "approved"


def test_a_new_decision_is_a_new_row(engine: Engine) -> None:
    _review(engine)
    with engine.begin() as conn:
        item = conn.execute(text("SELECT id FROM test_item")).scalar()
        conn.execute(
            text(
                "INSERT INTO review_decision (test_item_id, decision, reviewer) "
                "VALUES (:item, 'rejected', 'pr-closed')"
            ),
            {"item": item},
        )
        latest = conn.execute(
            text("SELECT decision FROM review_decision ORDER BY id DESC LIMIT 1")
        ).scalar()
    assert latest == "rejected"


def test_checks_reject_unknown_values(engine: Engine) -> None:
    with pytest.raises(DBAPIError, match="ck_project|ck_run_trigger"), engine.begin() as conn:
        conn.execute(text("INSERT INTO project (slug, name) VALUES ('p', 'p')"))
        conn.execute(
            text(
                "INSERT INTO run (public_id, project_id, trigger, status, tool_version) "
                "SELECT 'r', id, 'webhook', 'done', '0' FROM project"
            )
        )


def test_downgrade_removes_everything(bare: Engine) -> None:
    with bare.begin() as conn:
        config = migrate.alembic_config(connection=conn)
        migrate.upgrade(config)
        migrate.downgrade(config, "base")
    assert set(inspect(bare).get_table_names()) <= {"alembic_version"}
