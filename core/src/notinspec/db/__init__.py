"""Postgres storage (SPEC §10, §18): tables, migrations, mapping from the pipeline's dataclasses,
and the import of run folders written before the DB existed.

Needs the extra `notinspec[db]`; the CLI imports this package only for its `db` commands.
Pipeline code never imports it (SPEC §18).
"""

from notinspec.db.engine import DatabaseUrlError, database_url, make_engine, sqlalchemy_url

__all__ = ["DatabaseUrlError", "database_url", "make_engine", "sqlalchemy_url"]
