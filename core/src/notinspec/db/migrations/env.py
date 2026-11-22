"""Alembic environment: `notinspec.db.migrate` sets the URL or hands in a connection."""

from alembic import context
from sqlalchemy import Connection, create_engine

from notinspec.db.models import Base

config = context.config


def _run(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=Base.metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


def _main() -> None:
    url = config.get_main_option("sqlalchemy.url")
    if context.is_offline_mode():  # `alembic upgrade --sql`: print the SQL for review
        context.configure(url=url, target_metadata=Base.metadata, literal_binds=True)
        with context.begin_transaction():
            context.run_migrations()
        return
    connection: Connection | None = config.attributes.get("connection")
    if connection is not None:
        _run(connection)
        return
    if url is None:
        raise RuntimeError("no database URL: use notinspec.db.migrate.alembic_config(url)")
    engine = create_engine(url)
    try:
        with engine.begin() as conn:
            _run(conn)
    finally:
        engine.dispose()


_main()
