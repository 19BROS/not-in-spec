"""Golden NLI premises on the Sphinx fixture project, in all three builds (SPEC §13)."""

from collections.abc import Callable
from pathlib import Path

import pytest

from notinspec.chunking import chunk_blocks
from notinspec.grounding import check_citation, nli_premise
from notinspec.sphinx import read_sphinx_xml

SPHINX = Path(__file__).parents[1] / "fixtures" / "sphinx"

CITATIONS = (
    "Seconds to wait; `None` waits forever.",  # parameter entry: name in the breadcrumb
    "Set to `0` to fail on the first error.",  # continuation paragraph of an entry
    "If the server does not answer within `timeout` seconds.",  # Raises entry
    "Maximum number of bytes",  # numpydoc / napoleon entry vs. a plain list
    "two",  # list item inside an admonition: lead-in from the same block
    "A word with its definition.",  # list item after "Definitions:"
    "A timeout is in seconds.",  # plain paragraph
    "Closing twice raises `RuntimeError`.",  # admonition in an API description
    "At most `100` connections.",  # footnote
    'conn = connect("example.com", timeout=2.5)',  # code only → not checkable
    "`None` (wait forever)",  # table only → not checkable
    "Never written anywhere.",  # → not found
)


@pytest.mark.parametrize("build", ["xml-plain", "xml-napoleon", "xml-numpydoc"])
def test_premises(build: str, golden: Callable[[str, object], None]) -> None:
    xml = read_sphinx_xml(SPHINX / build)
    chunks = [c for d in xml.documents for c in chunk_blocks(d, project="fixturelib")]
    results = []
    for citation in CITATIONS:
        entry: dict[str, object] = {"citation": citation, "status": "not_found"}
        for chunk in chunks:
            check = check_citation(chunk, citation)
            if check.status == "not_found" or check.span is None:
                continue
            start, end = check.span
            entry = {
                "citation": citation,
                "status": check.status,
                "chunk": chunk.breadcrumb,
                "span": chunk.text[start:end],
            }
            if check.status == "found":
                entry["premise"] = nli_premise(chunk, check.span).text
            break
        results.append(entry)
    golden(f"premises-{build}", results)
