import json
from pathlib import Path
from typing import Any

import pytest

from notinspec import __version__
from notinspec.cli import main
from notinspec.runner import ChatRequest, Completion, ModelInfo, OpenRouterProvider
from notinspec.runner.openrouter import parse_completion


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
    assert "guide > Timeouts and retries > Migrating from 1.x" in out  # default: root's name
    assert " 1/2 " in out and " 2/2 " in out


def test_chunk_project_name(capsys: pytest.CaptureFixture[str]) -> None:
    code, out = _run(capsys, "--list", "--project", "urllib3")
    assert code == 0
    assert "urllib3 > Timeouts and retries > Migrating from 1.x" in out


def test_chunk_json(capsys: pytest.CaptureFixture[str]) -> None:
    code, out = _run(capsys, "--json", "--overlap-tokens", "0")
    data = json.loads(out)
    assert code == 0
    assert len(data["chunks"]) == 5
    assert set(data["windows"]) == {c["id"] for c in data["chunks"]}


def test_chunk_missing_root(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["chunk", "/nonexistent/docs"]) == 2
    assert "not a directory" in capsys.readouterr().err


class Stub:
    def __init__(self, content: str) -> None:
        self.content = content
        self.requests: list[ChatRequest] = []

    def complete(self, request: ChatRequest) -> Completion:
        self.requests.append(request)
        body = {"model": request.model, "choices": [{"message": {"content": self.content}}]}
        return parse_completion(body, request.model)

    def list_models(self) -> list[ModelInfo]:
        return [ModelInfo("a/paid", 8000, True), ModelInfo("b/free:free", None, False)]


def use(monkeypatch: pytest.MonkeyPatch, stub: Stub) -> None:
    monkeypatch.setattr(OpenRouterProvider, "from_env", classmethod(lambda cls: stub))


def test_ask_prints_parsed_request(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    stub = Stub('{"method": "get", "path": "/pets/1"}')
    use(monkeypatch, stub)
    fixture = tmp_path / "rec.json"

    assert main(["ask", "--model", "b/free:free", "--record", str(fixture), "Get pet 1"]) == 0
    out = capsys.readouterr().out
    assert '"method": "GET"' in out and '"path": "/pets/1"' in out
    assert stub.requests[0].response_schema is not None
    recorded: list[dict[str, Any]] = json.loads(fixture.read_text(encoding="utf-8"))
    assert recorded[0]["model"] == "b/free:free"


def test_ask_reports_malformed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    stub = Stub("GET /pets/1")
    use(monkeypatch, stub)
    assert main(["ask", "--model", "b/free:free", "--no-schema", "Get pet 1"]) == 0
    assert "malformed-output" in capsys.readouterr().out
    assert stub.requests[0].response_schema is None


def test_models_lists_free_only(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    use(monkeypatch, Stub(""))
    assert main(["models"]) == 0
    out = capsys.readouterr().out
    assert "b/free:free" in out and "a/paid" not in out
    assert main(["models", "--all"]) == 0
    assert "structured-output" in capsys.readouterr().out


def test_missing_key_is_an_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    assert main(["models"]) == 2
    assert "OPENROUTER_API_KEY is not set" in capsys.readouterr().err
