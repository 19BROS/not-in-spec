"""Python adapter for component C: code → raw call records → call records (SPEC §6.2).

`calls.py` parses code with `ast` (no inventory needed); `normalize.py` maps the raw records
onto the inventory. Model answers in L3 go through the same two steps (SPEC §6.10).
"""

from notinspec.adapters.python.calls import (
    AUTO_LANGS,
    PYTHON_ADAPTER_VERSION,
    PYTHON_LANGS,
    Keyword,
    PythonCode,
    RawCallRecord,
    Value,
    accepts,
    parse_python,
)
from notinspec.adapters.python.normalize import (
    CLASS_KINDS,
    ApiIndex,
    Argument,
    CallIssue,
    CallRecord,
    Lookup,
    NormalizedCalls,
    UnresolvedCall,
    example_additions,
    normalize_calls,
)

__all__ = [
    "AUTO_LANGS",
    "CLASS_KINDS",
    "PYTHON_ADAPTER_VERSION",
    "PYTHON_LANGS",
    "ApiIndex",
    "Argument",
    "CallIssue",
    "CallRecord",
    "Keyword",
    "Lookup",
    "NormalizedCalls",
    "PythonCode",
    "RawCallRecord",
    "UnresolvedCall",
    "Value",
    "accepts",
    "example_additions",
    "normalize_calls",
    "parse_python",
]
