import json
from pathlib import Path

import pytest

from notinspec import __version__
from notinspec.cli import main


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_no_args_prints_help() -> None:
    assert main([]) == 0


def _run(capsys: pytest.CaptureFixture[str], *args: str) -> tuple[int, str]:
    root = Path(__file__).parent / "chunking" / "fixtures" / "guide"
    code = main(["chunk", str(root), *args])
    return code, capsys.readouterr().out


def test_chunk_summary(capsys: pytest.CaptureFixture[str]) -> None:
    code, out = _run(capsys)
    assert code == 0
    assert "1 files, 5 chunks from 5 sections (0 split into parts, 0 oversized)" in out
    assert "NLI windows: 5" in out


def test_chunk_list_and_small_limits(capsys: pytest.CaptureFixture[str]) -> None:
    code, out = _run(capsys, "--list", "--soft-limit", "150", "--window-tokens", "60")
    assert code == 0
    assert "timeouts.md > Timeouts and retries > Migrating from 1.x" in out
    assert " 1/2 " in out and " 2/2 " in out


def test_chunk_json(capsys: pytest.CaptureFixture[str]) -> None:
    code, out = _run(capsys, "--json", "--overlap-tokens", "0")
    data = json.loads(out)
    assert code == 0
    assert len(data["chunks"]) == 5
    assert set(data["windows"]) == {c["id"] for c in data["chunks"]}


def test_chunk_missing_root(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["chunk", "/nonexistent/docs"]) == 2
    assert "not a directory" in capsys.readouterr().err
