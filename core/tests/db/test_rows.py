"""Mapping to rows, URLs and the CLI without a database: these run everywhere, CI included."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, get_args

import pytest

from notinspec.claims.model import ClaimType, RawClaim
from notinspec.claims.pipeline import STATUSES
from notinspec.claims.store import LlmCall, ReuseKey, StoredAnswer
from notinspec.cli import main
from notinspec.db import DatabaseUrlError, database_url, models, rows, sqlalchemy_url
from notinspec.db.save import Registration
from notinspec.findings import Check, Evidence, Finding
from notinspec.inventory.objects import (
    ChangeKind,
    Confidence,
    ParameterKind,
    ParameterLocation,
)

CALL = LlmCall(
    run_id="r1",
    role="claim-extractor",
    extractor="qwen",
    chunk_id="k1",
    model="qwen3.8-flash-next",
    prompt_hash="ph",
    request={"model": "qwen3.8-flash-next", "messages": []},
    response={
        "model": "qwen3.8-flash-next",
        "usage": {"prompt_tokens": 12, "completion_tokens": 3},
    },
    error=None,
    time="2026-11-21T10:00:00+00:00",
)


def test_postgres_urls_get_the_psycopg_driver() -> None:
    assert sqlalchemy_url("postgresql://u:p@h:5432/d") == "postgresql+psycopg://u:p@h:5432/d"
    assert sqlalchemy_url("postgres://u@h/d") == "postgresql+psycopg://u@h/d"
    assert sqlalchemy_url("postgresql+psycopg://h/d") == "postgresql+psycopg://h/d"
    with pytest.raises(DatabaseUrlError, match="postgresql://"):
        sqlalchemy_url("sqlite:///x.db")


def test_database_url_must_be_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(DatabaseUrlError, match="set DATABASE_URL"):
        database_url()
    monkeypatch.setenv("DATABASE_URL", " postgresql://h/d ")
    assert database_url() == "postgresql://h/d"


def test_cli_db_without_url_fails_with_a_message(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert main(["db", "upgrade"]) == 2
    assert "set DATABASE_URL" in capsys.readouterr().err
    assert main(["db"]) == 0  # help only


def test_llm_call_keeps_the_raw_response_and_reads_usage() -> None:
    row = rows.llm_call(rows.plain(CALL), run_id=7)
    assert (row.run_id, row.run_ref, row.role, row.actor, row.chunk_key) == (
        7,
        "r1",
        "claim-extractor",
        "qwen",
        "k1",
    )
    assert row.response == CALL.response
    assert (row.answered_model, row.tokens_in, row.tokens_out) == ("qwen3.8-flash-next", 12, 3)
    assert row.created_at == datetime(2026, 11, 21, 10, tzinfo=UTC)


def test_llm_call_without_an_answer() -> None:
    call = rows.plain(CALL) | {"response": None, "error": "timed-out"}
    row = rows.llm_call(call, run_id=None)
    assert (row.response, row.answered_model, row.tokens_in, row.error) == (
        None,
        None,
        None,
        "timed-out",
    )


def test_claim_answer_from_the_store_types() -> None:
    key = ReuseKey("h", "lib > A", "qwen", "m", 1, None, 2, False)
    answer = StoredAnswer((RawClaim("c1", "t", "c", "fact"),), ("p",), "r1", "ph", "m-exact")
    row = rows.claim_answer(rows.plain(key), rows.plain(answer))
    assert (row.parser_version, row.thinking, row.reasoning_effort) == (2, False, None)
    assert row.claims == [{"local_id": "c1", "text": "t", "citation": "c", "type": "fact"}]
    assert (row.run_ref, row.answered_model, row.problems) == ("r1", "m-exact", ["p"])


def test_claim_spans_become_start_and_end() -> None:
    grounded = {
        "claim": {"extractor": "e", "local_id": "c1", "text": "t", "citation": "c",
                  "type": "fact", "prompt_hash": "ph", "model": "m", "run_id": "r0",
                  "chunk_id": "k1"},
        "prompt_version": 1, "status": "kept", "citation_span": [3, 9], "citation_matches": 1,
        "premise_candidates": 1, "premise": "p", "premise_span": None, "nli": None,
        "missing": [],
    }  # fmt: skip
    row = rows.claim(grounded, run_id=1, chunk_id=2, versions={"grounding": 1})
    assert (row.citation_start, row.citation_end) == (3, 9)
    assert (row.premise_start, row.premise_end) == (None, None)
    assert (row.extraction_run, row.versions) == ("r0", {"grounding": 1})


def test_ingestion_versions_hash_changes_with_the_chunker() -> None:
    doc = {"schema_version": 4, "chunker_version": 3, "soft_limit": 2000,
           "sphinx": {"version": "9.1.0", "reader_version": 2},
           "inventory_builder_version": 1}  # fmt: skip
    versions = rows.ingestion_versions(doc)
    assert versions["sphinx_reader_version"] == 2
    assert rows.ingestion_versions(doc | {"sphinx": None})["sphinx_version"] is None
    newer = rows.ingestion_versions(doc | {"chunker_version": 4})
    assert rows.versions_hash(versions) != rows.versions_hash(newer)


def test_no_mutable_state_on_append_only_tables() -> None:
    """SPEC §10: review state and finding status are derived, never stored as a column."""
    columns = {t: set(models.Base.metadata.tables[t].columns.keys()) for t in models.APPEND_ONLY}
    assert not {"status", "review_status", "is_frozen"} & columns["test_item"]
    assert "status" not in models.Base.metadata.tables["finding"].columns
    every = {c for t in models.Base.metadata.tables.values() for c in t.columns.keys()}
    assert not {"recommended_fix", "overall_score", "slack_webhook"} & every


def _registration(**changes: Any) -> Registration:
    fields: dict[str, Any] = {
        "slug": "urllib3",
        "repository": "urllib3/urllib3",
        "repository_id": 2558107,
        "default_branch": "main",
        "workflow": "notinspec.yml",
    }
    return Registration(**(fields | changes))


def test_registration_gives_the_oidc_workflow_path() -> None:
    reg = _registration()
    assert reg.workflow_path == "urllib3/urllib3/.github/workflows/notinspec.yml"


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"repository": "urllib3"}, "owner/name"),
        ({"repository": "a/../b"}, "owner/name"),
        ({"repository_id": 0}, "numeric ID"),
        ({"default_branch": "refs/heads/main"}, "branch name"),
        ({"workflow": ".github/workflows/x.yml"}, "file name"),
        ({"slug": "a b"}, "project must match"),
        ({"budget_per_run_usd": Decimal("-1")}, "negative"),
        ({"max_upload_bytes": 0}, "positive"),
    ],
)
def test_registration_rejects_bad_values(changes: dict[str, Any], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        _registration(**changes)


def test_finding_from_the_findings_dataclass() -> None:
    evidence = (
        Evidence("claim", "a", "x is 1", "s1", quote="x is 1"),
        Evidence("claim", "b", "x is 2", "s2", quote="x is 2"),
    )
    found = Finding("K5a", "contradiction", "lib > X", "m", "high", evidence,
                    versions=(("k5a", "1"), ("nli_model", "m")))  # fmt: skip
    row = rows.finding(rows.plain(found), run_id=3)
    assert (row.key, row.check_code, row.confidence) == (found.key, "K5a", "high")
    assert row.versions == {"k5a": "1", "nli_model": "m"}
    assert [e["ref"] for e in row.evidence] == ["a", "b"]


@pytest.mark.parametrize(
    ("values", "pipeline"),
    [
        (models.GROUNDING_STATUSES, set(STATUSES)),
        (models.CHECKS, set(get_args(Check.__value__))),
        (models.CONFIDENCES, set(get_args(Confidence.__value__))),
        (models.CLAIM_TYPES, set(get_args(ClaimType.__value__))),
        (models.CHANGE_KINDS, set(get_args(ChangeKind.__value__))),
        (models.PARAMETER_KINDS, set(get_args(ParameterKind.__value__))),
        (models.PARAMETER_LOCATIONS, set(get_args(ParameterLocation.__value__))),
    ],
)
def test_check_values_match_the_pipeline(values: tuple[str, ...], pipeline: set[str]) -> None:
    """A new value in the pipeline needs a migration of the CHECK, or the DB refuses it."""
    assert set(values) == pipeline
