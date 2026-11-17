"""Component C: code examples in the docs → `Example`s and their call records (SPEC §6.2)."""

from notinspec.examples.calls import (
    ExampleCallRecords,
    ExampleCalls,
    normalize_example,
    read_calls,
)
from notinspec.examples.extract import (
    EXAMPLES_VERSION,
    Example,
    chunk_examples,
    extract_examples,
)

__all__ = [
    "EXAMPLES_VERSION",
    "Example",
    "ExampleCallRecords",
    "ExampleCalls",
    "chunk_examples",
    "extract_examples",
    "normalize_example",
    "read_calls",
]
