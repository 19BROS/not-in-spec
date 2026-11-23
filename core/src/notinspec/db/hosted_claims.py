"""The hosted worker's live claim pipeline, using the same core entry points as the CLI."""

import shutil
from pathlib import Path
from typing import Any

from sqlalchemy import Engine

from notinspec.adapters.canonical import canonical_json
from notinspec.claims import DEFAULT_EXTRACTORS, run_claims
from notinspec.claims.store import JsonlCallLog, LlmCall
from notinspec.db.stores import DbCallLog, DbClaimStore
from notinspec.ingestion import Ingestion
from notinspec.nli import NliModel
from notinspec.report import claim_counts, render_claims
from notinspec.runner import ModelClient


class HostedCallLog:
    def __init__(self, engine: Engine, path: Path) -> None:
        self.database = DbCallLog(engine)
        self.file = JsonlCallLog(path)

    def append(self, call: LlmCall) -> None:
        # The durable append-only journal survives a failed database write or run.
        self.file.append(call)
        self.database.append(call)


class HostedClaims:
    def __init__(self, engine: Engine, client: ModelClient, nli: NliModel, log_dir: Path) -> None:
        self.engine, self.client, self.nli = engine, client, nli
        self.log_dir = log_dir

    def __call__(
        self, ingestion: Ingestion, out: Path, run_id: str, allowed_models: tuple[str, ...]
    ) -> dict[str, Any]:
        specs = tuple(
            s for s in DEFAULT_EXTRACTORS if not allowed_models or s.model in allowed_models
        )
        if not specs:
            raise RuntimeError("project allows none of the configured free FIIT extractors")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        journal = self.log_dir / f"{run_id}.jsonl"
        result = run_claims(
            ingestion.chunks,
            specs,
            self.client,
            self.nli,
            run_id,
            HostedCallLog(self.engine, journal),
            sections=ingestion.chunks,
            inventory=ingestion.inventory,
            project=ingestion.project,
            store=DbClaimStore(self.engine),
        )
        doc = {
            "schema_version": 1,
            "project": ingestion.project,
            "input_hash": ingestion.input_hash,
            "sources": [],
            "chunks": len(ingestion.chunks),
            "extractors": [r.extractor for r in result.results],
            "versions": result.versions,
            "counts": claim_counts(result),
            "claims": result.claims,
            "failures": [f for r in result.results for f in r.failures],
            "problems": [p for r in result.results for p in r.problems],
        }
        (out / "claims.json").write_bytes(canonical_json(doc, pretty=True))
        (out / "claims.html").write_text(
            render_claims(ingestion, ingestion.chunks, result), encoding="utf-8"
        )
        if journal.is_file():
            shutil.copyfile(journal, out / "llm-calls.jsonl")
        if any(r.failures for r in result.results):
            raise RuntimeError(
                "claim extraction was incomplete; raw calls and completed answers kept"
            )
        import json

        return dict(json.loads(canonical_json(doc)))
