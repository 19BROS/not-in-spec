"""`Example` → call records: pick the language adapter, then normalize (SPEC §6.2, component C).

MVP adapters are Python (`ast`) and curl; only Python exists so far. A block in a language
no adapter reads (`bash`, `text`, `json`, ...) gives no record at all, not an error.

Two steps, so the inventory is needed only for the second: `read_calls` gives raw call
records (the call as written), `normalize_example` maps them onto the inventory and lists the
symbols the inventory lacks (`Source` example, SPEC §6.3).
"""

from dataclasses import dataclass

from notinspec.adapters.python import (
    PYTHON_ADAPTER_VERSION,
    ApiIndex,
    CallRecord,
    PythonCode,
    RawCallRecord,
    UnresolvedCall,
    accepts,
    example_additions,
    normalize_calls,
    parse_python,
)
from notinspec.examples.extract import Example
from notinspec.inventory import Symbol


@dataclass(frozen=True)
class ExampleCalls:
    example_id: str
    adapter: str  # "python"
    adapter_version: int
    status: str  # "ok" | "invalid" (explicit language, does not parse) | "not-python"
    calls: tuple[RawCallRecord, ...]
    error: str | None = None


def read_calls(example: Example) -> ExampleCalls | None:
    """Raw call records of one example, or None when no adapter reads its language. Pure."""
    if not accepts(example.lang):
        return None
    result: PythonCode = parse_python(example.code, example.lang)
    return ExampleCalls(
        example_id=example.id,
        adapter="python",
        adapter_version=PYTHON_ADAPTER_VERSION,
        status=result.status,
        calls=result.calls,
        error=result.error,
    )


@dataclass(frozen=True)
class ExampleCallRecords:
    example_id: str
    calls: tuple[CallRecord, ...]
    unresolved: tuple[UnresolvedCall, ...]  # not the documented API, or not known which
    additions: tuple[Symbol, ...]  # called, in the project's packages, missing in the inventory


def normalize_example(example: Example, raw: ExampleCalls, api: ApiIndex) -> ExampleCallRecords:
    """Call records of one example, mapped onto the inventory. Pure."""
    if raw.example_id != example.id:
        raise ValueError(f"raw calls of {raw.example_id} given for example {example.id}")
    normalized = normalize_calls(raw.calls, api)
    return ExampleCallRecords(
        example_id=example.id,
        calls=normalized.calls,
        unresolved=normalized.unresolved,
        additions=example_additions(raw.calls, normalized, api, example.section_id),
    )
