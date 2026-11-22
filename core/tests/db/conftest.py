"""Database tests run against TEST_DATABASE_URL and are skipped without it (no CI step yet).

Each test gets a fresh schema with every migration applied, dropped afterwards, so the tests
never touch tables outside it. Use an empty database you don't need, e.g.
`TEST_DATABASE_URL=postgresql://postgres:<password>@localhost:5432/notinspec_test`.
"""

import os
import secrets
from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine, text

from notinspec.db import migrate, sqlalchemy_url


@pytest.fixture(scope="session")
def db_url() -> str:
    url = os.environ.get("TEST_DATABASE_URL", "").strip()
    if not url:
        pytest.skip("set TEST_DATABASE_URL to run the database tests")
    return url


@pytest.fixture
def schema(db_url: str) -> Iterator[str]:
    """An empty schema of its own; dropped with everything in it after the test."""
    name = f"test_{secrets.token_hex(6)}"
    admin = create_engine(sqlalchemy_url(db_url))
    with admin.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA {name}"))
    try:
        yield name
    finally:
        with admin.begin() as conn:
            conn.execute(text(f"DROP SCHEMA {name} CASCADE"))
        admin.dispose()


def schema_engine(db_url: str, schema: str) -> Engine:
    return create_engine(
        sqlalchemy_url(db_url), connect_args={"options": f"-csearch_path={schema}"}
    )


@pytest.fixture
def bare(db_url: str, schema: str) -> Iterator[Engine]:
    """An engine on the empty schema, before any migration."""
    engine = schema_engine(db_url, schema)
    yield engine
    engine.dispose()


@pytest.fixture
def engine(bare: Engine) -> Engine:
    """An engine on a schema with every migration applied."""
    with bare.begin() as conn:
        migrate.upgrade(migrate.alembic_config(connection=conn))
    return bare
