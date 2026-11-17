import json
from pathlib import Path
from typing import Any

import pytest

from notinspec import __version__
from notinspec.cli import main
from notinspec.runner import (
    GROQ,
    OPENROUTER,
    ChatRequest,
    Completion,
    ModelInfo,
    OpenAICompatProvider,
    ProviderConfig,
    ProviderError,
)
from notinspec.runner.openai_compat import parse_completion


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
    """Stands in for the live provider: answers per model, or raises."""

    def __init__(self, content: str, answers: dict[str, str | ProviderError] | None = None) -> None:
        self.content = content
        self.answers = answers or {}
        self.requests: list[ChatRequest] = []
        self.config = GROQ

    def complete(self, request: ChatRequest) -> Completion:
        self.requests.append(request)
        answer = self.answers.get(request.model, self.content)
        if isinstance(answer, ProviderError):
            raise answer
        body = {"model": request.model, "choices": [{"message": {"content": answer}}]}
        return parse_completion(body, request.model)

    def list_models(self) -> list[ModelInfo]:
        return [
            ModelInfo("llama-3.3-70b-versatile", 131072, False),
            ModelInfo("openai/gpt-oss-20b", 131072, True),
        ]


def use(monkeypatch: pytest.MonkeyPatch, stub: Stub) -> list[ProviderConfig]:
    configs: list[ProviderConfig] = []

    def from_env(cls: type, config: ProviderConfig = GROQ) -> Stub:
        configs.append(config)
        stub.config = config
        return stub

    monkeypatch.setattr(OpenAICompatProvider, "from_env", classmethod(from_env))
    return configs


def test_ask_prints_parsed_request(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    stub = Stub('{"method": "get", "path": "/pets/1"}')
    configs = use(monkeypatch, stub)
    fixture = tmp_path / "rec.json"

    assert main(["ask", "--model", "openai/gpt-oss-20b", "--record", str(fixture), "Pet 1"]) == 0
    out = capsys.readouterr().out
    assert '"method": "GET"' in out and '"path": "/pets/1"' in out
    assert stub.requests[0].response_schema is not None
    assert configs == [GROQ]  # Groq unless asked otherwise
    recorded: list[dict[str, Any]] = json.loads(fixture.read_text(encoding="utf-8"))
    assert recorded[0]["model"] == "openai/gpt-oss-20b"


def test_ask_defaults_to_qwen(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    stub = Stub('{"method": "GET", "path": "/pets/1"}')
    use(monkeypatch, stub)
    assert main(["ask", "Pet 1"]) == 0
    assert stub.requests[0].model == GROQ.default_model == "qwen/qwen3.8-27b"


def test_ask_needs_model_without_default(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    stub = Stub("")
    use(monkeypatch, stub)
    assert main(["ask", "--provider", "openrouter", "Pet 1"]) == 2
    assert "--model is required for openrouter" in capsys.readouterr().err
    assert stub.requests == []


def test_ask_reports_malformed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    stub = Stub("GET /pets/1")
    configs = use(monkeypatch, stub)
    args = ["ask", "--provider", "openrouter", "--model", "b/free:free", "--no-schema", "Pet 1"]
    assert main(args) == 0
    assert "malformed-output" in capsys.readouterr().out
    assert stub.requests[0].response_schema is None
    assert configs == [OPENROUTER]


def test_models(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    stub = Stub("")
    use(monkeypatch, stub)
    assert main(["models"]) == 0
    out = capsys.readouterr().out
    assert "llama-3.3-70b-versatile" in out and "openai/gpt-oss-20b" in out
    assert "probe" not in out and stub.requests == []  # listing asks no model
    assert main(["models", "--structured"]) == 0
    out = capsys.readouterr().out
    assert "llama" not in out and "openai/gpt-oss-20b" in out and "structured-output" in out


def test_models_probe(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    stub = Stub(
        '{"method": "GET", "path": "/pets/1"}',
        {"llama-3.3-70b-versatile": ProviderError("HTTP 400: response_format is not supported")},
    )
    use(monkeypatch, stub)
    assert main(["models", "--probe"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert "probe: rejected (ProviderError: HTTP 400: response_format" in lines[0]
    assert lines[1].endswith("probe: ok")
    assert all(r.response_schema is not None for r in stub.requests)


def test_models_probe_malformed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    use(monkeypatch, Stub("GET /pets/1"))
    assert main(["models", "--structured", "--probe"]) == 0
    assert "probe: answered, malformed-output (finish: None)" in capsys.readouterr().out


def test_missing_key_is_an_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    assert main(["models"]) == 2
    assert "GROQ_API_KEY is not set" in capsys.readouterr().err
