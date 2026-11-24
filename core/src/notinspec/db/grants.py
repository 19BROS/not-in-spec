"""Privileges of the role the API and the worker connect as (SPEC §10).

Computed from the models, so a table added by a later migration gets its grants without anyone
repeating a list. `notinspec db upgrade` calls it after every upgrade; it is idempotent. The
role itself is created by deploy (with its password from env); until it exists this does
nothing. Migration 0001 keeps its own frozen grants for databases where the role existed first.
"""

from sqlalchemy import Connection, text

from notinspec.db.models import APPEND_ONLY, Base

APP_ROLE = "notinspec_app"


def grant_app_role(conn: Connection, role: str = APP_ROLE) -> bool:
    """Read and insert everywhere, update and delete only mutable tables; False: no such role.

    Also revokes UPDATE, DELETE and TRUNCATE on append-only tables, in case anything granted
    them by hand. Works in the connection's current schema.
    """
    exists = conn.scalar(text("SELECT 1 FROM pg_roles WHERE rolname = :role"), {"role": role})
    if exists is None:
        return False
    quote = conn.dialect.identifier_preparer.quote
    schema = quote(str(conn.scalar(text("SELECT current_schema()"))))
    grantee = quote(role)
    every = sorted(Base.metadata.tables)
    append_only = [t for t in every if t in APPEND_ONLY]
    mutable = [t for t in every if t not in APPEND_ONLY]

    def tables(names: list[str]) -> str:
        return ", ".join(f"{schema}.{quote(name)}" for name in names)

    for statement in (
        f"GRANT USAGE ON SCHEMA {schema} TO {grantee}",
        f"GRANT SELECT, INSERT ON {tables(every)} TO {grantee}",
        f"GRANT UPDATE, DELETE ON {tables(mutable)} TO {grantee}",
        f"REVOKE UPDATE, DELETE, TRUNCATE ON {tables(append_only)} FROM {grantee}",
        f"GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA {schema} TO {grantee}",
    ):
        conn.execute(text(statement))
    return True
