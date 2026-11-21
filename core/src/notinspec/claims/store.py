"""Where extraction writes: the append-only call log and the claim store for reuse.

**Call log** (SPEC §10: raw LLM responses are append-only): one record per request actually
sent to the provider, with the raw body, usage and time. A JSONL file is only ever appended to.
The DB stores the same records later.

**Claim store**: extraction is generation, not a model under test, so the claims of a chunk are
reused while the chunk's text, its breadcrumb (which is in the prompt), the extractor, its model,
its reasoning effort, the prompt version and the parser version stay the same. Only parsed
answers are stored, with their skipped claims and the call that produced them; a failed chunk is
asked again by the next run.
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
    # how much the model reasons changes its answer; entries stored before this field have None
    reasoning_effort: str | None = None
    # `claims.parse.PARSER_VERSION` that parsed the stored answer; entries stored before this
    # field have None, so they are asked again (version 1 stored some cut-off answers)
    parser_version: int | None = None
    # not `max_tokens`: it only decides whether an answer is cut off, and cut-off answers are
    # never stored


@dataclass(frozen=True)
class StoredAnswer:
    """A parsed answer, kept for reuse together with the call that produced it."""

    claims: tuple[RawClaim, ...]
    problems: tuple[str, ...]  # claims of the answer that were skipped, and why
    run_id: str
    prompt_hash: str
    model: str  # exact model ID that answered


class ClaimStore(Protocol):
    def get(self, key: ReuseKey) -> StoredAnswer | None: ...
    def put(self, key: ReuseKey, answer: StoredAnswer) -> None: ...


class MemoryClaimStore:
    def __init__(self) -> None:
        self._items: dict[ReuseKey, StoredAnswer] = {}

    def get(self, key: ReuseKey) -> StoredAnswer | None:
        return self._items.get(key)

    def put(self, key: ReuseKey, answer: StoredAnswer) -> None:
        self._items[key] = answer


class JsonlClaimStore:
    """A JSONL file of {key, answer}, read once and appended to. A later line wins.

    A crash while writing can cut off only the last line, so a broken last line is removed
    from the file with a warning (`warnings`), and the run asks for that chunk again. A broken
    line anywhere else means the file was damaged otherwise, which is an error.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.warnings: list[str] = []
        self._items: dict[ReuseKey, StoredAnswer] = {}
        if not path.exists():
            return
        data = path.read_bytes()
        lines = data.split(b"\n")
        offset = 0
        for number, line in enumerate(lines, 1):
            start, offset = offset, offset + len(line) + 1
            if not line.strip():
                continue
            try:
                key, answer = _entry(line)
            except (ValueError, TypeError, KeyError) as e:
                if any(rest.strip() for rest in lines[number:]):
                    raise ValueError(f"{path}:{number}: not a claim store entry: {e}") from e
                with path.open("r+b") as f:
                    f.truncate(start)
                self.warnings.append(
                    f"{path.name}:{number}: removed a cut-off last line ({e}); "
                    "its chunk is asked again"
                )
                return
            self._items[key] = answer
        if data and not data.endswith(b"\n"):  # a whole last line whose newline was cut off
            with path.open("ab") as f:
                f.write(b"\n")

    def get(self, key: ReuseKey) -> StoredAnswer | None:
        return self._items.get(key)

    def put(self, key: ReuseKey, answer: StoredAnswer) -> None:
        self._items[key] = answer
        entry = {"key": asdict(key), "answer": asdict(answer)}
        with self.path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def _entry(line: bytes) -> tuple[ReuseKey, StoredAnswer]:
    entry = json.loads(line)
    answer = entry["answer"]
    stored = StoredAnswer(
        claims=tuple(RawClaim(**c) for c in answer["claims"]),
        problems=tuple(str(p) for p in answer["problems"]),
        run_id=str(answer["run_id"]),
        prompt_hash=str(answer["prompt_hash"]),
        model=str(answer["model"]),
    )
    return ReuseKey(**entry["key"]), stored
