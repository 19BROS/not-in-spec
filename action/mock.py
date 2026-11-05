"""Mock of `notinspec ci` (SPEC §11): same inputs, outputs and exit codes, fake numbers.

Lets the Action, the image and the server be built before `core` can evaluate anything.
Replace with the real CLI from `core` once it exists; the interface stays.

    python mock.py ci --config notinspec.yaml --out notinspec-out

Writes results.json (schema v0), report.html and comment.md. Exit 0 = pass, 1 = fail,
2 = bad config or crash. Numbers come from a hash of the docs, so the same docs give the same
results. A changed file containing FAIL_MARKER makes L3 drop, to demo a red PR.
"""

import argparse
import hashlib
import html
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

SCHEMA_VERSION = 0
TOOL_VERSION = "0.0.0-mock"
FAIL_MARKER = "<!-- notinspec-mock: fail -->"
COMMENT_MARKER = "<!-- notinspec -->"  # the Action finds its own PR comment by this
ITEMS_PER_ROW = 10
MODES = ("none", "gold")


class ConfigError(Exception):
    pass


def load_config(path: Path) -> dict[str, Any]:
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigError(f"cannot read {path}: {exc}") from exc
    docs = config.get("docs") if isinstance(config, dict) else None
    paths = docs.get("paths") if isinstance(docs, dict) else None
    if not isinstance(paths, list) or not all(isinstance(p, str) for p in paths):
        raise ConfigError(f"{path}: docs.paths must be a list of glob patterns")
    return config


def doc_files(root: Path, config: dict[str, Any]) -> list[Path]:
    """Files the config points at, never outside `root` (a pattern like `../*` is ignored)."""
    root = root.resolve()
    docs = config["docs"]
    candidates = [p for pattern in docs["paths"] for p in root.glob(pattern)]
    candidates += [root / docs[key] for key in ("openapi", "changelog") if docs.get(key)]
    return sorted(
        {p.resolve() for p in candidates if p.is_file() and p.resolve().is_relative_to(root)}
    )


def changed_files(root: Path, files: list[Path]) -> tuple[list[Path], str]:
    """Docs files changed vs. the PR base (or the previous commit on push).

    Falls back to "all changed" when git can't tell (shallow clone, no repo).
    """
    base = os.environ.get("GITHUB_BASE_REF")
    diff_range = f"origin/{base}...HEAD" if base else "HEAD^...HEAD"
    # the workspace is mounted from the runner, owned by another uid than the container
    git = ["git", "-c", "safe.directory=*", "-C", str(root)]
    try:
        top = Path(_run([*git, "rev-parse", "--show-toplevel"]).strip()).resolve()
        names = _run([*git, "diff", "--name-only", diff_range]).splitlines()
    except (OSError, subprocess.CalledProcessError):
        return files, "git diff unavailable, treating all docs as changed"
    changed = {(top / n).resolve() for n in names}
    return [f for f in files if f in changed], f"git diff {diff_range}"


def _run(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def build_results(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    root = root.resolve()
    files = doc_files(root, config)
    changed, diff_note = changed_files(root, files)
    failing = [f for f in changed if FAIL_MARKER in f.read_text(encoding="utf-8", errors="replace")]

    digest = hashlib.sha256()
    for f in files:
        digest.update(f.relative_to(root).as_posix().encode() + b"\0" + f.read_bytes())
    seed = digest.hexdigest()

    levels = ["L0", "L1", "L3"] + (["L4"] if config["docs"].get("openapi") else [])
    models = config.get("models", {}).get("pr") or ["mock-small"]
    rows = []
    for level in levels:
        for model in models:
            for mode in MODES:
                h = int(hashlib.sha256(f"{seed}/{level}/{model}/{mode}".encode()).hexdigest(), 16)
                baseline = 5 + h % (ITEMS_PER_ROW - 4)  # 5..10 of 10
                drop = 4 if failing and level == "L3" else 0
                rows.append(
                    {
                        "level": level,
                        "model": model,
                        "mode": mode,
                        "items": ITEMS_PER_ROW,
                        "passed": max(baseline - drop, 0),
                        "baseline_passed": baseline,
                    }
                )

    rel = [f.relative_to(root).as_posix() for f in failing]
    findings = [
        {"check": "K4", "file": r, "message": "example uses a removed parameter (mock)"}
        for r in rel
    ]
    reasons = [f"L3 dropped in {r} (mock)" for r in rel]
    commit = os.environ.get("NOTINSPEC_COMMIT") or _git_head(root)
    pr = os.environ.get("NOTINSPEC_PR")
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "notinspec", "version": TOOL_VERSION},
        "repo": os.environ.get("GITHUB_REPOSITORY", "local/local"),
        "commit": commit,
        "ref": os.environ.get("GITHUB_REF", ""),
        "event": os.environ.get("GITHUB_EVENT_NAME", "local"),
        "pr": int(pr) if pr else None,
        "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "docs": {
            "files": [f.relative_to(root).as_posix() for f in files],
            "changed": [f.relative_to(root).as_posix() for f in changed],
            "diff": diff_note,
        },
        # one row per level × model × mode; never averaged into one score (SPEC §1.1)
        "results": rows,
        "findings": findings,
        "verdict": "fail" if reasons else "pass",
        "reasons": reasons,
    }


def _git_head(root: Path) -> str:
    try:
        return _run(["git", "-c", "safe.directory=*", "-C", str(root), "rev-parse", "HEAD"]).strip()
    except (OSError, subprocess.CalledProcessError):
        return "0" * 40


def render_comment(results: dict[str, Any]) -> str:
    icon = "✓" if results["verdict"] == "pass" else "✗"
    changed = results["docs"]["changed"]
    lines = [
        COMMENT_MARKER,
        f"**NOT-IN-SPEC** {icon} {results['verdict']} · {len(changed)} changed docs files · "
        f"`{TOOL_VERSION}` (mock results)",
        "",
        "| Level | Model | Mode | Passed | main |",
        "|---|---|---|---|---|",
    ]
    for r in results["results"]:
        lines.append(
            f"| {r['level']} | {r['model']} | {r['mode']} | "
            f"{r['passed']}/{r['items']} | {r['baseline_passed']}/{r['items']} |"
        )
    lines += [""] + [f"- ✗ {reason}" for reason in results["reasons"]]
    lines += [f"- finding {f['check']}: `{f['file']}` {f['message']}" for f in results["findings"]]
    return "\n".join(lines).rstrip() + "\n"


def render_report(results: dict[str, Any]) -> str:
    e = html.escape
    rows = "".join(
        f"<tr><td>{e(r['level'])}</td><td>{e(r['model'])}</td><td>{e(r['mode'])}</td>"
        f"<td>{r['passed']}/{r['items']}</td><td>{r['baseline_passed']}/{r['items']}</td></tr>"
        for r in results["results"]
    )
    reasons = "".join(f"<li>{e(x)}</li>" for x in results["reasons"])
    return (
        "<!doctype html><meta charset=utf-8><title>NOT-IN-SPEC report</title>"
        f"<h1>NOT-IN-SPEC: {e(results['verdict'])}</h1>"
        f"<p>{e(results['repo'])} @ {e(results['commit'][:12])} · mock results</p>"
        "<table border=1><tr><th>Level<th>Model<th>Mode<th>Passed<th>main</tr>"
        f"{rows}</table><ul>{reasons}</ul>\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="notinspec")
    sub = parser.add_subparsers(dest="command", required=True)
    ci = sub.add_parser("ci", help="evaluate changed docs, write results (mock)")
    ci.add_argument("--config", type=Path, default=Path("notinspec.yaml"))
    ci.add_argument("--out", type=Path, default=Path("notinspec-out"))
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
        results = build_results(args.config.parent, config)
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "results.json").write_text(json.dumps(results, indent=2) + "\n", "utf-8")
        (args.out / "comment.md").write_text(render_comment(results), encoding="utf-8")
        (args.out / "report.html").write_text(render_report(results), encoding="utf-8")
    # an uncaught exception exits 1, which means "docs got worse"; a crash must never look like that
    except Exception as exc:
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(render_comment(results))
    return 0 if results["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
