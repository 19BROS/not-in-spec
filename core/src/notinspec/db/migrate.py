"""Alembic, configured in code: no alembic.ini, the migrations ship inside the package.

`notinspec db upgrade` runs them on `DATABASE_URL`. A new migration (after changing
`models.py`): `notinspec db revision -m "what changed"` against a database at head, then read
and fix what autogenerate wrote before committing it.
"""

from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import Connection

from notinspec.db.engine import sqlalchemy_url

MIGRATIONS = Path(__file__).parent / "migrations"


def alembic_config(url: str | None = None, connection: Connection | None = None) -> Config:
    """`connection` wins over `url`: tests run migrations in their own schema on it."""
    config = Config()
    config.set_main_option("script_location", str(MIGRATIONS))
    if url is not None:
        # `%` would start an interpolation in Alembic's ConfigParser (passwords can contain it)
        config.set_main_option("sqlalchemy.url", sqlalchemy_url(url).replace("%", "%%"))
    if connection is not None:
        config.attributes["connection"] = connection
    return config


def upgrade(config: Config, revision: str = "head") -> None:
    command.upgrade(config, revision)


def downgrade(config: Config, revision: str) -> None:
    command.downgrade(config, revision)


def revision(config: Config, message: str) -> None:
    command.revision(config, message=message, autogenerate=True)


def current(config: Config) -> None:
    command.current(config, verbose=True)
