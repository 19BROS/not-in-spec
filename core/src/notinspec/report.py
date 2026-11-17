"""Ingestion artifacts using the Action's filenames, with no invented model scores.

results.json keeps the mock server's v0 envelope, extended by stage and ingestion metadata.
The not-evaluated verdict is a prototype extension, not a passing LLM evaluation.
"""

import html
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from notinspec import __version__
from notinspec.adapters.canonical import canonical_json
from notinspec.chunking import Chunk
from notinspec.ingestion import Ingestion

COMMENT_MARKER = "<!-- notinspec -->"
NOT_EVALUATED = "LLM evaluation has not run. No L0-L4 scores or regression verdict are available."


def build_results(ingestion: Ingestion, root: Path) -> dict[str, Any]:
    commit = os.environ.get("NOTINSPEC_COMMIT") or _git_head(root)
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("NOTINSPEC_COMMIT must be a 40-character lowercase commit SHA")
    return {
        "schema_version": 0,
        "tool": {"name": "notinspec", "version": __version__},
        "repo": os.environ.get("GITHUB_REPOSITORY", "local/local"),
        "commit": commit,
        "ref": os.environ.get("GITHUB_REF", ""),
        "event": os.environ.get("GITHUB_EVENT_NAME", "local"),
        "pr": int(os.environ["NOTINSPEC_PR"]) if os.environ.get("NOTINSPEC_PR") else None,
        "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "stage": "ingestion",
        "docs": {
            "project": ingestion.project,
            "files": [f.source for f in ingestion.files],
            "input_hash": ingestion.input_hash,
            "config_hash": ingestion.config_hash,
        },
        "ingestion": {
            "artifact": "ingestion.json",
            "files": len(ingestion.files),
            "chunks": len(ingestion.chunks),
            "sections": len({c.section_id for c in ingestion.chunks}),
            "operations": sum(len(i.spec.operations) for i in ingestion.openapi),
            "warnings": list(ingestion.warnings),
        },
        "results": [],
        "findings": [],
        "verdict": "not-evaluated",
        "reasons": [NOT_EVALUATED],
    }


def write_artifacts(output: Path, ingestion: Ingestion, results: dict[str, Any]) -> None:
    artifacts = {
        "ingestion.json": canonical_json(ingestion, pretty=True),
        "results.json": canonical_json(results, pretty=True),
        "comment.md": render_comment(results).encode("utf-8"),
        "report.html": render_report(ingestion).encode("utf-8"),
    }
    output.mkdir(parents=True, exist_ok=True)
    for name in artifacts:
        path = output / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f"output artifact must be a regular file: {path}")
    _publish(output, artifacts)


def _publish(output: Path, artifacts: dict[str, bytes]) -> None:
    """Stage every artifact before replacing any old one; roll back publication failures.

    Only our named artifacts are replaced; unrelated files in output are preserved. This
    handles ordinary I/O errors, not process termination or simultaneous writers.
    """
    output = output.resolve()
    staging = Path(tempfile.mkdtemp(prefix=".notinspec-", dir=output)).resolve()
    if staging.parent != output:
        raise ValueError("artifact staging directory must be inside output")
    cleanup = True
    backups: list[str] = []
    published: list[str] = []
    try:
        for name, data in artifacts.items():
            (staging / name).write_bytes(data)
        try:
            for name in artifacts:
                target = output / name
                if target.exists():
                    target.replace(staging / f"previous-{name}")
                    backups.append(name)
            for name in artifacts:
                (staging / name).replace(output / name)
                published.append(name)
        except OSError as exc:
            errors: list[str] = []
            for name in reversed(published):
                try:
                    (output / name).unlink()
                except OSError as error:
                    errors.append(str(error))
            for name in reversed(backups):
                try:
                    (staging / f"previous-{name}").replace(output / name)
                except OSError as error:
                    errors.append(str(error))
            if errors:
                cleanup = False  # leave the backups available for recovery
                raise OSError(f"cannot restore all artifacts; backups kept in {staging}") from exc
            raise
    finally:
        if cleanup:
            shutil.rmtree(staging)


def render_comment(results: dict[str, Any]) -> str:
    counts = results["ingestion"]
    lines = [
        COMMENT_MARKER,
        "**NOT-IN-SPEC: ingestion completed; model evaluation not run.**",
        "",
        f"{counts['files']} files, {counts['sections']} sections, "
        f"{counts['chunks']} chunks, {counts['operations']} OpenAPI operations.",
        "",
        NOT_EVALUATED,
        "",
        "Details: `ingestion.json`. All configured inputs were processed (no incremental diff).",
    ]
    if counts["warnings"]:
        lines += ["", "Warnings:", *[f"- {w}" for w in counts["warnings"]]]
    return "\n".join(lines) + "\n"


_STYLE = (
    ":root{color-scheme:light dark;--fg:#1f2328;--bg:#fff;--muted:#59636e;--line:#d0d7de;"
    "--code:#f6f8fa;--note:#fff3cd;--bad:#b42318}"
    "@media (prefers-color-scheme:dark){:root{--fg:#e6edf3;--bg:#0d1117;--muted:#9198a1;"
    "--line:#3d444d;--code:#161b22;--note:#3b2e00;--bad:#ff7b72}}"
    "body{font:15px/1.45 system-ui,sans-serif;max-width:1100px;margin:2rem auto;"
    "padding:0 1rem;color:var(--fg);background:var(--bg)}"
    "aside{padding:.75rem 1rem;background:var(--note)}"
    "table{border-collapse:collapse;margin:.5rem 0}"
    "td,th{border:1px solid var(--line);padding:.2rem .5rem;text-align:left;vertical-align:top}"
    "td,li,summary{overflow-wrap:anywhere}"
    "h2{margin-top:2rem;border-bottom:2px solid var(--line)}"
    "details.chunk{border-bottom:1px solid var(--line);padding:.3rem 0}"
    "summary{cursor:pointer}.meta{color:var(--muted);font-size:13px}"
    ".over{color:var(--bad);font-weight:600}"
    "pre{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--code);padding:.75rem;"
    "font:13px/1.4 ui-monospace,Consolas,monospace}"
)


def render_report(ingestion: Ingestion) -> str:
    """Plain HTML for reviewing chunks by eye (SPEC §6.1).

    No scripts and no external files, so it opens from a CI artifact as is and stays
    usable for thousands of chunks; every input-derived string is HTML-escaped.
    """
    chunks = ingestion.chunks
    documents: dict[str, list[Chunk]] = {}
    for chunk in chunks:  # document order: the order of the chunks
        documents.setdefault(chunk.source, []).append(chunk)
    counts = {
        "files": len(ingestion.files),
        "documents with chunks": len(documents),
        "chunks": len(chunks),
        "sections": len({c.section_id for c in chunks}),
        "oversized chunks": sum(c.oversized for c in chunks),
        "OpenAPI operations": sum(len(i.spec.operations) for i in ingestion.openapi),
        "warnings": len(ingestion.warnings),
    }
    out = [
        "<!doctype html><html lang=en><meta charset=utf-8>",
        "<meta name=viewport content='width=device-width,initial-scale=1'>",
        f"<title>{_e(ingestion.project)} · NOT-IN-SPEC chunks</title><style>{_STYLE}</style>",
        f"<h1>{_e(ingestion.project)}: documentation chunks</h1>",
        f"<aside>{NOT_EVALUATED}</aside>",
        "<table>",
        *(f"<tr><th>{name}<td>{value}" for name, value in counts.items()),
        f"<tr><th>input hash<td><code>{_e(ingestion.input_hash)}</code>",
        f"<tr><th>chunker<td>v{ingestion.chunker_version}, soft limit {ingestion.soft_limit}",
        *(
            [
                f"<tr><th>Sphinx<td>{_e(ingestion.sphinx.version)} "
                f"(reader v{ingestion.sphinx.reader_version})"
            ]
            if ingestion.sphinx
            else []
        ),
        "</table>",
        "<p>Full data: <a href=ingestion.json>ingestion.json</a>.</p>",
        *_warnings(ingestion.warnings),
        "<h2>Documents</h2><ol>",
        *(
            f"<li><a href='#d{n}'>{_e(source)}</a> <span class=meta>{len(items)} chunks</span>"
            for n, (source, items) in enumerate(documents.items(), 1)
        ),
        "</ol>" if documents else "</ol><p>No chunks.</p>",
        f"<details><summary>Input files ({len(ingestion.files)})</summary><ul>",
        *(f"<li>{_e(f.source)} <span class=meta>{_e(f.kind)}</span>" for f in ingestion.files),
        "</ul></details>",
    ]
    for n, (source, items) in enumerate(documents.items(), 1):
        out.append(f"<h2 id=d{n}>{_e(source)}</h2>")
        out.extend(_chunk(chunk) for chunk in items)
    out.append("</html>\n")
    return "\n".join(out)


def _warnings(warnings: tuple[str, ...]) -> list[str]:
    """Reader warnings end in "(3x)"; `unknown node` ones go first: the reader missed content."""
    rows: list[tuple[bool, str, int]] = []
    for warning in warnings:
        match = re.fullmatch(r"(.*) \((\d+)x\)", warning)
        message, count = (match[1], int(match[2])) if match else (warning, 1)
        rows.append(("unknown node" not in message, message, count))
    if not rows:
        return ["<h2>Warnings</h2><p>None.</p>"]
    return [
        "<h2>Warnings</h2><table><tr><th>Warning<th>Count",
        *(f"<tr><td>{_e(message)}<td>{count}" for _, message, count in sorted(rows)),
        "</table>",
    ]


def _chunk(chunk: Chunk) -> str:
    kinds = Counter(block.kind for block in chunk.blocks)
    meta = [f"part {chunk.part}/{chunk.parts}", f"{chunk.tokens} tokens"]
    meta += [f"{kind} {n}" for kind, n in kinds.items()]
    oversized = " <span class=over>oversized</span>" if chunk.oversized else ""
    return (
        f"<details class=chunk id='c-{_e(chunk.id)}'><summary>{_e(chunk.breadcrumb)} "
        f"<span class=meta>{' · '.join(meta)}</span>{oversized}</summary>"
        f"<p class=meta>id {_e(chunk.id)} · section {_e(chunk.section_id)} · "
        f"lines {chunk.start_line}–{chunk.end_line}</p>"
        f"<pre>{_e(chunk.text)}</pre>{_fields(chunk)}</details>"
    )


def _fields(chunk: Chunk) -> str:
    """API reference entries as the reader typed them: check name / type / field by eye."""
    fields = [b for b in chunk.blocks if b.field is not None]
    if not fields:
        return ""
    rows = "".join(
        f"<tr><td>{_e(b.field or '')}<td>{_e(b.name or '')}<td>{_e(b.type or '')}<td>{b.kind}"
        for b in fields
    )
    return f"<table class=fields><tr><th>field<th>name<th>type<th>kind{rows}</table>"


def _e(text: str) -> str:
    return html.escape(text, quote=True)


def _git_head(root: Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "0" * 40
