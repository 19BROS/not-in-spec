"""`Example` → raw call records: pick the language adapter (SPEC §6.2, component C).

MVP adapters are Python (`ast`) and curl; only Python exists so far. A block in a language
no adapter reads (`bash`, `text`, `json`, ...) gives no record at all, not an error.
"""

from dataclasses import dataclass

from notinspec.adapters.python import (
    PYTHON_ADAPTER_VERSION,
    PythonCode,
    RawCallRecord,
    accepts,
    parse_python,
)
from notinspec.examples.extract import Example


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
