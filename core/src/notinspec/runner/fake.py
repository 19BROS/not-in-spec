"""Recorded responses, so tests and CI never call OpenRouter (SPEC §9).

A recording file is a JSON list of {"model", "prompt_hash", "request", "response"}, where
`response` is the provider's raw body. Replaying goes through the same parsing as a live call.
`request` is there for humans reading the fixture; replay ignores it.
"""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from notinspec.runner.openrouter import parse_completion
from notinspec.runner.provider import ChatRequest, Completion, Provider


class FakeProvider:
    def __init__(self, recordings: dict[tuple[str, str], dict[str, Any]]) -> None:
        self._recordings = recordings
        self.calls: list[ChatRequest] = []

    @classmethod
    def load(cls, path: Path) -> "FakeProvider":
        entries = json.loads(path.read_text(encoding="utf-8"))
        return cls({(e["model"], e["prompt_hash"]): e["response"] for e in entries})

    def complete(self, request: ChatRequest) -> Completion:
        self.calls.append(request)
        key = (request.model, request.prompt_hash())
        if key not in self._recordings:
            raise LookupError(f"no recording for {key[0]} prompt {key[1]}")
        return parse_completion(self._recordings[key], request.model)


class RecordingProvider:
    """Wraps a live provider and keeps every answer, to be saved as a fixture."""

    def __init__(self, inner: Provider) -> None:
        self._inner = inner
        self._entries: list[dict[str, Any]] = []

    def complete(self, request: ChatRequest) -> Completion:
        completion = self._inner.complete(request)
        self._entries.append(
            {
                "model": request.model,
                "prompt_hash": request.prompt_hash(),
                "request": asdict(request),
                "response": completion.raw,
            }
        )
        return completion

    def save(self, path: Path) -> None:
        text = json.dumps(self._entries, indent=2, ensure_ascii=False, sort_keys=True)
        path.write_text(text + "\n", encoding="utf-8")
