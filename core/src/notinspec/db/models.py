"""Postgres tables (SPEC §10). Pipeline code never imports this: it works on dataclasses, and
`notinspec.db.rows` maps them to these tables.

Conventions:
- surrogate `bigint` keys; the pipeline's own stable IDs (`Chunk.id`, `Example.id`,
  `Finding.key`, the test item's identity key) are unique columns next to them;
- closed value sets are `text` with a CHECK, not Postgres enums, so a new value is a small
  migration;
- nested dataclasses the UI never filters on (sources, constraints, NLI scores) are `jsonb` in
  the shape `dataclasses.asdict` gives them;
- no state that changes on an append-only record: an item's review state is its latest
  `review_decision`, a finding is open while its key is in the latest main run, a candidate is
  stale when no main run picked it up and no `pr_closed` came (all derived, SPEC §10);
- no fix recommendations (SPEC §6.11), no averaged level and no overall score (AGENTS.md);
- no secrets: keys and webhooks stay in env (AGENTS.md).
"""

from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Integer,
    LargeBinary,
    MetaData,
    Numeric,
    PrimaryKeyConstraint,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# SPEC §10: never UPDATE or DELETE. A trigger refuses both (and TRUNCATE) for every role, and
# the application role gets only SELECT and INSERT on them (migration 0001).
APPEND_ONLY = (
    "upload",
    "pr_closed",
    "llm_call",
    "claim_answer",
    "test_item",
    "golden_set_version",
    "golden_set_commit",
    "golden_set_item",
    "review_decision",
    "run_test_item",
    "result",
)

# closed value sets, shared with the CHECKs below and the tests
TRIGGERS = ("cli", "pull_request", "push", "workflow_dispatch", "nightly")
UPLOAD_EVENTS = ("pull_request", "push", "workflow_dispatch")  # SPEC §11: everything else 403
RUN_STATUSES = ("queued", "running", "done", "error")  # SPEC §11.1
STEP_STATUSES = ("pending", "running", "done", "failed", "skipped", "not_implemented")
LOG_LEVELS = ("debug", "info", "warning", "error")
PARAMETER_KINDS = (
    "positional_only",
    "positional_or_keyword",
    "var_positional",
    "keyword_only",
    "var_keyword",
)
PARAMETER_LOCATIONS = ("path", "query", "header", "cookie", "body")
CHANGE_KINDS = ("added", "deprecated", "removed")
CLAIM_TYPES = ("fact", "change")
GROUNDING_STATUSES = (
    "kept",
    "citation_not_found",
    "not_checkable",
    "nli_neutral",
    "nli_contradiction",
    "id_missing",
)
EXTRACTION_ISSUES = ("failure", "problem")
LLM_ROLES = ("model-under-test", "claim-extractor", "task-writer", "round-trip-solver", "judge")
LEVELS = ("L0", "L1", "L2", "L3", "L4")
OPERATORS = ("copy", "adaptation", "variation", "composition", "migration", "perturbation")
DECISIONS = ("approved", "rejected")
ITEM_ROLES = ("stable", "superseded", "candidate")  # SPEC §7, per run
MODES = ("none", "retrieved", "gold")  # SPEC §6.9
ERROR_CATEGORIES = (  # SPEC §6.10, L3, and `invented` for "not in the documentation" (L2)
    "success",
    "wrong-symbol",
    "wrong-arguments",
    "hallucinated-api",
    "deprecated-api",
    "api-bypass",
    "invalid-format",
    "invented",
)
CHECKS = ("K1", "K2", "K3", "K4", "K5a", "K5b", "K6", "K7")
CONFIDENCES = ("high", "medium", "low")


def one_of(column: str, values: tuple[str, ...], *, nullable: bool = False) -> CheckConstraint:
    listed = ", ".join(f"'{v}'" for v in values)
    condition = f"{column} IN ({listed})"
    if nullable:
        condition = f"{column} IS NULL OR {condition}"
    return CheckConstraint(condition, name=column)


def _id() -> Mapped[int]:
    return mapped_column(BigInteger, Identity(), primary_key=True)


def _fk(target: str, *, nullable: bool = False, index: bool = True) -> Mapped[Any]:
    return mapped_column(BigInteger, ForeignKey(target), nullable=nullable, index=index)


def _created() -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), server_default=func.now())


def _json(default: str = "'[]'::jsonb") -> Mapped[Any]:
    return mapped_column(JSONB, server_default=text(default))


def _texts() -> Mapped[list[str]]:
    return mapped_column(ARRAY(Text), server_default=text("'{}'::text[]"))


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING)


# --- projects and inputs --------------------------------------------------------------------


class Project(Base):
    """A registered project (SPEC §11): our team registers it with the CLI on the VM.

    Demo runs started with the CLI create one without a repository.
    """

    __tablename__ = "project"

    id: Mapped[int] = _id()
    slug: Mapped[str] = mapped_column(Text, unique=True)  # `project` of notinspec.yaml
    name: Mapped[str] = mapped_column(Text)
    repository: Mapped[str | None] = mapped_column(Text)  # "owner/name", for display only
    # GitHub's numeric ID: the OIDC check uses it, never the name, which can be taken again
    repository_id: Mapped[int | None] = mapped_column(BigInteger, unique=True)
    default_branch: Mapped[str | None] = mapped_column(Text)
    workflow_path: Mapped[str | None] = mapped_column(Text)  # "owner/repo/.github/workflows/x.yml"
    # limits (SPEC §18: still open); NULL = no limit
    allowed_models: Mapped[list[str]] = _texts()
    budget_per_run_usd: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    budget_per_month_usd: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    max_upload_bytes: Mapped[int | None] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = _created()


class InputSnapshot(Base):
    """The inputs of a run, identified by `Ingestion.input_hash` (the hash of every file's hash).

    The uploaded archive itself lives on a volume, addressed by its hash (SPEC §10).
    """

    __tablename__ = "input_snapshot"
    __table_args__ = (UniqueConstraint("project_id", "input_hash"),)

    id: Mapped[int] = _id()
    project_id: Mapped[int] = _fk("project.id")
    input_hash: Mapped[str] = mapped_column(Text)
    docs_version: Mapped[str | None] = mapped_column(Text)  # `docs.version`: a display label only
    archive_sha256: Mapped[str | None] = mapped_column(Text)
    archive_bytes: Mapped[int | None] = mapped_column(BigInteger)
    archive_path: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = _created()


class SourceFile(Base):
    """One input file (`ingestion.InputFile`)."""

    __tablename__ = "source_file"
    __table_args__ = (UniqueConstraint("snapshot_id", "path"),)

    id: Mapped[int] = _id()
    snapshot_id: Mapped[int] = _fk("input_snapshot.id")
    path: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(Text)  # "sphinx", "markdown", "openapi", "changelog"
    content_hash: Mapped[str] = mapped_column(Text)


class Ingestion(Base):
    """What one version of the readers, chunker and inventory builder made of a snapshot.

    The same inputs read by a newer chunker give other chunks, so chunks and the inventory hang
    here and not on the snapshot. The config is part of the key: its `project` is in every
    breadcrumb and chunk ID.
    """

    __tablename__ = "ingestion"
    __table_args__ = (UniqueConstraint("snapshot_id", "config_hash", "versions_hash"),)

    id: Mapped[int] = _id()
    snapshot_id: Mapped[int] = _fk("input_snapshot.id")
    config_hash: Mapped[str] = mapped_column(Text)
    # schema, chunker, soft limit, Sphinx reader, inventory builder: what the output depends on
    versions: Mapped[dict[str, Any]] = mapped_column(JSONB)
    versions_hash: Mapped[str] = mapped_column(Text)
    warnings: Mapped[list[Any]] = _json()
    conflicts: Mapped[list[Any]] = _json()
    created_at: Mapped[datetime] = _created()


# --- runs ------------------------------------------------------------------------------------


class Run(Base):
    """One run: an upload from the Action, a nightly run or a run started with the CLI."""

    __tablename__ = "run"
    __table_args__ = (
        one_of("trigger", TRIGGERS),
        one_of("status", RUN_STATUSES),
        one_of("verdict", ("pass", "fail"), nullable=True),
        one_of("error_kind", ("input", "internal"), nullable=True),
        Index("ix_run_project_id_created_at", "project_id", "created_at"),
    )

    id: Mapped[int] = _id()
    public_id: Mapped[str] = mapped_column(Text, unique=True)  # in URLs: "20261118T1355Z-…"
    project_id: Mapped[int] = _fk("project.id", index=False)
    ingestion_id: Mapped[int | None] = _fk("ingestion.id", nullable=True)  # NULL: input error
    golden_set_version_id: Mapped[int | None] = _fk("golden_set_version.id", nullable=True)
    baseline_run_id: Mapped[int | None] = _fk("run.id", nullable=True)  # SPEC §7
    trigger: Mapped[str] = mapped_column(Text)
    commit_sha: Mapped[str | None] = mapped_column(Text)  # the OIDC `sha` for uploads
    ref: Mapped[str | None] = mapped_column(Text)
    pr_number: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(Text)
    verdict: Mapped[str | None] = mapped_column(Text)
    error: Mapped[str | None] = mapped_column(Text)
    error_kind: Mapped[str | None] = mapped_column(Text)
    comment_md: Mapped[str | None] = mapped_column(Text)
    tool_version: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = _created()
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Upload(Base):
    """One accepted upload from the Action (SPEC §11, §11.1): what the OIDC token proved.

    Replay protection is one run per (GitHub run, attempt). The token itself is never stored,
    only its verified claims.
    """

    __tablename__ = "upload"
    __table_args__ = (
        UniqueConstraint("project_id", "github_run_id", "github_run_attempt"),
        one_of("event_name", UPLOAD_EVENTS),
    )

    id: Mapped[int] = _id()
    run_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("run.id"), unique=True)
    project_id: Mapped[int] = _fk("project.id", index=False)
    repository_id: Mapped[int] = mapped_column(BigInteger)
    github_run_id: Mapped[int] = mapped_column(BigInteger)
    github_run_attempt: Mapped[int] = mapped_column(Integer)
    event_name: Mapped[str] = mapped_column(Text)
    ref: Mapped[str] = mapped_column(Text)
    sha: Mapped[str] = mapped_column(Text)  # the run's commit (on a PR: the merge commit)
    workflow_ref: Mapped[str] = mapped_column(Text)
    pr_number: Mapped[int | None] = mapped_column(Integer)  # from ref = refs/pull/<N>/merge
    # sent by the client: display and baseline lookup only, never proof (SPEC §11)
    head_sha: Mapped[str | None] = mapped_column(Text)
    base_sha: Mapped[str | None] = mapped_column(Text)
    archive_sha256: Mapped[str] = mapped_column(Text)
    archive_bytes: Mapped[int] = mapped_column(BigInteger)
    claims: Mapped[dict[str, Any]] = mapped_column(JSONB)  # the verified OIDC claims
    received_at: Mapped[datetime] = _created()


class PrClosed(Base):
    """`POST /api/pr-closed`: a PR closed without merging; its candidates get rejected."""

    __tablename__ = "pr_closed"

    id: Mapped[int] = _id()
    project_id: Mapped[int] = _fk("project.id")
    pr_number: Mapped[int] = mapped_column(Integer)
    github_run_id: Mapped[int] = mapped_column(BigInteger)
    claims: Mapped[dict[str, Any]] = mapped_column(JSONB)
    received_at: Mapped[datetime] = _created()


class RunStep(Base):
    """A pipeline step of a run with its progress, as the Run progress screen shows it."""

    __tablename__ = "run_step"
    __table_args__ = (UniqueConstraint("run_id", "step"), one_of("status", STEP_STATUSES))

    id: Mapped[int] = _id()
    run_id: Mapped[int] = _fk("run.id", index=False)
    position: Mapped[int] = mapped_column(Integer)
    step: Mapped[str] = mapped_column(Text)  # "read", "inventory", "claims", …
    label: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    detail: Mapped[str | None] = mapped_column(Text)
    progress_done: Mapped[int | None] = mapped_column(Integer)
    progress_total: Mapped[int | None] = mapped_column(Integer)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class RunLog(Base):
    __tablename__ = "run_log"
    __table_args__ = (one_of("level", LOG_LEVELS),)

    id: Mapped[int] = _id()
    run_id: Mapped[int] = _fk("run.id")
    step: Mapped[str | None] = mapped_column(Text)
    level: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(Text)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = _created()


class RunArtifact(Base):
    """A file a run wrote (run.json, results.json, comment.md, report.html, …), as written."""

    __tablename__ = "run_artifact"
    __table_args__ = (UniqueConstraint("run_id", "name"),)

    id: Mapped[int] = _id()
    run_id: Mapped[int] = _fk("run.id", index=False)
    name: Mapped[str] = mapped_column(Text)
    media_type: Mapped[str] = mapped_column(Text)
    content: Mapped[bytes] = mapped_column(LargeBinary)
    sha256: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = _created()


# --- documentation: chunks, examples, inventory ----------------------------------------------


class Chunk(Base):
    """`chunking.Chunk`. `chunk_key` is its ID, which survives text edits."""

    __tablename__ = "chunk"
    __table_args__ = (UniqueConstraint("ingestion_id", "chunk_key"),)

    id: Mapped[int] = _id()
    ingestion_id: Mapped[int] = _fk("ingestion.id", index=False)
    chunk_key: Mapped[str] = mapped_column(Text)
    section_id: Mapped[str] = mapped_column(Text, index=True)
    content_hash: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(Text)
    heading_path: Mapped[list[str]] = mapped_column(ARRAY(Text))
    breadcrumb: Mapped[str] = mapped_column(Text)
    heading_level: Mapped[int] = mapped_column(Integer)
    occurrence: Mapped[int] = mapped_column(Integer)
    part: Mapped[int] = mapped_column(Integer)
    parts: Mapped[int] = mapped_column(Integer)
    start_line: Mapped[int] = mapped_column(Integer)
    end_line: Mapped[int] = mapped_column(Integer)
    tokens: Mapped[int] = mapped_column(Integer)
    oversized: Mapped[bool] = mapped_column(Boolean)
    text: Mapped[str] = mapped_column(Text)
    blocks: Mapped[list[Any]] = mapped_column(JSONB)


class Example(Base):
    """`examples.Example`: a code block of a chunk."""

    __tablename__ = "example"
    __table_args__ = (UniqueConstraint("ingestion_id", "example_key"),)

    id: Mapped[int] = _id()
    ingestion_id: Mapped[int] = _fk("ingestion.id", index=False)
    chunk_id: Mapped[int] = _fk("chunk.id")
    example_key: Mapped[str] = mapped_column(Text)
    section_id: Mapped[str] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer)
    content_hash: Mapped[str] = mapped_column(Text)
    lang: Mapped[str | None] = mapped_column(Text)
    code: Mapped[str] = mapped_column(Text)
    start_line: Mapped[int] = mapped_column(Integer)
    end_line: Mapped[int] = mapped_column(Integer)
    nested: Mapped[bool] = mapped_column(Boolean)


class ExampleCalls(Base):
    """What an adapter read from an example: `ExampleCalls` and `ExampleCallRecords`."""

    __tablename__ = "example_calls"
    __table_args__ = (UniqueConstraint("example_id", "adapter", "adapter_version"),)

    id: Mapped[int] = _id()
    example_id: Mapped[int] = _fk("example.id", index=False)
    adapter: Mapped[str] = mapped_column(Text)  # "python"
    adapter_version: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(Text)  # "ok", "invalid", "not-python"
    error: Mapped[str | None] = mapped_column(Text)
    calls: Mapped[list[Any]] = _json()  # CallRecord, resolved against the inventory
    unresolved: Mapped[list[Any]] = _json()
    additions: Mapped[list[Any]] = _json()  # called symbols missing in the inventory


class Symbol(Base):
    """`inventory.Symbol`."""

    __tablename__ = "symbol"
    __table_args__ = (UniqueConstraint("ingestion_id", "path"),)

    id: Mapped[int] = _id()
    ingestion_id: Mapped[int] = _fk("ingestion.id", index=False)
    path: Mapped[str] = mapped_column(Text)  # "urllib3.util.Retry.sleep", "POST /orders"
    kind: Mapped[str] = mapped_column(Text)
    sources: Mapped[list[Any]] = mapped_column(JSONB)


class Signature(Base):
    """`inventory.Signature`; a symbol can have several (overloads)."""

    __tablename__ = "signature"
    __table_args__ = (UniqueConstraint("symbol_id", "position"),)

    id: Mapped[int] = _id()
    symbol_id: Mapped[int] = _fk("symbol.id", index=False)
    position: Mapped[int] = mapped_column(Integer)
    text: Mapped[str | None] = mapped_column(Text)
    returns: Mapped[dict[str, Any] | None] = mapped_column(JSONB)  # ReturnType
    sources: Mapped[list[Any]] = mapped_column(JSONB)


class Parameter(Base):
    """`inventory.Parameter`, in signature order."""

    __tablename__ = "parameter"
    __table_args__ = (
        UniqueConstraint("signature_id", "position"),
        one_of("kind", PARAMETER_KINDS),
        one_of("location", PARAMETER_LOCATIONS, nullable=True),
        Index("ix_parameter_name", "name"),
    )

    id: Mapped[int] = _id()
    signature_id: Mapped[int] = _fk("signature.id", index=False)
    position: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(Text)
    required: Mapped[bool] = mapped_column(Boolean)
    type: Mapped[str | None] = mapped_column(Text)
    default: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(Text)  # OpenAPI only
    constraints: Mapped[list[Any]] = _json()
    sources: Mapped[list[Any]] = mapped_column(JSONB)


class Change(Base):
    """`inventory.Change`: the symbol is a path, whether or not it is in the inventory."""

    __tablename__ = "change"
    __table_args__ = (UniqueConstraint("ingestion_id", "position"), one_of("kind", CHANGE_KINDS))

    id: Mapped[int] = _id()
    ingestion_id: Mapped[int] = _fk("ingestion.id", index=False)
    position: Mapped[int] = mapped_column(Integer)  # the inventory's sorted order
    symbol: Mapped[str] = mapped_column(Text, index=True)
    kind: Mapped[str] = mapped_column(Text)
    version: Mapped[str] = mapped_column(Text)
    parameter: Mapped[str | None] = mapped_column(Text)
    replacement: Mapped[str | None] = mapped_column(Text)
    removal_planned: Mapped[str | None] = mapped_column(Text)
    sources: Mapped[list[Any]] = mapped_column(JSONB)


# --- claims and LLM calls ---------------------------------------------------------------------


class Claim(Base):
    """`claims.GroundedClaim`: an extracted claim and how grounding decided on it (SPEC §6.4).

    Dropped claims are stored too, with their status.
    """

    __tablename__ = "claim"
    __table_args__ = (
        UniqueConstraint("run_id", "chunk_id", "extractor", "local_id"),
        one_of("type", CLAIM_TYPES),
        one_of("status", GROUNDING_STATUSES),
    )

    id: Mapped[int] = _id()
    run_id: Mapped[int] = _fk("run.id", index=False)
    chunk_id: Mapped[int] = _fk("chunk.id")
    extractor: Mapped[str] = mapped_column(Text)
    local_id: Mapped[str] = mapped_column(Text)  # "c1" from the answer
    text: Mapped[str] = mapped_column(Text)
    citation: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(Text)
    prompt_version: Mapped[int] = mapped_column(Integer)
    prompt_hash: Mapped[str] = mapped_column(Text)
    model: Mapped[str] = mapped_column(Text)  # the model that answered
    extraction_run: Mapped[str] = mapped_column(Text)  # run ID of the answer, when reused
    status: Mapped[str] = mapped_column(Text)
    citation_start: Mapped[int | None] = mapped_column(Integer)
    citation_end: Mapped[int | None] = mapped_column(Integer)
    citation_matches: Mapped[int] = mapped_column(Integer)
    premise_candidates: Mapped[int] = mapped_column(Integer)
    premise: Mapped[str | None] = mapped_column(Text)
    premise_start: Mapped[int | None] = mapped_column(Integer)
    premise_end: Mapped[int | None] = mapped_column(Integer)
    nli: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    missing: Mapped[list[str]] = _texts()
    versions: Mapped[dict[str, Any]] = mapped_column(JSONB)  # GroundingVersions


class ExtractionIssue(Base):
    """A chunk an extractor gave no claims for (failure), or a claim it skipped (problem)."""

    __tablename__ = "extraction_issue"
    __table_args__ = (one_of("kind", EXTRACTION_ISSUES),)

    id: Mapped[int] = _id()
    run_id: Mapped[int] = _fk("run.id")
    chunk_key: Mapped[str] = mapped_column(Text)
    extractor: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(Text)
    cause: Mapped[str | None] = mapped_column(Text)  # ExtractionCause, failures only
    detail: Mapped[str] = mapped_column(Text)


class ClaimAnswer(Base):
    """The claim store (`claims.store`): parsed answers, reused while the key stays the same.

    Append-only: a later answer for the same key wins (highest id).
    """

    __tablename__ = "claim_answer"
    __table_args__ = (
        Index(
            "ix_claim_answer_key",
            "content_hash",
            "breadcrumb",
            "extractor",
            "model",
            "prompt_version",
        ),
    )

    id: Mapped[int] = _id()
    content_hash: Mapped[str] = mapped_column(Text)
    breadcrumb: Mapped[str] = mapped_column(Text)
    extractor: Mapped[str] = mapped_column(Text)
    model: Mapped[str] = mapped_column(Text)
    prompt_version: Mapped[int] = mapped_column(Integer)
    reasoning_effort: Mapped[str | None] = mapped_column(Text)
    parser_version: Mapped[int | None] = mapped_column(Integer)
    thinking: Mapped[bool | None] = mapped_column(Boolean)
    claims: Mapped[list[Any]] = mapped_column(JSONB)  # RawClaim
    problems: Mapped[list[str]] = _texts()
    run_ref: Mapped[str] = mapped_column(Text)
    prompt_hash: Mapped[str] = mapped_column(Text)
    answered_model: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = _created()


class LlmCall(Base):
    """Every request sent to an LLM, for every role of SPEC §8, with the raw response.

    Append-only (SPEC §10): raw responses cannot be reconstructed.
    """

    __tablename__ = "llm_call"
    __table_args__ = (one_of("role", LLM_ROLES),)

    id: Mapped[int] = _id()
    run_id: Mapped[int | None] = _fk("run.id", nullable=True)
    run_ref: Mapped[str] = mapped_column(Text)  # the run ID the caller used (CLI runs too)
    role: Mapped[str] = mapped_column(Text)
    actor: Mapped[str | None] = mapped_column(Text)  # e.g. the extractor's name
    chunk_key: Mapped[str | None] = mapped_column(Text)
    test_item_id: Mapped[int | None] = _fk("test_item.id", nullable=True)
    model: Mapped[str] = mapped_column(Text)  # requested
    answered_model: Mapped[str | None] = mapped_column(Text)  # as the provider reported it
    prompt_hash: Mapped[str] = mapped_column(Text, index=True)
    request: Mapped[dict[str, Any]] = mapped_column(JSONB)  # the whole ChatRequest
    response: Mapped[dict[str, Any] | None] = mapped_column(JSONB)  # NULL: no answer came back
    error: Mapped[str | None] = mapped_column(Text)
    tokens_in: Mapped[int | None] = mapped_column(Integer)
    tokens_out: Mapped[int | None] = mapped_column(Integer)
    cost_usd: Mapped[Decimal | None] = mapped_column(Numeric(12, 6))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # when it came back


# --- golden set, results, findings ------------------------------------------------------------


class TestItem(Base):
    """A test item (SPEC §6.7, §10). Never updated: a change is a new item.

    `identity_key` is built from the deterministic parts only (project, chunk, level, operator
    and its version, format, difficulty, source example, canonical reference). The task text is
    written by an LLM and is not part of it.
    """

    __test__ = False  # not a pytest class
    __tablename__ = "test_item"
    __table_args__ = (
        UniqueConstraint("project_id", "identity_key"),
        one_of("level", LEVELS),
        one_of("operator", OPERATORS, nullable=True),
    )

    id: Mapped[int] = _id()
    project_id: Mapped[int] = _fk("project.id", index=False)
    identity_key: Mapped[str] = mapped_column(Text)
    level: Mapped[str] = mapped_column(Text)
    operator: Mapped[str | None] = mapped_column(Text)  # NULL for L0 / L1 questions
    operator_version: Mapped[int] = mapped_column(Integer)
    format: Mapped[str] = mapped_column(Text)  # "python", "curl", …
    difficulty: Mapped[str] = mapped_column(Text)  # "explicit-single-step", …
    question_kind: Mapped[str | None] = mapped_column(Text)  # L0 / L1: "exists", "default", …
    chunk_key: Mapped[str] = mapped_column(Text)
    chunk_keys: Mapped[list[str]] = _texts()  # every chunk of the gold context
    source_example_key: Mapped[str | None] = mapped_column(Text)
    symbol_path: Mapped[str | None] = mapped_column(Text, index=True)
    reference: Mapped[dict[str, Any]] = mapped_column(JSONB)  # computed by code
    wording: Mapped[dict[str, Any]] = mapped_column(JSONB)  # task text, paraphrases, options
    sources: Mapped[list[Any]] = _json()
    generator_version: Mapped[int] = mapped_column(Integer)  # metadata, not in the key
    input_snapshot_id: Mapped[int] = _fk("input_snapshot.id")  # where it was generated
    docs_version: Mapped[str | None] = mapped_column(Text)
    origin_run_id: Mapped[int | None] = _fk("run.id", nullable=True)  # PR (candidate) or main
    flags: Mapped[list[str]] = _texts()  # "parametric_known" (SPEC §6.8)
    created_at: Mapped[datetime] = _created()


class GoldenSetVersion(Base):
    """Project + input snapshot + generator version, with a parent (SPEC §10)."""

    __tablename__ = "golden_set_version"
    __table_args__ = (UniqueConstraint("project_id", "input_snapshot_id", "generator_version"),)

    id: Mapped[int] = _id()
    project_id: Mapped[int] = _fk("project.id", index=False)
    input_snapshot_id: Mapped[int] = _fk("input_snapshot.id")
    generator_version: Mapped[int] = mapped_column(Integer)
    parent_id: Mapped[int | None] = _fk("golden_set_version.id", nullable=True)
    created_at: Mapped[datetime] = _created()


class GoldenSetCommit(Base):
    """A commit that produced a golden-set version: metadata, many commits can give one."""

    __tablename__ = "golden_set_commit"
    __table_args__ = (UniqueConstraint("version_id", "commit_sha"),)

    id: Mapped[int] = _id()
    version_id: Mapped[int] = _fk("golden_set_version.id", index=False)
    commit_sha: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = _created()


class GoldenSetItem(Base):
    """An item of a golden-set version; unchanged items are referenced, never copied."""

    __tablename__ = "golden_set_item"
    __table_args__ = (PrimaryKeyConstraint("version_id", "test_item_id"),)

    version_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("golden_set_version.id"))
    test_item_id: Mapped[int] = _fk("test_item.id")


class ReviewDecision(Base):
    """A review decision (SPEC §2.5, §10); an item's state is its latest decision.

    `reviewer` is a GitHub login, `auto` for an automatic approval, or `pr-closed` for a
    candidate rejected because its PR was closed without merging.
    """

    __tablename__ = "review_decision"
    __table_args__ = (one_of("decision", DECISIONS),)

    id: Mapped[int] = _id()
    test_item_id: Mapped[int] = _fk("test_item.id")
    decision: Mapped[str] = mapped_column(Text)
    reviewer: Mapped[str] = mapped_column(Text)
    reason: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = _created()


class RunTestItem(Base):
    """How a run used an item (SPEC §7): stable, superseded in this PR, or a candidate."""

    __tablename__ = "run_test_item"
    __table_args__ = (PrimaryKeyConstraint("run_id", "test_item_id"), one_of("role", ITEM_ROLES))

    run_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("run.id"))
    test_item_id: Mapped[int] = _fk("test_item.id")
    role: Mapped[str] = mapped_column(Text)


class Result(Base):
    """One test item × model × mode (× paraphrase × repeat) of a run (SPEC §6.10, §10).

    Commit, input snapshot and docs version come through the run, the generator version through
    the item, the raw response through `llm_call`.
    """

    __tablename__ = "result"
    __table_args__ = (
        UniqueConstraint("run_id", "test_item_id", "model", "mode", "paraphrase", "repeat"),
        one_of("mode", MODES),
        one_of("error_category", ERROR_CATEGORIES, nullable=True),
        one_of("deprecated_kind", ("deprecated", "removed"), nullable=True),
    )

    id: Mapped[int] = _id()
    run_id: Mapped[int] = _fk("run.id", index=False)
    test_item_id: Mapped[int] = _fk("test_item.id")
    golden_set_version_id: Mapped[int | None] = _fk("golden_set_version.id", nullable=True)
    model: Mapped[str] = mapped_column(Text)
    model_params: Mapped[dict[str, Any]] = _json("'{}'::jsonb")
    mode: Mapped[str] = mapped_column(Text)
    paraphrase: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    repeat: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    llm_call_id: Mapped[int | None] = _fk("llm_call.id", nullable=True)
    parsed: Mapped[dict[str, Any] | None] = mapped_column(JSONB)  # e.g. the answer's CallRecord
    passed: Mapped[bool | None] = mapped_column(Boolean)  # NULL: not evaluated
    error_category: Mapped[str | None] = mapped_column(Text)
    deprecated_kind: Mapped[str | None] = mapped_column(Text)
    evaluation: Mapped[dict[str, Any] | None] = mapped_column(JSONB)  # argument comparison, …
    evaluator_version: Mapped[int] = mapped_column(Integer)
    cost_usd: Mapped[Decimal | None] = mapped_column(Numeric(12, 6))
    created_at: Mapped[datetime] = _created()


class Finding(Base):
    """A problem in the docs from a cross-check (SPEC §6.5). `key` identifies the problem.

    Open or fixed is derived: open while the key is in the project's latest main run.
    """

    __tablename__ = "finding"
    __table_args__ = (
        UniqueConstraint("run_id", "key"),
        one_of("check_code", CHECKS),
        one_of("confidence", CONFIDENCES),
        Index("ix_finding_key", "key"),
    )

    id: Mapped[int] = _id()
    run_id: Mapped[int] = _fk("run.id", index=False)
    key: Mapped[str] = mapped_column(Text)
    check_code: Mapped[str] = mapped_column(Text)  # "K1" … "K7"; CHECK is a reserved word
    kind: Mapped[str] = mapped_column(Text)
    subject: Mapped[str] = mapped_column(Text)
    message: Mapped[str] = mapped_column(Text)  # from a template in code, never an LLM
    confidence: Mapped[str] = mapped_column(Text)
    evidence: Mapped[list[Any]] = mapped_column(JSONB)
    nli: Mapped[list[Any]] = _json()
    versions: Mapped[dict[str, Any]] = _json("'{}'::jsonb")
    created_at: Mapped[datetime] = _created()
