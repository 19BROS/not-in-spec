"""Demo run (docs/plans/demo-cli-web.md): ingestion + claims artifacts -> one run.json for the web.

shortcut: runs are folders on disk (`tmp/runs/<id>/run.json`) instead of Postgres, because the
DB models are still open (SPEC §18). The web shows counts only: never an averaged level or one
overall score.
"""

import secrets
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

SCHEMA = "notinspec-demo-run"
SCHEMA_VERSION = 0

_NEXT = "next iteration"


def new_run_id(project: str, now: datetime | None = None) -> str:
    """`YYYYmmddTHHMMZ-<project>-<4 hex>`; the hex keeps two runs in the same minute apart."""
    stamp = (now or datetime.now(UTC)).strftime("%Y%m%dT%H%MZ")
    # the API takes [A-Za-z0-9_.-]{1,100} only: ASCII, and the name cut so the ID stays short
    allowed = (ch if (ch.isascii() and ch.isalnum()) or ch in "_.-" else "-" for ch in project)
    name = "".join(allowed)[:60] or "project"
    return f"{stamp}-{name}-{secrets.token_hex(2)}"


def _step(step_id: str, label: str, status: str, detail: str) -> dict[str, str]:
    return {"id": step_id, "label": label, "status": status, "detail": detail}


def _symbol_source(symbol: dict[str, Any], section_source: dict[str, str]) -> str | None:
    sources = symbol["sources"]
    return section_source.get(sources[0]["section_id"]) if sources else None


def build_demo_run(
    ingestion: dict[str, Any],
    results: dict[str, Any],
    claims: dict[str, Any] | None,
    run_id: str,
    *,
    stopped: Sequence[str] = (),
) -> dict[str, Any]:
    """run.json v0 from ingestion.json, results.json and claims.json (None: claims not run).

    `stopped`: `<extractor>: <reason>` for each extractor whose run stopped (quota, model gone,
    timeout), which claims.json does not record; it makes step `claims` `failed`.
    """
    inventory = ingestion["inventory"]
    symbols: list[dict[str, Any]] = inventory["symbols"]
    changes: list[dict[str, Any]] = inventory["changes"]
    chunks = {c["id"]: c for c in ingestion["chunks"]}
    section_source = {c["section_id"]: c["source"] for c in ingestion["chunks"]}

    documents: dict[str, dict[str, Any]] = {}
    for c in ingestion["chunks"]:
        doc = documents.setdefault(
            c["source"],
            {"source": c["source"], "chunks": 0, "tokens": 0, "symbols": 0,
             "claims": 0, "claims_kept": 0},
        )  # fmt: skip
        doc["chunks"] += 1
        doc["tokens"] += c["tokens"]
    for s in symbols:
        source = _symbol_source(s, section_source)
        if source in documents:
            documents[source]["symbols"] += 1

    n_files, n_chunks = len(ingestion["files"]), len(ingestion["chunks"])
    steps = [
        _step("read", "Read & chunk", "done", f"{n_files} files · {n_chunks} chunks"),
        _step(
            "inventory",
            "Build inventory",
            "done",
            f"{len(symbols)} symbols · {len(changes)} changes",
        ),  # fmt: skip
    ]
    claims_out: dict[str, Any] | None = None
    n_claims: int | None = None
    n_kept: int | None = None
    if claims is None:
        steps += [
            _step("claims", "Extract claims", "skipped", "not run (--no-claims)"),
            _step(
                "grounding",
                "Ground claims (citation, NLI, identifiers)",
                "skipped",
                "no claims",
            ),  # fmt: skip
        ]
    else:
        items = []
        for grounded in claims["claims"]:
            claim = grounded["claim"]
            chunk = chunks.get(claim["chunk_id"], {})
            source = chunk.get("source")
            kept = grounded["status"] == "kept"
            if source in documents:
                documents[source]["claims"] += 1
                documents[source]["claims_kept"] += kept
            items.append(
                {
                    "id": f"{claim['chunk_id']}:{claim['extractor']}:{claim['local_id']}",
                    "extractor": claim["extractor"],
                    "source": source,
                    "breadcrumb": chunk.get("breadcrumb"),
                    "chunk_id": claim["chunk_id"],
                    "type": claim["type"],
                    "text": claim["text"],
                    "citation": claim["citation"],
                    "status": grounded["status"],
                    "premise": grounded.get("premise"),
                    "nli": grounded.get("nli"),
                    "missing": grounded.get("missing", []),
                }
            )
        n_claims = len(items)
        n_kept = sum(1 for x in items if x["status"] == "kept")
        failed = len(claims.get("failures", []))
        detail = (
            f"{n_claims} claims · {len(claims['extractors'])} extractors · "
            f"{len(claims['sources'])} pages"
        )
        if failed:
            detail += f" · {failed} chunks failed"
        if stopped:  # e.g. no quota left: the claims so far are kept, but the step did not finish
            detail = f"stopped: {'; '.join(stopped)}; run again to continue"
        steps += [
            _step("claims", "Extract claims", "failed" if stopped else "done", detail),
            _step(
                "grounding",
                "Ground claims (citation, NLI, identifiers)",
                "done",
                f"{n_kept} kept · {n_claims - n_kept} dropped",
            ),  # fmt: skip
        ]
        claims_out = {
            "sources": claims["sources"],
            "extractors": [e["name"] for e in claims["extractors"]],
            "counts": claims["counts"],
            "versions": claims["versions"],
            "items": items,
        }
    steps += [
        _step("tests", "Generate tests (L0-L4)", "not_implemented", _NEXT),
        _step("models", "Run models", "not_implemented", _NEXT),
        _step("evaluate", "Evaluate & report", "not_implemented", _NEXT),
    ]

    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "id": run_id,
        "project": ingestion["project"],
        "created_at": results["created_at"],
        "commit": results.get("commit", ""),
        "tool_version": results["tool"]["version"],
        "docs": {
            "sphinx_version": (ingestion.get("sphinx") or {}).get("version"),
            "input_hash": ingestion["input_hash"],
            "config_hash": ingestion["config_hash"],
        },
        "counts": {
            "files": n_files,
            "chunks": n_chunks,
            "symbols": len(symbols),
            "parameters": sum(len(sig["parameters"]) for s in symbols for sig in s["signatures"]),
            "changes": len(changes),
            "warnings": len(ingestion["warnings"]),
            "claims": n_claims,
            "claims_kept": n_kept,
        },
        "steps": steps,
        "documents": list(documents.values()),
        "symbols": [
            {
                "path": s["path"],
                "kind": s["kind"],
                "source": _symbol_source(s, section_source),
                "parameters": [p["name"] for sig in s["signatures"] for p in sig["parameters"]],
            }
            for s in symbols
        ],
        "changes": [
            {
                "symbol": c["symbol"],
                "kind": c["kind"],
                "version": c["version"],
                "parameter": c["parameter"],
                "replacement": c["replacement"],
            }
            for c in changes
        ],
        "warnings": ingestion["warnings"],
        "claims": claims_out,
    }
