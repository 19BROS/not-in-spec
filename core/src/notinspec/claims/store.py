"""Where extraction writes: the append-only call log and the claim store for reuse.

**Call log** (SPEC §10: raw LLM responses are append-only): one record per request actually
sent to the provider, with the raw body, usage and time. A JSONL file is only ever appended to.
The DB stores the same records later.

**Claim store**: extraction is generation, not a model under test, so the claims of a chunk are
reused while the chunk's text, its breadcrumb (which is in the prompt), the extractor, its model
and the prompt version stay the same. Only parsed answers are stored; a failed chunk is asked
again by the next run.
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Protocol

from notinspec.claims.model import RawClaim


@dataclass(frozen=True)
class LlmCall:
    run_id: str
    role: str  # "claim-extractor" (SPEC §8 roles)
    extractor: str
    chunk_id: str
    model: str  # requested model ID
    prompt_hash: str
    request: dict[str, Any]  # the whole ChatRequest
    response: dict[str, Any] | None  # the provider's raw body; None when no answer came back
    error: str | None  # why there is no answer
    time: str  # UTC, ISO 8601, when the answer (or the error) arrived


class CallLog(Protocol):
    def append(self, call: LlmCall) -> None: ...


class MemoryCallLog:
    def __init__(self) -> None:
        self.calls: list[LlmCall] = []

    def append(self, call: LlmCall) -> None:
        self.calls.append(call)


class JsonlCallLog:
    """Appends one JSON line per call and closes the file, so a crash keeps every earlier call."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def append(self, call: LlmCall) -> None:
        line = json.dumps(asdict(call), ensure_ascii=False, sort_keys=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(line + "\n")


@dataclass(frozen=True)
class ReuseKey:
    content_hash: str  # Chunk.content_hash: the chunk's text
    breadcrumb: str  # part of the prompt, not of the content hash
    extractor: str
    model: str
    prompt_version: int


class ClaimStore(Protocol):
    def get(self, key: ReuseKey) -> tuple[RawClaim, ...] | None: ...
    def put(self, key: ReuseKey, claims: tuple[RawClaim, ...]) -> None: ...


class MemoryClaimStore:
    def __init__(self) -> None:
        self._items: dict[ReuseKey, tuple[RawClaim, ...]] = {}

    def get(self, key: ReuseKey) -> tuple[RawClaim, ...] | None:
        return self._items.get(key)

    def put(self, key: ReuseKey, claims: tuple[RawClaim, ...]) -> None:
        self._items[key] = claims


class JsonlClaimStore:
    """A JSONL file of {key, claims}, read once and appended to. A later line wins."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._items: dict[ReuseKey, tuple[RawClaim, ...]] = {}
        if path.exists():
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    key = ReuseKey(**entry["key"])
                    claims = tuple(RawClaim(**c) for c in entry["claims"])
                except (ValueError, TypeError, KeyError) as e:
                    raise ValueError(f"{path}:{number}: not a claim store entry: {e}") from e
                self._items[key] = claims

    def get(self, key: ReuseKey) -> tuple[RawClaim, ...] | None:
        return self._items.get(key)

    def put(self, key: ReuseKey, claims: tuple[RawClaim, ...]) -> None:
        self._items[key] = claims
        entry = {"key": asdict(key), "claims": [asdict(c) for c in claims]}
        with self.path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
