"""Where the database is: `DATABASE_URL` (deploy/docker-compose.yml); tests: `TEST_DATABASE_URL`."""

import os

from sqlalchemy import Engine, create_engine


class DatabaseUrlError(ValueError):
    """No database URL configured, or one that is not Postgres."""


def sqlalchemy_url(url: str) -> str:
    """`postgresql://…` (as Compose and libpq write it) → SQLAlchemy with the psycopg 3 driver."""
    for prefix in ("postgresql+psycopg://", "postgresql://", "postgres://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url.removeprefix(prefix)
    raise DatabaseUrlError("the database URL must start with postgresql://")


def database_url(variable: str = "DATABASE_URL") -> str:
    url = os.environ.get(variable, "").strip()
    if not url:
        raise DatabaseUrlError(f"set {variable} (postgresql://user:password@host:5432/name)")
    return url


def make_engine(url: str) -> Engine:
    return create_engine(sqlalchemy_url(url), pool_pre_ping=True)
