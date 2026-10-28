from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from notinspec.runner import ChatRequest, Completion, FakeProvider, RecordingProvider
from notinspec.runner.openrouter import parse_completion


class Live:
    def __init__(self, body: dict[str, Any]) -> None:
        self.body = body

    def complete(self, request: ChatRequest) -> Completion:
        return parse_completion(self.body, request.model)


def test_record_then_replay(tmp_path: Path, request_: ChatRequest, body: dict[str, Any]) -> None:
    recorder = RecordingProvider(Live(body))
    live = recorder.complete(request_)
    fixture = tmp_path / "recorded.json"
    recorder.save(fixture)

    fake = FakeProvider.load(fixture)
    assert fake.complete(request_) == live
    assert fake.calls == [request_]


def test_missing_recording(request_: ChatRequest, body: dict[str, Any]) -> None:
    fake = FakeProvider({(request_.model, request_.prompt_hash()): body})
    with pytest.raises(LookupError, match="no recording for acme/model-b:free"):
        fake.complete(replace(request_, model="acme/model-b:free"))
