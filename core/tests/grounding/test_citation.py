from pathlib import Path

import pytest

from notinspec.chunking import Chunk, Document, chunk_blocks, chunk_document
from notinspec.grounding import check_citation, normalize
from notinspec.sphinx import read_sphinx_xml


def _chunk(text: str) -> Chunk:
    return chunk_document(Document("docs/a.md", text), project="acme")[0]


GUIDE = _chunk(
    "# Timeouts\n"
    "\n"
    "The `timeout` parameter is given in\n"
    "seconds. See the [API reference](api.md) for **all** options.\n"
    "\n"
    "Use “retries” to retry:\n"
    "\n"
    "- `0` fails on the first error.\n"
    "- `None` retries forever.\n"
    "\n"
    "```python\n"
    "connect(timeout=2.5)\n"
    "```\n"
    "\n"
    "| Option | Default |\n"
    "| --- | --- |\n"
    "| `timeout` | `None` |\n"
)


def test_normalize_drops_markup_whitespace_and_typographic_quotes() -> None:
    assert normalize("  The `timeout`\n  is **given**  in “seconds”. ") == (
        'The timeout is given in "seconds".'
    )
    assert normalize("See the [API reference](api.md) and <https://x.org>.") == (
        "See the API reference and https://x.org."
    )
    assert normalize("- `0` fails\n> quoted\n## Heading") == "0 fails quoted Heading"


@pytest.mark.parametrize(
    "citation",
    [
        "The `timeout` parameter is given in seconds.",  # wrapped line in the chunk
        "The timeout parameter is given in seconds",  # backticks dropped by the extractor
        "See the API reference for all options",  # link and bold markup dropped
        'Use "retries" to retry',  # plain quotes for typographic ones
        "- `0` fails on the first error.",  # with the list marker
    ],
)
def test_found_in_prose(citation: str) -> None:
    result = check_citation(GUIDE, citation)
    assert result.status == "found"
    assert result.span is not None


def test_span_points_into_the_raw_text() -> None:
    result = check_citation(GUIDE, "`timeout` parameter is given in seconds")
    assert result.span is not None
    assert GUIDE.text[result.span[0] : result.span[1]] == (
        "`timeout` parameter is given in\nseconds"
    )


@pytest.mark.parametrize("citation", ["connect(timeout=2.5)", "| `timeout` | `None` |", "Timeouts"])
def test_only_outside_prose_is_not_checkable(citation: str) -> None:
    result = check_citation(GUIDE, citation)
    assert result.status == "not_checkable"
    assert result.span is not None


@pytest.mark.parametrize("citation", ["", "  ", "given in minutes", "seconds is given"])
def test_not_found(citation: str) -> None:
    assert check_citation(GUIDE, citation).status == "not_found"
    assert check_citation(GUIDE, citation).span is None


def test_a_match_in_prose_wins_over_an_earlier_one_in_code() -> None:
    chunk = _chunk("# A\n\n```python\nretries = 3\n```\n\nSet retries = 3 to retry three times.\n")
    result = check_citation(chunk, "retries = 3")
    assert result.status == "found"
    assert result.span is not None
    assert chunk.text[: result.span[0]].endswith("Set ")


def test_a_citation_across_two_prose_blocks_is_found() -> None:
    chunk = _chunk("# A\n\nFirst paragraph ends here.\n\nSecond one starts here.\n")
    assert check_citation(chunk, "ends here. Second one").status == "found"


SPHINX = Path(__file__).parents[1] / "fixtures" / "sphinx"


def test_field_entry_en_dash_matches_a_plain_hyphen() -> None:
    xml = read_sphinx_xml(SPHINX / "xml-plain")
    chunks = [c for d in xml.documents for c in chunk_blocks(d, project="fixturelib")]
    connect = next(c for c in chunks if c.breadcrumb.endswith("> connect()"))
    result = check_citation(connect, "`timeout` (float or None) - Seconds to wait")
    assert result.status == "found"
    assert result.span is not None
    assert connect.text[result.span[0] : result.span[1]] == (
        "`timeout` (float or None) – Seconds to wait"
    )


@pytest.mark.parametrize(
    ("text", "citation"),
    [
        ("Retries — unless disabled — are counted.", "Retries - unless disabled - are counted."),
        ("Retries - unless disabled - are counted.", "Retries — unless disabled – are counted."),
        ("Pages 1–3 — see below.", "Pages 1-3 – see below."),
    ],
)
def test_en_and_em_dashes_are_plain_hyphens(text: str, citation: str) -> None:
    chunk = _chunk(f"# A\n\n{text}\n")
    result = check_citation(chunk, citation)
    assert result.status == "found"
    assert result.span is not None
    assert chunk.text[result.span[0] : result.span[1]] == text
    assert normalize("a – b — c") == "a - b - c"
