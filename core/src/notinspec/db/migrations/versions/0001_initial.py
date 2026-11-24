# ruff: noqa: E501  (generated CHECK lists)
"""Initial schema: projects, inputs, runs, docs, inventory, claims, LLM calls, golden set,
results and findings (SPEC §10), with the append-only tables guarded in the database.

Revision ID: 0001
Revises:
Create Date: 2026-11-22
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# frozen copy of models.APPEND_ONLY at this revision: a migration never imports models
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
APP_ROLE = "notinspec_app"  # the role the API and the worker connect as (docs/DEPLOY.md)


def upgrade() -> None:
    op.create_table(
        "claim_answer",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.Column("breadcrumb", sa.Text(), nullable=False),
        sa.Column("extractor", sa.Text(), nullable=False),
        sa.Column("model", sa.Text(), nullable=False),
        sa.Column("prompt_version", sa.Integer(), nullable=False),
        sa.Column("reasoning_effort", sa.Text(), nullable=True),
        sa.Column("parser_version", sa.Integer(), nullable=True),
        sa.Column("thinking", sa.Boolean(), nullable=True),
        sa.Column("claims", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "problems",
            postgresql.ARRAY(sa.Text()),
            server_default=sa.text("'{}'::text[]"),
            nullable=False,
        ),
        sa.Column("run_ref", sa.Text(), nullable=False),
        sa.Column("prompt_hash", sa.Text(), nullable=False),
        sa.Column("answered_model", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_claim_answer")),
    )
    op.create_table(
        "project",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("slug", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("repository", sa.Text(), nullable=True),
        sa.Column("repository_id", sa.BigInteger(), nullable=True),
        sa.Column("default_branch", sa.Text(), nullable=True),
        sa.Column("workflow_path", sa.Text(), nullable=True),
        sa.Column(
            "allowed_models",
            postgresql.ARRAY(sa.Text()),
            server_default=sa.text("'{}'::text[]"),
            nullable=False,
        ),
        sa.Column("budget_per_run_usd", sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column("budget_per_month_usd", sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column("max_upload_bytes", sa.BigInteger(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project")),
        sa.UniqueConstraint("repository_id", name=op.f("uq_project_repository_id")),
        sa.UniqueConstraint("slug", name=op.f("uq_project_slug")),
    )
    op.create_table(
        "input_snapshot",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("project_id", sa.BigInteger(), nullable=False),
        sa.Column("input_hash", sa.Text(), nullable=False),
        sa.Column("docs_version", sa.Text(), nullable=True),
        sa.Column("archive_sha256", sa.Text(), nullable=True),
        sa.Column("archive_bytes", sa.BigInteger(), nullable=True),
        sa.Column("archive_path", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["project.id"], name=op.f("fk_input_snapshot_project_id_project")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_input_snapshot")),
        sa.UniqueConstraint(
            "project_id", "input_hash", name=op.f("uq_input_snapshot_project_id_input_hash")
        ),
    )
    op.create_table(
        "pr_closed",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("project_id", sa.BigInteger(), nullable=False),
        sa.Column("pr_number", sa.Integer(), nullable=False),
        sa.Column("github_run_id", sa.BigInteger(), nullable=False),
        sa.Column("claims", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["project.id"], name=op.f("fk_pr_closed_project_id_project")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pr_closed")),
    )
    op.create_table(
        "golden_set_version",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("project_id", sa.BigInteger(), nullable=False),
        sa.Column("input_snapshot_id", sa.BigInteger(), nullable=False),
        sa.Column("generator_version", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["input_snapshot_id"],
            ["input_snapshot.id"],
            name=op.f("fk_golden_set_version_input_snapshot_id_input_snapshot"),
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["golden_set_version.id"],
            name=op.f("fk_golden_set_version_parent_id_golden_set_version"),
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["project.id"], name=op.f("fk_golden_set_version_project_id_project")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_golden_set_version")),
        sa.UniqueConstraint(
            "project_id",
            "input_snapshot_id",
            "generator_version",
            name=op.f("uq_golden_set_version_project_id_input_snapshot_id_generator_version"),
        ),
    )
    op.create_table(
        "ingestion",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("snapshot_id", sa.BigInteger(), nullable=False),
        sa.Column("config_hash", sa.Text(), nullable=False),
        sa.Column("versions", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("versions_hash", sa.Text(), nullable=False),
        sa.Column(
            "warnings",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "conflicts",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "openapi",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["snapshot_id"],
            ["input_snapshot.id"],
            name=op.f("fk_ingestion_snapshot_id_input_snapshot"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ingestion")),
        sa.UniqueConstraint(
            "snapshot_id",
            "config_hash",
            "versions_hash",
            name=op.f("uq_ingestion_snapshot_id_config_hash_versions_hash"),
        ),
    )
    op.create_table(
        "source_file",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("snapshot_id", sa.BigInteger(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["snapshot_id"],
            ["input_snapshot.id"],
            name=op.f("fk_source_file_snapshot_id_input_snapshot"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_source_file")),
        sa.UniqueConstraint("snapshot_id", "path", name=op.f("uq_source_file_snapshot_id_path")),
    )
    op.create_table(
        "change",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("ingestion_id", sa.BigInteger(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("symbol", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("version", sa.Text(), nullable=False),
        sa.Column("parameter", sa.Text(), nullable=True),
        sa.Column("replacement", sa.Text(), nullable=True),
        sa.Column("removal_planned", sa.Text(), nullable=True),
        sa.Column("sources", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.CheckConstraint(
            "kind IN ('added', 'deprecated', 'removed')", name=op.f("ck_change_kind")
        ),
        sa.ForeignKeyConstraint(
            ["ingestion_id"], ["ingestion.id"], name=op.f("fk_change_ingestion_id_ingestion")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_change")),
        sa.UniqueConstraint(
            "ingestion_id", "position", name=op.f("uq_change_ingestion_id_position")
        ),
    )
    op.create_table(
        "chunk",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("ingestion_id", sa.BigInteger(), nullable=False),
        sa.Column("chunk_key", sa.Text(), nullable=False),
        sa.Column("section_id", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("heading_path", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("breadcrumb", sa.Text(), nullable=False),
        sa.Column("heading_level", sa.Integer(), nullable=False),
        sa.Column("occurrence", sa.Integer(), nullable=False),
        sa.Column("part", sa.Integer(), nullable=False),
        sa.Column("parts", sa.Integer(), nullable=False),
        sa.Column("start_line", sa.Integer(), nullable=False),
        sa.Column("end_line", sa.Integer(), nullable=False),
        sa.Column("tokens", sa.Integer(), nullable=False),
        sa.Column("oversized", sa.Boolean(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("blocks", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(
            ["ingestion_id"], ["ingestion.id"], name=op.f("fk_chunk_ingestion_id_ingestion")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_chunk")),
        sa.UniqueConstraint(
            "ingestion_id", "chunk_key", name=op.f("uq_chunk_ingestion_id_chunk_key")
        ),
    )
    op.create_table(
        "golden_set_commit",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("version_id", sa.BigInteger(), nullable=False),
        sa.Column("commit_sha", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["version_id"],
            ["golden_set_version.id"],
            name=op.f("fk_golden_set_commit_version_id_golden_set_version"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_golden_set_commit")),
        sa.UniqueConstraint(
            "version_id", "commit_sha", name=op.f("uq_golden_set_commit_version_id_commit_sha")
        ),
    )
    op.create_table(
        "run",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("public_id", sa.Text(), nullable=False),
        sa.Column("project_id", sa.BigInteger(), nullable=False),
        sa.Column("ingestion_id", sa.BigInteger(), nullable=True),
        sa.Column("golden_set_version_id", sa.BigInteger(), nullable=True),
        sa.Column("baseline_run_id", sa.BigInteger(), nullable=True),
        sa.Column("trigger", sa.Text(), nullable=False),
        sa.Column("commit_sha", sa.Text(), nullable=True),
        sa.Column("ref", sa.Text(), nullable=True),
        sa.Column("pr_number", sa.Integer(), nullable=True),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("verdict", sa.Text(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("error_kind", sa.Text(), nullable=True),
        sa.Column("comment_md", sa.Text(), nullable=True),
        sa.Column("tool_version", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "error_kind IS NULL OR error_kind IN ('input', 'internal')",
            name=op.f("ck_run_error_kind"),
        ),
        sa.CheckConstraint(
            "status IN ('queued', 'running', 'done', 'error')", name=op.f("ck_run_status")
        ),
        sa.CheckConstraint(
            "trigger IN ('cli', 'pull_request', 'push', 'workflow_dispatch', 'nightly')",
            name=op.f("ck_run_trigger"),
        ),
        sa.CheckConstraint(
            "verdict IS NULL OR verdict IN ('pass', 'fail')", name=op.f("ck_run_verdict")
        ),
        sa.ForeignKeyConstraint(
            ["baseline_run_id"], ["run.id"], name=op.f("fk_run_baseline_run_id_run")
        ),
        sa.ForeignKeyConstraint(
            ["golden_set_version_id"],
            ["golden_set_version.id"],
            name=op.f("fk_run_golden_set_version_id_golden_set_version"),
        ),
        sa.ForeignKeyConstraint(
            ["ingestion_id"], ["ingestion.id"], name=op.f("fk_run_ingestion_id_ingestion")
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["project.id"], name=op.f("fk_run_project_id_project")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_run")),
        sa.UniqueConstraint("public_id", name=op.f("uq_run_public_id")),
    )
    op.create_table(
        "symbol",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("ingestion_id", sa.BigInteger(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("sources", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(
            ["ingestion_id"], ["ingestion.id"], name=op.f("fk_symbol_ingestion_id_ingestion")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_symbol")),
        sa.UniqueConstraint("ingestion_id", "path", name=op.f("uq_symbol_ingestion_id_path")),
    )
    op.create_table(
        "claim",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("chunk_id", sa.BigInteger(), nullable=False),
        sa.Column("extractor", sa.Text(), nullable=False),
        sa.Column("local_id", sa.Text(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("citation", sa.Text(), nullable=False),
        sa.Column("type", sa.Text(), nullable=False),
        sa.Column("prompt_version", sa.Integer(), nullable=False),
        sa.Column("prompt_hash", sa.Text(), nullable=False),
        sa.Column("model", sa.Text(), nullable=False),
        sa.Column("extraction_run", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("citation_start", sa.Integer(), nullable=True),
        sa.Column("citation_end", sa.Integer(), nullable=True),
        sa.Column("citation_matches", sa.Integer(), nullable=False),
        sa.Column("premise_candidates", sa.Integer(), nullable=False),
        sa.Column("premise", sa.Text(), nullable=True),
        sa.Column("premise_start", sa.Integer(), nullable=True),
        sa.Column("premise_end", sa.Integer(), nullable=True),
        sa.Column("nli", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "missing",
            postgresql.ARRAY(sa.Text()),
            server_default=sa.text("'{}'::text[]"),
            nullable=False,
        ),
        sa.Column("versions", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.CheckConstraint(
            "status IN ('kept', 'citation_not_found', 'not_checkable', 'nli_neutral', 'nli_contradiction', 'id_missing')",
            name=op.f("ck_claim_status"),
        ),
        sa.CheckConstraint("type IN ('fact', 'change')", name=op.f("ck_claim_type")),
        sa.ForeignKeyConstraint(["chunk_id"], ["chunk.id"], name=op.f("fk_claim_chunk_id_chunk")),
        sa.ForeignKeyConstraint(["run_id"], ["run.id"], name=op.f("fk_claim_run_id_run")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_claim")),
        sa.UniqueConstraint(
            "run_id",
            "chunk_id",
            "extractor",
            "local_id",
            name=op.f("uq_claim_run_id_chunk_id_extractor_local_id"),
        ),
    )
    op.create_table(
        "example",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("ingestion_id", sa.BigInteger(), nullable=False),
        sa.Column("chunk_id", sa.BigInteger(), nullable=False),
        sa.Column("example_key", sa.Text(), nullable=False),
        sa.Column("section_id", sa.Text(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.Column("lang", sa.Text(), nullable=True),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("start_line", sa.Integer(), nullable=False),
        sa.Column("end_line", sa.Integer(), nullable=False),
        sa.Column("nested", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["chunk_id"], ["chunk.id"], name=op.f("fk_example_chunk_id_chunk")),
        sa.ForeignKeyConstraint(
            ["ingestion_id"], ["ingestion.id"], name=op.f("fk_example_ingestion_id_ingestion")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_example")),
        sa.UniqueConstraint(
            "ingestion_id", "example_key", name=op.f("uq_example_ingestion_id_example_key")
        ),
    )
    op.create_table(
        "extraction_issue",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("chunk_key", sa.Text(), nullable=False),
        sa.Column("extractor", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("cause", sa.Text(), nullable=True),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.CheckConstraint("kind IN ('failure', 'problem')", name=op.f("ck_extraction_issue_kind")),
        sa.ForeignKeyConstraint(
            ["run_id"], ["run.id"], name=op.f("fk_extraction_issue_run_id_run")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_extraction_issue")),
    )
    op.create_table(
        "finding",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("key", sa.Text(), nullable=False),
        sa.Column("check_code", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("subject", sa.Text(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Text(), nullable=False),
        sa.Column("evidence", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "nli",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "versions",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "check_code IN ('K1', 'K2', 'K3', 'K4', 'K5a', 'K5b', 'K6', 'K7')",
            name=op.f("ck_finding_check_code"),
        ),
        sa.CheckConstraint(
            "confidence IN ('high', 'medium', 'low')", name=op.f("ck_finding_confidence")
        ),
        sa.ForeignKeyConstraint(["run_id"], ["run.id"], name=op.f("fk_finding_run_id_run")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_finding")),
        sa.UniqueConstraint("run_id", "key", name=op.f("uq_finding_run_id_key")),
    )
    op.create_table(
        "run_artifact",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("media_type", sa.Text(), nullable=False),
        sa.Column("content", sa.LargeBinary(), nullable=False),
        sa.Column("sha256", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["run_id"], ["run.id"], name=op.f("fk_run_artifact_run_id_run")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_run_artifact")),
        sa.UniqueConstraint("run_id", "name", name=op.f("uq_run_artifact_run_id_name")),
    )
    op.create_table(
        "run_log",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("step", sa.Text(), nullable=True),
        sa.Column("level", sa.Text(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "level IN ('debug', 'info', 'warning', 'error')", name=op.f("ck_run_log_level")
        ),
        sa.ForeignKeyConstraint(["run_id"], ["run.id"], name=op.f("fk_run_log_run_id_run")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_run_log")),
    )
    op.create_table(
        "run_step",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("step", sa.Text(), nullable=False),
        sa.Column("label", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("progress_done", sa.Integer(), nullable=True),
        sa.Column("progress_total", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('pending', 'running', 'done', 'failed', 'skipped', 'not_implemented')",
            name=op.f("ck_run_step_status"),
        ),
        sa.ForeignKeyConstraint(["run_id"], ["run.id"], name=op.f("fk_run_step_run_id_run")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_run_step")),
        sa.UniqueConstraint("run_id", "step", name=op.f("uq_run_step_run_id_step")),
    )
    op.create_table(
        "signature",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("symbol_id", sa.BigInteger(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("returns", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("sources", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(
            ["symbol_id"], ["symbol.id"], name=op.f("fk_signature_symbol_id_symbol")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_signature")),
        sa.UniqueConstraint("symbol_id", "position", name=op.f("uq_signature_symbol_id_position")),
    )
    op.create_table(
        "test_item",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("project_id", sa.BigInteger(), nullable=False),
        sa.Column("identity_key", sa.Text(), nullable=False),
        sa.Column("level", sa.Text(), nullable=False),
        sa.Column("operator", sa.Text(), nullable=True),
        sa.Column("operator_version", sa.Integer(), nullable=False),
        sa.Column("format", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.Text(), nullable=False),
        sa.Column("question_kind", sa.Text(), nullable=True),
        sa.Column("chunk_key", sa.Text(), nullable=False),
        sa.Column(
            "chunk_keys",
            postgresql.ARRAY(sa.Text()),
            server_default=sa.text("'{}'::text[]"),
            nullable=False,
        ),
        sa.Column("source_example_key", sa.Text(), nullable=True),
        sa.Column("symbol_path", sa.Text(), nullable=True),
        sa.Column("reference", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("wording", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "sources",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column("generator_version", sa.Integer(), nullable=False),
        sa.Column("input_snapshot_id", sa.BigInteger(), nullable=False),
        sa.Column("docs_version", sa.Text(), nullable=True),
        sa.Column("origin_run_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "flags",
            postgresql.ARRAY(sa.Text()),
            server_default=sa.text("'{}'::text[]"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "level IN ('L0', 'L1', 'L2', 'L3', 'L4')", name=op.f("ck_test_item_level")
        ),
        sa.CheckConstraint(
            "operator IS NULL OR operator IN ('copy', 'adaptation', 'variation', 'composition', 'migration', 'perturbation')",
            name=op.f("ck_test_item_operator"),
        ),
        sa.ForeignKeyConstraint(
            ["input_snapshot_id"],
            ["input_snapshot.id"],
            name=op.f("fk_test_item_input_snapshot_id_input_snapshot"),
        ),
        sa.ForeignKeyConstraint(
            ["origin_run_id"], ["run.id"], name=op.f("fk_test_item_origin_run_id_run")
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["project.id"], name=op.f("fk_test_item_project_id_project")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_test_item")),
        sa.UniqueConstraint(
            "project_id", "identity_key", name=op.f("uq_test_item_project_id_identity_key")
        ),
    )
    op.create_table(
        "upload",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("project_id", sa.BigInteger(), nullable=False),
        sa.Column("repository_id", sa.BigInteger(), nullable=False),
        sa.Column("github_run_id", sa.BigInteger(), nullable=False),
        sa.Column("github_run_attempt", sa.Integer(), nullable=False),
        sa.Column("event_name", sa.Text(), nullable=False),
        sa.Column("ref", sa.Text(), nullable=False),
        sa.Column("sha", sa.Text(), nullable=False),
        sa.Column("workflow_ref", sa.Text(), nullable=False),
        sa.Column("pr_number", sa.Integer(), nullable=True),
        sa.Column("head_sha", sa.Text(), nullable=True),
        sa.Column("base_sha", sa.Text(), nullable=True),
        sa.Column("archive_sha256", sa.Text(), nullable=False),
        sa.Column("archive_bytes", sa.BigInteger(), nullable=False),
        sa.Column("claims", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "event_name IN ('pull_request', 'push', 'workflow_dispatch')",
            name=op.f("ck_upload_event_name"),
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["project.id"], name=op.f("fk_upload_project_id_project")
        ),
        sa.ForeignKeyConstraint(["run_id"], ["run.id"], name=op.f("fk_upload_run_id_run")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_upload")),
        sa.UniqueConstraint(
            "project_id",
            "github_run_id",
            "github_run_attempt",
            name=op.f("uq_upload_project_id_github_run_id_github_run_attempt"),
        ),
        sa.UniqueConstraint("run_id", name=op.f("uq_upload_run_id")),
    )
    op.create_table(
        "example_calls",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("example_id", sa.BigInteger(), nullable=False),
        sa.Column("adapter", sa.Text(), nullable=False),
        sa.Column("adapter_version", sa.Integer(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column(
            "calls",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "unresolved",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "additions",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["example_id"], ["example.id"], name=op.f("fk_example_calls_example_id_example")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_example_calls")),
        sa.UniqueConstraint(
            "example_id",
            "adapter",
            "adapter_version",
            name=op.f("uq_example_calls_example_id_adapter_adapter_version"),
        ),
    )
    op.create_table(
        "golden_set_item",
        sa.Column("version_id", sa.BigInteger(), nullable=False),
        sa.Column("test_item_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["test_item_id"],
            ["test_item.id"],
            name=op.f("fk_golden_set_item_test_item_id_test_item"),
        ),
        sa.ForeignKeyConstraint(
            ["version_id"],
            ["golden_set_version.id"],
            name=op.f("fk_golden_set_item_version_id_golden_set_version"),
        ),
        sa.PrimaryKeyConstraint("version_id", "test_item_id", name=op.f("pk_golden_set_item")),
    )
    op.create_table(
        "llm_call",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=True),
        sa.Column("run_ref", sa.Text(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("actor", sa.Text(), nullable=True),
        sa.Column("chunk_key", sa.Text(), nullable=True),
        sa.Column("test_item_id", sa.BigInteger(), nullable=True),
        sa.Column("model", sa.Text(), nullable=False),
        sa.Column("answered_model", sa.Text(), nullable=True),
        sa.Column("prompt_hash", sa.Text(), nullable=False),
        sa.Column("request", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("response", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("tokens_in", sa.Integer(), nullable=True),
        sa.Column("tokens_out", sa.Integer(), nullable=True),
        sa.Column("cost_usd", sa.Numeric(precision=12, scale=6), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "role IN ('model-under-test', 'claim-extractor', 'task-writer', 'round-trip-solver', 'judge')",
            name=op.f("ck_llm_call_role"),
        ),
        sa.ForeignKeyConstraint(["run_id"], ["run.id"], name=op.f("fk_llm_call_run_id_run")),
        sa.ForeignKeyConstraint(
            ["test_item_id"], ["test_item.id"], name=op.f("fk_llm_call_test_item_id_test_item")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_llm_call")),
    )
    op.create_table(
        "parameter",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("signature_id", sa.BigInteger(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False),
        sa.Column("type", sa.Text(), nullable=True),
        sa.Column("default", sa.Text(), nullable=True),
        sa.Column("location", sa.Text(), nullable=True),
        sa.Column(
            "constraints",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column("sources", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.CheckConstraint(
            "kind IN ('positional_only', 'positional_or_keyword', 'var_positional', 'keyword_only', 'var_keyword')",
            name=op.f("ck_parameter_kind"),
        ),
        sa.CheckConstraint(
            "location IS NULL OR location IN ('path', 'query', 'header', 'cookie', 'body')",
            name=op.f("ck_parameter_location"),
        ),
        sa.ForeignKeyConstraint(
            ["signature_id"], ["signature.id"], name=op.f("fk_parameter_signature_id_signature")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parameter")),
        sa.UniqueConstraint(
            "signature_id", "position", name=op.f("uq_parameter_signature_id_position")
        ),
    )
    op.create_table(
        "review_decision",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("test_item_id", sa.BigInteger(), nullable=False),
        sa.Column("decision", sa.Text(), nullable=False),
        sa.Column("reviewer", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "decision IN ('approved', 'rejected')", name=op.f("ck_review_decision_decision")
        ),
        sa.ForeignKeyConstraint(
            ["test_item_id"],
            ["test_item.id"],
            name=op.f("fk_review_decision_test_item_id_test_item"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_review_decision")),
    )
    op.create_table(
        "run_test_item",
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("test_item_id", sa.BigInteger(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.CheckConstraint(
            "role IN ('stable', 'superseded', 'candidate')", name=op.f("ck_run_test_item_role")
        ),
        sa.ForeignKeyConstraint(["run_id"], ["run.id"], name=op.f("fk_run_test_item_run_id_run")),
        sa.ForeignKeyConstraint(
            ["test_item_id"], ["test_item.id"], name=op.f("fk_run_test_item_test_item_id_test_item")
        ),
        sa.PrimaryKeyConstraint("run_id", "test_item_id", name=op.f("pk_run_test_item")),
    )
    op.create_table(
        "result",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("test_item_id", sa.BigInteger(), nullable=False),
        sa.Column("golden_set_version_id", sa.BigInteger(), nullable=True),
        sa.Column("model", sa.Text(), nullable=False),
        sa.Column(
            "model_params",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("mode", sa.Text(), nullable=False),
        sa.Column("paraphrase", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("repeat", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("llm_call_id", sa.BigInteger(), nullable=True),
        sa.Column("parsed", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("passed", sa.Boolean(), nullable=True),
        sa.Column("error_category", sa.Text(), nullable=True),
        sa.Column("deprecated_kind", sa.Text(), nullable=True),
        sa.Column("evaluation", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("evaluator_version", sa.Integer(), nullable=False),
        sa.Column("cost_usd", sa.Numeric(precision=12, scale=6), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "deprecated_kind IS NULL OR deprecated_kind IN ('deprecated', 'removed')",
            name=op.f("ck_result_deprecated_kind"),
        ),
        sa.CheckConstraint(
            "error_category IS NULL OR error_category IN ('success', 'wrong-symbol', 'wrong-arguments', 'hallucinated-api', 'deprecated-api', 'api-bypass', 'invalid-format', 'invented')",
            name=op.f("ck_result_error_category"),
        ),
        sa.CheckConstraint("mode IN ('none', 'retrieved', 'gold')", name=op.f("ck_result_mode")),
        sa.ForeignKeyConstraint(
            ["golden_set_version_id"],
            ["golden_set_version.id"],
            name=op.f("fk_result_golden_set_version_id_golden_set_version"),
        ),
        sa.ForeignKeyConstraint(
            ["llm_call_id"], ["llm_call.id"], name=op.f("fk_result_llm_call_id_llm_call")
        ),
        sa.ForeignKeyConstraint(["run_id"], ["run.id"], name=op.f("fk_result_run_id_run")),
        sa.ForeignKeyConstraint(
            ["test_item_id"], ["test_item.id"], name=op.f("fk_result_test_item_id_test_item")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_result")),
        sa.UniqueConstraint(
            "run_id",
            "test_item_id",
            "model",
            "mode",
            "paraphrase",
            "repeat",
            name=op.f("uq_result_run_id_test_item_id_model_mode_paraphrase_repeat"),
        ),
    )
    op.create_index(
        "ix_claim_answer_key",
        "claim_answer",
        ["content_hash", "breadcrumb", "extractor", "model", "prompt_version"],
        unique=False,
    )
    op.create_index(
        op.f("ix_input_snapshot_project_id"), "input_snapshot", ["project_id"], unique=False
    )
    op.create_index(op.f("ix_pr_closed_project_id"), "pr_closed", ["project_id"], unique=False)
    op.create_index(
        op.f("ix_golden_set_version_input_snapshot_id"),
        "golden_set_version",
        ["input_snapshot_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_golden_set_version_parent_id"), "golden_set_version", ["parent_id"], unique=False
    )
    op.create_index(op.f("ix_ingestion_snapshot_id"), "ingestion", ["snapshot_id"], unique=False)
    op.create_index(
        op.f("ix_source_file_snapshot_id"), "source_file", ["snapshot_id"], unique=False
    )
    op.create_index(op.f("ix_change_symbol"), "change", ["symbol"], unique=False)
    op.create_index(op.f("ix_chunk_section_id"), "chunk", ["section_id"], unique=False)
    op.create_index(op.f("ix_run_baseline_run_id"), "run", ["baseline_run_id"], unique=False)
    op.create_index(
        op.f("ix_run_golden_set_version_id"), "run", ["golden_set_version_id"], unique=False
    )
    op.create_index(op.f("ix_run_ingestion_id"), "run", ["ingestion_id"], unique=False)
    op.create_index(
        "ix_run_project_id_created_at", "run", ["project_id", "created_at"], unique=False
    )
    op.create_index(op.f("ix_claim_chunk_id"), "claim", ["chunk_id"], unique=False)
    op.create_index(op.f("ix_example_chunk_id"), "example", ["chunk_id"], unique=False)
    op.create_index(
        op.f("ix_extraction_issue_run_id"), "extraction_issue", ["run_id"], unique=False
    )
    op.create_index("ix_finding_key", "finding", ["key"], unique=False)
    op.create_index(op.f("ix_run_log_run_id"), "run_log", ["run_id"], unique=False)
    op.create_index(
        op.f("ix_test_item_input_snapshot_id"), "test_item", ["input_snapshot_id"], unique=False
    )
    op.create_index(
        op.f("ix_test_item_origin_run_id"), "test_item", ["origin_run_id"], unique=False
    )
    op.create_index(op.f("ix_test_item_symbol_path"), "test_item", ["symbol_path"], unique=False)
    op.create_index(
        op.f("ix_golden_set_item_test_item_id"), "golden_set_item", ["test_item_id"], unique=False
    )
    op.create_index(op.f("ix_llm_call_prompt_hash"), "llm_call", ["prompt_hash"], unique=False)
    op.create_index(op.f("ix_llm_call_run_id"), "llm_call", ["run_id"], unique=False)
    op.create_index(op.f("ix_llm_call_test_item_id"), "llm_call", ["test_item_id"], unique=False)
    op.create_index("ix_parameter_name", "parameter", ["name"], unique=False)
    op.create_index(
        op.f("ix_review_decision_test_item_id"), "review_decision", ["test_item_id"], unique=False
    )
    op.create_index(
        op.f("ix_run_test_item_test_item_id"), "run_test_item", ["test_item_id"], unique=False
    )
    op.create_index(
        op.f("ix_result_golden_set_version_id"), "result", ["golden_set_version_id"], unique=False
    )
    op.create_index(op.f("ix_result_llm_call_id"), "result", ["llm_call_id"], unique=False)
    op.create_index(op.f("ix_result_test_item_id"), "result", ["test_item_id"], unique=False)
    _append_only()
    _grants()


def _append_only() -> None:
    """SPEC §10: these rows are never updated or deleted, by any role, the owner included."""
    op.execute(
        """
        CREATE FUNCTION notinspec_append_only() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
            RAISE EXCEPTION '% on %: the table is append-only (SPEC §10)', TG_OP, TG_TABLE_NAME
                USING ERRCODE = 'insufficient_privilege';
        END
        $$
        """
    )
    for table in APPEND_ONLY:
        op.execute(
            f"CREATE TRIGGER append_only BEFORE UPDATE OR DELETE ON {table} "
            "FOR EACH ROW EXECUTE FUNCTION notinspec_append_only()"
        )
        op.execute(
            f"CREATE TRIGGER append_only_truncate BEFORE TRUNCATE ON {table} "
            "FOR EACH STATEMENT EXECUTE FUNCTION notinspec_append_only()"
        )


def _grants() -> None:
    """The application role reads and inserts everywhere, and changes only mutable tables.

    The role is created by deploy (with its password from env), so it may not exist yet, e.g.
    on a developer's database: then this does nothing, and deploy grants after creating it.
    """
    mutable = ", ".join(sorted(t for t in _TABLES if t not in APPEND_ONLY))
    every = ", ".join(sorted(_TABLES))
    op.execute(
        f"""
        DO $$
        BEGIN
            IF EXISTS (SELECT FROM pg_roles WHERE rolname = '{APP_ROLE}') THEN
                GRANT SELECT, INSERT ON {every} TO {APP_ROLE};
                GRANT UPDATE, DELETE ON {mutable} TO {APP_ROLE};
                EXECUTE format(
                    'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA %I TO %I',
                    current_schema(), '{APP_ROLE}'
                );
            END IF;
        END
        $$
        """
    )


_TABLES = (
    "claim_answer",
    "project",
    "input_snapshot",
    "pr_closed",
    "golden_set_version",
    "ingestion",
    "source_file",
    "change",
    "chunk",
    "golden_set_commit",
    "run",
    "symbol",
    "claim",
    "example",
    "extraction_issue",
    "finding",
    "run_artifact",
    "run_log",
    "run_step",
    "signature",
    "test_item",
    "upload",
    "example_calls",
    "golden_set_item",
    "llm_call",
    "parameter",
    "review_decision",
    "run_test_item",
    "result",
)


def downgrade() -> None:
    op.drop_table("result")
    op.drop_table("run_test_item")
    op.drop_table("review_decision")
    op.drop_table("parameter")
    op.drop_table("llm_call")
    op.drop_table("golden_set_item")
    op.drop_table("example_calls")
    op.drop_table("upload")
    op.drop_table("test_item")
    op.drop_table("signature")
    op.drop_table("run_step")
    op.drop_table("run_log")
    op.drop_table("run_artifact")
    op.drop_table("finding")
    op.drop_table("extraction_issue")
    op.drop_table("example")
    op.drop_table("claim")
    op.drop_table("symbol")
    op.drop_table("run")
    op.drop_table("golden_set_commit")
    op.drop_table("chunk")
    op.drop_table("change")
    op.drop_table("source_file")
    op.drop_table("ingestion")
    op.drop_table("golden_set_version")
    op.drop_table("pr_closed")
    op.drop_table("input_snapshot")
    op.drop_table("project")
    op.drop_table("claim_answer")
    op.execute("DROP FUNCTION notinspec_append_only()")
