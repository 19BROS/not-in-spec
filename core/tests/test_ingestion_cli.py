import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from notinspec.cli import main
from notinspec.report import render_report

EXAMPLE = Path(__file__).parents[1] / "examples" / "cli"


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    shutil.copytree(EXAMPLE, root)
    return root


def run(project: Path, output: Path, *args: str) -> int:
    return main(["ci", "--config", str(project / "notinspec.yaml"), "--out", str(output), *args])


def test_real_ingestion_from_another_working_directory(
    project: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    output = tmp_path / "artifacts"
    assert run(project, output) == 0
    assert {p.name for p in output.iterdir()} == {
        "ingestion.json",
        "results.json",
        "report.html",
        "comment.md",
    }
    data = json.loads((output / "ingestion.json").read_bytes())
    assert [f["source"] for f in data["files"]] == ["docs/guide.md", "openapi.yaml"]
    assert [c["heading_path"] for c in data["chunks"]] == [
        ["Items API"],
        ["Items API", "List items"],
        ["Items API", "Create an item"],
    ]
    operations = data["openapi"][0]["spec"]["operations"]
    assert [(o["method"], o["path"]) for o in operations] == [("GET", "/items"), ("POST", "/items")]
    assert operations[0]["parameters"][0]["name"] == "limit"
    assert operations[1]["body_fields"][0]["name"] == "name"
    assert operations[1]["body_fields"][0]["required"] is True
    assert data["warnings"] == []
    assert str(project) not in (output / "ingestion.json").read_text("utf-8")
    assert "2 OpenAPI operations" in capsys.readouterr().out


def test_no_fabricated_evaluation_results(project: Path, tmp_path: Path) -> None:
    output = tmp_path / "out"
    assert run(project, output) == 0
    result = json.loads((output / "results.json").read_bytes())
    assert result["schema_version"] == 0
    assert result["stage"] == "ingestion"
    assert result["verdict"] == "not-evaluated"
    assert result["results"] == []
    assert result["findings"] == []
    assert result["ingestion"]["chunks"] == 3
    assert result["ingestion"]["operations"] == 2
    assert (output / "comment.md").read_text("utf-8").startswith("<!-- notinspec -->")
    assert "LLM evaluation has not run" in (output / "report.html").read_text("utf-8")


def test_repeated_run_ignores_its_own_artifacts(project: Path) -> None:
    config = project / "notinspec.yaml"
    config.write_text('docs:\n  paths: ["**/*.md"]\n  openapi: openapi.yaml\n', "utf-8")
    output = project / "output"
    assert run(project, output) == 0
    first = (output / "ingestion.json").read_bytes()
    assert run(project, output) == 0
    assert (output / "ingestion.json").read_bytes() == first
    guide = project / "docs" / "guide.md"
    guide.write_text(guide.read_text("utf-8") + "\nExtra documentation.\n", "utf-8")
    assert run(project, output) == 0
    second = json.loads((output / "ingestion.json").read_bytes())
    assert second["input_hash"] != json.loads(first)["input_hash"]


def test_ingest_alias_and_changelog_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "notinspec.yaml").write_text("docs: {changelog: CHANGES.md}", "utf-8")
    (tmp_path / "CHANGES.md").write_text("# Changes\n\nA parameter was renamed.\n", "utf-8")
    assert main(["ingest"]) == 0
    data = json.loads((tmp_path / "notinspec-out" / "ingestion.json").read_bytes())
    assert len(data["chunks"]) == 1
    assert data["openapi"] == []


def test_overlapping_patterns_and_explicit_paths_are_deduplicated(
    project: Path, tmp_path: Path
) -> None:
    (project / "notinspec.yaml").write_text(
        'docs:\n  paths: ["docs/**/*.md", "./docs/guide.md", "./openapi.yaml"]\n'
        '  changelog: "./docs/guide.md"\n  openapi: "./openapi.yaml"\n',
        "utf-8",
    )
    output = tmp_path / "out"
    assert run(project, output) == 0
    data = json.loads((output / "ingestion.json").read_bytes())
    assert len(data["files"]) == 2
    assert len(data["chunks"]) == 3
    assert len(data["openapi"]) == 1


@pytest.mark.parametrize(
    "config, message",
    [
        ('docs: {paths: ["missing/**/*.md"]}', "no input files matched"),
        ("docs: {openapi: missing.yaml}", "input is not a file"),
        ("docs: {paths: [docs/guide.md], changelog: missing.md}", "input is not a file"),
        ("docs: {paths: [openapi.yaml]}", "unsupported text format"),
    ],
)
def test_bad_inputs_return_two_without_reports(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str], config: str, message: str
) -> None:
    (project / "notinspec.yaml").write_text(config, "utf-8")
    output = tmp_path / "out"
    assert run(project, output) == 2
    assert message in capsys.readouterr().err
    assert not output.exists()


def test_invalid_openapi_is_not_a_documentation_regression(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (project / "openapi.yaml").write_text("openapi: [", "utf-8")
    assert run(project, tmp_path / "out") == 2
    assert "cannot parse" in capsys.readouterr().err


def test_validation_problems_are_reported_not_hidden(project: Path, tmp_path: Path) -> None:
    (project / "openapi.yaml").write_text(
        "openapi: 3.0.3\ninfo: {title: Broken}\npaths: {}\n", "utf-8"
    )
    output = tmp_path / "out"
    assert run(project, output) == 0
    result = json.loads((output / "results.json").read_bytes())
    assert any("version" in warning for warning in result["ingestion"]["warnings"])
    assert result["verdict"] == "not-evaluated"


def test_nonmatching_pattern_warns_when_other_inputs_exist(project: Path, tmp_path: Path) -> None:
    (project / "notinspec.yaml").write_text(
        'docs: {paths: ["missing.md", "docs/**/*.md"]}', "utf-8"
    )
    output = tmp_path / "out"
    assert run(project, output) == 0
    data = json.loads((output / "ingestion.json").read_bytes())
    assert "missing.md" in data["warnings"][0]


def test_bad_utf8_is_visible(project: Path, tmp_path: Path) -> None:
    (project / "docs" / "guide.md").write_bytes(b"# Guide\n\nBad: \xff\n")
    output = tmp_path / "out"
    assert run(project, output) == 0
    data = json.loads((output / "ingestion.json").read_bytes())
    assert any("UTF-8" in w for w in data["warnings"])


def test_output_cannot_overwrite_the_input_root(
    project: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(project, project) == 2
    assert "output must not" in capsys.readouterr().err
    assert not (project / "comment.md").exists()


def test_bad_output_is_exit_two(project: Path, tmp_path: Path) -> None:
    output = tmp_path / "out"
    output.mkdir()
    (output / "results.json").mkdir()
    assert run(project, output) == 2
    assert not (output / "ingestion.json").exists()


def test_unexpected_crash_returns_two(
    project: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def broken(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("unexpected pipeline failure")

    monkeypatch.setattr("notinspec.cli.ingest", broken)
    assert run(project, tmp_path / "out") == 2
    assert "RuntimeError: unexpected pipeline failure" in capsys.readouterr().err


def test_html_report_escapes_input_names() -> None:
    report = render_report(
        {
            "ingestion": {
                "files": 1,
                "chunks": 0,
                "sections": 0,
                "operations": 0,
                "warnings": ["<script>bad()</script>"],
            },
            "docs": {"files": ["<img src=x>.md"]},
        }
    )
    assert "<script>" not in report
    assert "&lt;script&gt;" in report
    assert "<img" not in report


@pytest.mark.parametrize("command", ["ci", "chunk"])
def test_limits_must_be_positive(command: str) -> None:
    with pytest.raises(SystemExit) as exc:
        main([command, "--soft-limit", "0"])
    assert exc.value.code == 2


def test_dry_run_lists_inputs_without_parsing_or_writing(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # Dry-run checks selection, not the OpenAPI document's content.
    (project / "openapi.yaml").write_text("openapi: [", "utf-8")
    output = tmp_path / "out"
    assert run(project, output, "--dry-run") == 0
    text = capsys.readouterr().out
    assert "docs/guide.md" in text
    assert "openapi.yaml" in text
    assert "No documents parsed" in text
    assert not output.exists()


def test_dry_run_still_rejects_missing_inputs(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (project / "openapi.yaml").unlink()
    assert run(project, tmp_path / "out", "--dry-run") == 2
    assert "input is not a file" in capsys.readouterr().err


def test_write_failure_keeps_previous_artifacts(
    project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "out"
    assert run(project, output) == 0
    previous = {p.name: p.read_bytes() for p in output.iterdir()}
    guide = project / "docs" / "guide.md"
    guide.write_text(guide.read_text("utf-8") + "\n## New section\n\nNew content.\n", "utf-8")
    original_write = Path.write_bytes

    def disk_full(path: Path, data: bytes) -> int:
        if path.name == "report.html":
            raise OSError("disk full")
        return original_write(path, data)

    monkeypatch.setattr(Path, "write_bytes", disk_full)
    assert run(project, output) == 2
    assert {p.name: p.read_bytes() for p in output.iterdir()} == previous


@pytest.mark.parametrize("existing", [False, True])
def test_publish_failure_restores_artifacts_and_preserves_unrelated_files(
    project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, existing: bool
) -> None:
    output = tmp_path / "out"
    if existing:
        assert run(project, output) == 0
    else:
        output.mkdir()
    (output / "notes.txt").write_text("User's unrelated file", "utf-8")
    previous = {p.name: p.read_bytes() for p in output.iterdir()}
    guide = project / "docs" / "guide.md"
    guide.write_text("# Changed\n\nA new snapshot.\n", "utf-8")
    original_replace = Path.replace
    failed = False

    def fail_once(path: Path, target: Path) -> Path:
        nonlocal failed
        if not failed and path.name == "results.json" and target.parent == output:
            failed = True
            raise PermissionError("cannot publish results")
        return original_replace(path, target)

    monkeypatch.setattr(Path, "replace", fail_once)
    assert run(project, output) == 2
    assert failed
    assert {p.name: p.read_bytes() for p in output.iterdir()} == previous


def test_failed_rollback_keeps_backups_for_recovery(
    project: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output = tmp_path / "out"
    assert run(project, output) == 0
    old_results = (output / "results.json").read_bytes()
    original_replace = Path.replace

    def cannot_publish_or_restore_results(path: Path, target: Path) -> Path:
        if target == output / "results.json":
            raise PermissionError("results is locked")
        return original_replace(path, target)

    monkeypatch.setattr(Path, "replace", cannot_publish_or_restore_results)
    assert run(project, output) == 2
    assert "backups kept" in capsys.readouterr().err
    (backup_dir,) = output.glob(".notinspec-*")
    assert (backup_dir / "previous-results.json").read_bytes() == old_results


def test_dry_run_preserves_existing_output(project: Path, tmp_path: Path) -> None:
    output = tmp_path / "out"
    assert run(project, output) == 0
    previous = {p.name: p.read_bytes() for p in output.iterdir()}
    assert run(project, output, "--dry-run") == 0
    assert {p.name: p.read_bytes() for p in output.iterdir()} == previous


def test_dry_run_rejects_output_file(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    output = tmp_path / "out"
    output.write_text("Do not overwrite", "utf-8")
    assert run(project, output, "--dry-run") == 2
    assert "output must be a directory" in capsys.readouterr().err
    assert output.read_text("utf-8") == "Do not overwrite"
