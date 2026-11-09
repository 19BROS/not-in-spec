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
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from notinspec import __version__
from notinspec.adapters.canonical import canonical_json
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
        "report.html": render_report(results).encode("utf-8"),
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


def render_report(results: dict[str, Any]) -> str:
    counts = results["ingestion"]
    warnings = "".join(f"<li>{html.escape(w)}</li>" for w in counts["warnings"])
    files = "".join(f"<li>{html.escape(f)}</li>" for f in results["docs"]["files"])
    return (
        "<!doctype html><html lang=en><meta charset=utf-8>"
        "<title>NOT-IN-SPEC ingestion</title>"
        "<style>body{font:16px system-ui;max-width:800px;margin:3rem auto;padding:0 1rem}"
        "li{overflow-wrap:anywhere}aside{padding:1rem;background:#fff3cd}</style>"
        "<h1>Documentation ingestion completed</h1>"
        f"<aside>{NOT_EVALUATED}</aside>"
        f"<p>{counts['files']} files / {counts['sections']} sections / "
        f"{counts['chunks']} chunks / {counts['operations']} OpenAPI operations.</p>"
        f"<h2>Input files</h2><ul>{files}</ul>"
        f"<h2>Warnings</h2><ul>{warnings or '<li>None</li>'}</ul>"
        "<p>All configured inputs were processed. See <a href=ingestion.json>ingestion.json</a> "
        "for chunks and normalized OpenAPI data.</p></html>\n"
    )


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
