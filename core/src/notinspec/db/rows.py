"""Pipeline output → table rows. Pure: no session, no I/O, so it is tested without a database.

Every function takes the JSON shape of a dataclass (what `canonical_json` writes into
ingestion.json, claims.json and llm-calls.jsonl), so a dataclass from the pipeline and a run
folder written before the DB existed go through the same code. `plain()` turns a dataclass into
that shape.
"""

import json
from collections.abc import Mapping
from dataclasses import asdict
from datetime import datetime
from typing import Any

from notinspec.adapters.canonical import canonical_json, content_hash
from notinspec.db import models
from notinspec.tasks import TestItem, loads
from notinspec.tasks.serialization import SCHEMA_VERSION as TASK_SCHEMA_VERSION

type Doc = Mapping[str, Any]


def plain(obj: Any) -> Any:
    """A dataclass (or anything canonical_json takes) as plain JSON: dicts, lists, scalars."""
    return json.loads(canonical_json(obj))


def ingestion_versions(ingestion: Doc) -> dict[str, Any]:
    """What chunks and the inventory depend on besides the inputs and the config."""
    sphinx = ingestion.get("sphinx")
    return {
        "schema_version": ingestion.get("schema_version"),
        "chunker_version": ingestion.get("chunker_version"),
        "soft_limit": ingestion.get("soft_limit"),
        "sphinx_reader_version": sphinx.get("reader_version") if sphinx else None,
        "sphinx_version": sphinx.get("version") if sphinx else None,
        "inventory_builder_version": ingestion.get("inventory_builder_version"),
    }


def versions_hash(versions: Doc) -> str:
    return content_hash(dict(versions))


def source_file(f: Doc, snapshot_id: int) -> models.SourceFile:
    return models.SourceFile(
        snapshot_id=snapshot_id, path=f["source"], kind=f["kind"], content_hash=f["content_hash"]
    )


def chunk(c: Doc, ingestion_id: int) -> models.Chunk:
    return models.Chunk(
        ingestion_id=ingestion_id,
        chunk_key=c["id"],
        section_id=c["section_id"],
        content_hash=c["content_hash"],
        source=c["source"],
        heading_path=list(c["heading_path"]),
        breadcrumb=c["breadcrumb"],
        heading_level=c["heading_level"],
        occurrence=c["occurrence"],
        part=c["part"],
        parts=c["parts"],
        start_line=c["start_line"],
        end_line=c["end_line"],
        tokens=c["tokens"],
        oversized=c["oversized"],
        text=c["text"],
        blocks=list(c["blocks"]),
    )


def example(e: Doc, ingestion_id: int, chunk_id: int) -> models.Example:
    return models.Example(
        ingestion_id=ingestion_id,
        chunk_id=chunk_id,
        example_key=e["id"],
        section_id=e["section_id"],
        position=e["position"],
        content_hash=e["content_hash"],
        lang=e["lang"],
        code=e["code"],
        start_line=e["start_line"],
        end_line=e["end_line"],
        nested=e["nested"],
    )


def symbol(s: Doc, ingestion_id: int) -> models.Symbol:
    return models.Symbol(
        ingestion_id=ingestion_id, path=s["path"], kind=s["kind"], sources=list(s["sources"])
    )


def signature(sig: Doc, symbol_id: int, position: int) -> models.Signature:
    return models.Signature(
        symbol_id=symbol_id,
        position=position,
        text=sig.get("text"),
        returns=sig.get("returns"),
        sources=list(sig.get("sources", [])),
    )


def parameter(p: Doc, signature_id: int, position: int) -> models.Parameter:
    return models.Parameter(
        signature_id=signature_id,
        position=position,
        name=p["name"],
        kind=p["kind"],
        required=p["required"],
        type=p.get("type"),
        default=p.get("default"),
        location=p.get("location"),
        constraints=list(p.get("constraints", [])),
        sources=list(p.get("sources", [])),
    )


def change(c: Doc, ingestion_id: int, position: int) -> models.Change:
    return models.Change(
        ingestion_id=ingestion_id,
        position=position,
        symbol=c["symbol"],
        kind=c["kind"],
        version=c["version"],
        parameter=c.get("parameter"),
        replacement=c.get("replacement"),
        removal_planned=c.get("removal_planned"),
        sources=list(c.get("sources", [])),
    )


def _span(value: Any) -> tuple[int | None, int | None]:
    return (value[0], value[1]) if value else (None, None)


def claim(g: Doc, run_id: int, chunk_id: int, versions: Doc) -> models.Claim:
    """One entry of claims.json (`GroundedClaim`)."""
    c = g["claim"]
    citation_start, citation_end = _span(g.get("citation_span"))
    premise_start, premise_end = _span(g.get("premise_span"))
    return models.Claim(
        run_id=run_id,
        chunk_id=chunk_id,
        extractor=c["extractor"],
        local_id=c["local_id"],
        text=c["text"],
        citation=c["citation"],
        type=c["type"],
        prompt_version=g["prompt_version"],
        prompt_hash=c["prompt_hash"],
        model=c["model"],
        extraction_run=c["run_id"],
        status=g["status"],
        citation_start=citation_start,
        citation_end=citation_end,
        citation_matches=g["citation_matches"],
        premise_candidates=g["premise_candidates"],
        premise=g.get("premise"),
        premise_start=premise_start,
        premise_end=premise_end,
        nli=g.get("nli"),
        missing=list(g.get("missing", [])),
        versions=dict(versions),
    )


def extraction_failure(f: Doc, run_id: int) -> models.ExtractionIssue:
    return models.ExtractionIssue(
        run_id=run_id,
        chunk_key=f["chunk_id"],
        extractor=f["extractor"],
        kind="failure",
        cause=f["cause"],
        detail=f["detail"],
    )


def extraction_problem(p: Doc, run_id: int) -> models.ExtractionIssue:
    return models.ExtractionIssue(
        run_id=run_id,
        chunk_key=p["chunk_id"],
        extractor=p["extractor"],
        kind="problem",
        cause=None,
        detail=p["detail"],
    )


def _usage(response: Doc | None, field: str) -> int | None:
    usage = response.get("usage") if response else None
    value = usage.get(field) if isinstance(usage, Mapping) else None
    return value if isinstance(value, int) else None


def llm_call(call: Doc, run_id: int | None) -> models.LlmCall:
    """One `claims.store.LlmCall` (a line of llm-calls.jsonl)."""
    response = call.get("response")
    answered = response.get("model") if response else None
    return models.LlmCall(
        run_id=run_id,
        run_ref=call["run_id"],
        role=call["role"],
        actor=call.get("extractor"),
        chunk_key=call.get("chunk_id"),
        model=call["model"],
        answered_model=answered if isinstance(answered, str) else None,
        prompt_hash=call["prompt_hash"],
        request=dict(call["request"]),
        response=response,
        error=call.get("error"),
        tokens_in=_usage(response, "prompt_tokens"),
        tokens_out=_usage(response, "completion_tokens"),
        created_at=datetime.fromisoformat(call["time"]),
    )


def claim_answer(key: Doc, answer: Doc) -> models.ClaimAnswer:
    """One claim store entry (`ReuseKey`, `StoredAnswer`)."""
    return models.ClaimAnswer(
        content_hash=key["content_hash"],
        breadcrumb=key["breadcrumb"],
        extractor=key["extractor"],
        model=key["model"],
        prompt_version=key["prompt_version"],
        reasoning_effort=key.get("reasoning_effort"),
        parser_version=key.get("parser_version"),
        thinking=key.get("thinking"),
        claims=list(answer["claims"]),
        problems=list(answer["problems"]),
        run_ref=answer["run_id"],
        prompt_hash=answer["prompt_hash"],
        answered_model=answer["model"],
    )


def finding(f: Doc, run_id: int) -> models.Finding:
    """One `findings.Finding`; its `versions` pairs become an object."""
    return models.Finding(
        run_id=run_id,
        key=f["key"],
        check_code=f["check"],
        kind=f["kind"],
        subject=f["subject"],
        message=f["message"],
        confidence=f["confidence"],
        evidence=list(f["evidence"]),
        nli=list(f.get("nli", [])),
        versions={name: value for name, value in f.get("versions", [])},
    )


def item_doc(item: TestItem) -> dict[str, Any]:
    """A `tasks.TestItem` as the task export writes it: every field plus its `id`.

    Not `plain()`: canonical_json leaves out the references' `kind` tag (an init=False field).
    """
    return {**plain(asdict(item)), "id": item.id}


def test_item(
    item: Doc, *, project_id: int, input_snapshot_id: int, origin_run_id: int | None = None
) -> models.TestItem:
    """One test item (`item_doc` shape). Its `status` is not stored: the latest review decision
    is (SPEC §10), and an item without one is a candidate."""
    return models.TestItem(
        project_id=project_id,
        identity_key=item["id"],
        level=item["level"],
        operator=item["operator"],
        operator_version=item["operator_version"],
        format=item["format"],
        difficulty=item["difficulty"],
        question_kind=item["question_kind"],
        chunk_key=item["chunk_id"],
        chunk_keys=list(item["chunk_ids"]),
        source_example_key=item["source_example_id"],
        symbol_path=item["reference"]["subject"]["symbol"],
        reference=dict(item["reference"]),
        wording=dict(item["wording"]),
        sources=list(item["sources"]),
        generator_version=item["generator_version"],
        input_snapshot_id=input_snapshot_id,
        docs_version=item["docs_version"],
        origin_run_id=origin_run_id,
    )


def item_from_row(row: models.TestItem, *, project: str, input_hash: str) -> TestItem:
    """A stored row back as a `tasks.TestItem`; the task export's loader checks its identity.

    Every item comes back as a candidate: the dataclass knows no other status, and the real
    state is the latest review decision.
    """
    doc = {
        "id": row.identity_key,
        "project": project,
        "chunk_id": row.chunk_key,
        "chunk_ids": row.chunk_keys,
        "level": row.level,
        "question_kind": row.question_kind,
        "reference": row.reference,
        "sources": row.sources,
        "wording": row.wording,
        "input_snapshot_hash": input_hash,
        "docs_version": row.docs_version,
        "generator_version": row.generator_version,
        "operator_version": row.operator_version,
        "operator": row.operator,
        "format": row.format,
        "difficulty": row.difficulty,
        "source_example_id": row.source_example_key,
        "status": "candidate",
    }
    export = {"schema_version": TASK_SCHEMA_VERSION, "items": [doc], "skipped": []}
    (item,) = loads(canonical_json(export)).items
    return item
