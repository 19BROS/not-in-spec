"""Component C: `Example`s from chunks and their raw call records (SPEC §4, §6.2)."""

from collections.abc import Callable
from pathlib import Path

import pytest

from notinspec.adapters.canonical import canonical_json
from notinspec.adapters.python import RawCallRecord, Value
from notinspec.chunking import Chunk, Document, chunk_blocks, chunk_document
from notinspec.examples import chunk_examples, extract_examples, read_calls
from notinspec.sphinx import read_sphinx_xml

EXAMPLES = Path(__file__).parents[2] / "examples" / "sphinx"

GUIDE = """\
# Guide

Connect:

```python
import acme
acme.connect(timeout=10)
```

- a list item with code:

  ```python
  acme.close()
  ```

```bash
$ acme --help
```
"""


def _chunks(text: str) -> tuple[Chunk, ...]:
    return chunk_document(Document("guide.md", text), project="acme")


def test_every_code_block_is_an_example_in_document_order() -> None:
    (chunk,) = _chunks(GUIDE)
    examples = chunk_examples(chunk)
    assert [(e.position, e.lang, e.nested) for e in examples] == [
        (0, "python", False),
        (1, "python", True),
        (2, "bash", False),
    ]
    assert examples[1].code == "acme.close()\n"
    assert {e.chunk_id for e in examples} == {chunk.id}
    assert {e.section_id for e in examples} == {chunk.section_id}
    assert len({e.id for e in examples}) == 3


def test_editing_the_code_keeps_the_id_and_changes_the_hash() -> None:
    before = extract_examples(_chunks(GUIDE))
    after = extract_examples(_chunks(GUIDE.replace("timeout=10", "timeout=20")))
    assert [e.id for e in before] == [e.id for e in after]
    assert before[0].content_hash != after[0].content_hash
    assert before[1:] == after[1:]


def test_changing_the_language_changes_the_hash() -> None:
    before = extract_examples(_chunks(GUIDE))[0]
    after = extract_examples(_chunks(GUIDE.replace("```python\nimport", "```py\nimport")))[0]
    assert (before.id, before.code) == (after.id, after.code)
    assert before.content_hash != after.content_hash


def test_math_block_is_not_an_example() -> None:
    xml = EXAMPLES / "urllib3" / "xml"
    chunks = [c for d in read_sphinx_xml(xml).documents for c in chunk_blocks(d, project="u")]
    math = [b for c in chunks for b in c.blocks if b.kind == "code" and b.lang == "math"]
    examples = extract_examples(chunks)
    assert all(e.lang != "math" for e in examples)
    assert len(examples) == sum(1 for c in chunks for b in c.blocks if b.kind == "code") - len(math)


def test_read_calls_routes_by_language() -> None:
    python, nested, bash = extract_examples(_chunks(GUIDE))
    result = read_calls(python)
    assert result is not None
    assert (result.example_id, result.adapter, result.status) == (python.id, "python", "ok")
    assert [c.symbol for c in result.calls] == ["acme.connect"]
    nested_result = read_calls(nested)
    assert nested_result is not None
    assert nested_result.calls[0].callee == Value(
        "name", "acme.close", name="acme", attrs=("close",)
    )
    assert read_calls(bash) is None


def test_invalid_python_example_keeps_its_error() -> None:
    (chunk,) = _chunks("# T\n\n```python\nf(\n```\n")
    (example,) = chunk_examples(chunk)
    result = read_calls(example)
    assert result is not None
    assert (result.status, result.calls) == ("invalid", ())
    assert result.error is not None


def _value(v: Value) -> str:
    """One value, compact: every field of `Value` that its kind uses."""
    attrs = "".join(f".{a}" for a in v.attrs)
    match v.kind:
        case "literal":
            return canonical_json(v.literal).decode()
        case "call":
            return f"#{v.call}{attrs}"
        case "import":
            return f"<{v.path}>"
        case "name":
            return f"?{v.name}{attrs}"
        case "unpack":
            return v.source
        case _:
            return f"`{v.source}`"


def _call(c: RawCallRecord) -> str:
    """`#index Lline-end symbol = callee(args, name=value)`: easy to review in a diff."""
    args = [_value(a) for a in c.args] + [
        f"{k.name}={_value(k.value)}" if k.name else _value(k.value) for k in c.kwargs
    ]
    lines = f"L{c.line}" if c.line == c.end_line else f"L{c.line}-{c.end_line}"
    return f"#{c.index} {lines} {c.symbol} = {_value(c.callee)}({', '.join(args)})"


def _golden_examples(library: str) -> list[dict[str, object]]:
    sphinx = read_sphinx_xml(EXAMPLES / library / "xml")
    chunks = [c for d in sphinx.documents for c in chunk_blocks(d, project=library)]
    breadcrumbs = {c.id: c.breadcrumb for c in chunks}
    rows: list[dict[str, object]] = []
    for example in extract_examples(chunks):
        calls = read_calls(example)
        rows.append(
            {
                "id": example.id,
                "chunk": f"{example.chunk_id} {breadcrumbs[example.chunk_id]}",
                "position": example.position,
                "lang": example.lang,
                "lines": f"{example.start_line}-{example.end_line}",
                "nested": example.nested,
                "content_hash": example.content_hash,
                "status": calls.status if calls else None,
                "error": calls.error if calls else None,
                "calls": [_call(c) for c in calls.calls] if calls else [],
            }
        )
    return rows


def test_urllib3_examples_golden(golden: Callable[[str, object], None]) -> None:
    golden("urllib3", _golden_examples("urllib3"))


@pytest.mark.parametrize("library", ["urllib3", "trio", "hydra-zen"])
def test_examples_are_deterministic_and_never_crash(library: str) -> None:
    sphinx = read_sphinx_xml(EXAMPLES / library / "xml")
    chunks = [c for d in sphinx.documents for c in chunk_blocks(d, project=library)]
    first = extract_examples(chunks)
    assert first == extract_examples(chunks)
    assert len({e.id for e in first}) == len(first)
    results = [read_calls(e) for e in first]
    assert canonical_json(results) == canonical_json([read_calls(e) for e in first])
    for result in results:
        if result is not None and result.status != "ok":
            assert result.error and result.calls == ()
        for call in result.calls if result else ():
            refs = [call.callee, *call.args, *(k.value for k in call.kwargs)]
            assert all(r.call is None or r.call < call.index for r in refs)
