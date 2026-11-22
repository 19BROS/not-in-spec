"""Writing pipeline output into the database, inside the caller's session (one transaction).

The functions take the JSON shape of the pipeline's dataclasses (see `notinspec.db.rows`), so
the worker, the API and the import of old run folders share them.
"""

from collections.abc import Iterable, Mapping
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from notinspec.db import models, rows

type Doc = Mapping[str, Any]


def project(session: Session, slug: str, *, name: str | None = None) -> models.Project:
    """The project with this slug; created (without a repository) when it does not exist."""
    found = session.scalar(select(models.Project).where(models.Project.slug == slug))
    if found is not None:
        return found
    created = models.Project(slug=slug, name=name or slug)
    session.add(created)
    session.flush()
    return created


def ingestion(session: Session, proj: models.Project, doc: Doc) -> models.Ingestion:
    """ingestion.json → snapshot, files, chunks, inventory. Stored once per inputs + versions.

    The same inputs, config and versions always give the same chunks and inventory, so a second
    run on them reuses the rows.
    """
    snapshot = session.scalar(
        select(models.InputSnapshot).where(
            models.InputSnapshot.project_id == proj.id,
            models.InputSnapshot.input_hash == doc["input_hash"],
        )
    )
    if snapshot is None:
        snapshot = models.InputSnapshot(project_id=proj.id, input_hash=doc["input_hash"])
        session.add(snapshot)
        session.flush()
        session.add_all(rows.source_file(f, snapshot.id) for f in doc["files"])

    versions = rows.ingestion_versions(doc)
    key = rows.versions_hash(versions)
    found = session.scalar(
        select(models.Ingestion).where(
            models.Ingestion.snapshot_id == snapshot.id,
            models.Ingestion.config_hash == doc["config_hash"],
            models.Ingestion.versions_hash == key,
        )
    )
    if found is not None:
        return found
    ing = models.Ingestion(
        snapshot_id=snapshot.id,
        config_hash=doc["config_hash"],
        versions=versions,
        versions_hash=key,
        warnings=list(doc.get("warnings", [])),
        conflicts=list(doc.get("conflicts", [])),
    )
    session.add(ing)
    session.flush()
    session.add_all(rows.chunk(c, ing.id) for c in doc["chunks"])
    _inventory(session, ing.id, doc["inventory"])
    session.flush()
    return ing


def _inventory(session: Session, ingestion_id: int, inventory: Doc) -> None:
    symbols = [(s, rows.symbol(s, ingestion_id)) for s in inventory["symbols"]]
    session.add_all(row for _, row in symbols)
    session.flush()
    signatures = [
        (sig, rows.signature(sig, row.id, i))
        for s, row in symbols
        for i, sig in enumerate(s.get("signatures", []))
    ]
    session.add_all(row for _, row in signatures)
    session.flush()
    session.add_all(
        rows.parameter(p, row.id, i)
        for sig, row in signatures
        for i, p in enumerate(sig.get("parameters", []))
    )
    session.add_all(rows.change(c, ingestion_id, i) for i, c in enumerate(inventory["changes"]))


def chunk_ids(session: Session, ingestion_id: int) -> dict[str, int]:
    """`Chunk.id` (the pipeline's key) → row id, for the rows that point at chunks."""
    found = session.execute(
        select(models.Chunk.chunk_key, models.Chunk.id).where(
            models.Chunk.ingestion_id == ingestion_id
        )
    )
    return {key: row_id for key, row_id in found.tuples()}


def claims(session: Session, run: models.Run, doc: Doc) -> int:
    """claims.json (grounded claims, dropped ones included) → claim and extraction_issue rows.

    Returns the number of claims stored.
    """
    if run.ingestion_id is None:
        raise ValueError(f"run {run.public_id} has no ingestion: claims need its chunks")
    ids = chunk_ids(session, run.ingestion_id)
    unknown = sorted({g["claim"]["chunk_id"] for g in doc["claims"]} - ids.keys())
    if unknown:
        raise ValueError(f"claims of chunks not in the run's ingestion: {', '.join(unknown)}")
    versions = doc["versions"]
    session.add_all(
        rows.claim(g, run.id, ids[g["claim"]["chunk_id"]], versions) for g in doc["claims"]
    )
    session.add_all(rows.extraction_failure(f, run.id) for f in doc.get("failures", []))
    session.add_all(rows.extraction_problem(p, run.id) for p in doc.get("problems", []))
    session.flush()
    return len(doc["claims"])


def llm_calls(session: Session, run: models.Run | None, calls: Iterable[Doc]) -> int:
    count = 0
    for call in calls:
        session.add(rows.llm_call(call, run.id if run is not None else None))
        count += 1
    session.flush()
    return count


def claim_answers(session: Session, entries: Iterable[tuple[Doc, Doc]]) -> int:
    """Claim store entries; an entry already stored (same key, same answer) is skipped.

    Run folders often carry a copy of the same store (`notinspec demo --claims-store`).
    """
    count = 0
    for key, answer in entries:
        row = rows.claim_answer(key, answer)
        if _stored(session, row):
            continue
        session.add(row)
        session.flush()
        count += 1
    return count


def _stored(session: Session, row: models.ClaimAnswer) -> bool:
    a = models.ClaimAnswer
    found = session.scalar(
        select(a.id)
        .where(
            a.content_hash == row.content_hash,
            a.breadcrumb == row.breadcrumb,
            a.extractor == row.extractor,
            a.model == row.model,
            a.prompt_version == row.prompt_version,
            a.reasoning_effort.is_not_distinct_from(row.reasoning_effort),
            a.parser_version.is_not_distinct_from(row.parser_version),
            a.thinking.is_not_distinct_from(row.thinking),
            a.prompt_hash == row.prompt_hash,
            a.run_ref == row.run_ref,
        )
        .limit(1)
    )
    return found is not None
