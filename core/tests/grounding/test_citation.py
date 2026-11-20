from pathlib import Path

import pytest

from notinspec.chunking import Chunk, Document, chunk_blocks, chunk_document
from notinspec.grounding import check_citation, nli_premise, normalize
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


URLLIB3 = Path(__file__).parents[2] / "examples" / "sphinx" / "urllib3" / "xml"


def test_a_repeated_citation_returns_every_prose_match() -> None:
    xml = read_sphinx_xml(URLLIB3)
    chunks = [c for d in xml.documents for c in chunk_blocks(d, project="urllib3")]
    retry = next(c for c in chunks if c.breadcrumb == "urllib3 > Utilities > Retry")
    result = check_citation(retry, "Set to `0` to fail on the first retry of this type.")
    assert result.status == "found"
    assert len(result.spans) == 5
    assert result.span == result.spans[0]
    assert list(result.spans) == sorted(result.spans)
    crumbs = [nli_premise(retry, span).text.split(":", 1)[0] for span in result.spans]
    assert crumbs == [
        f"urllib3 > Utilities > Retry > {name}"
        for name in ("connect", "read", "redirect", "status", "other")
    ]


def test_a_single_match_has_one_span() -> None:
    result = check_citation(GUIDE, "A timeout")
    assert result.status == "not_found"
    result = check_citation(GUIDE, "is given in")
    assert result.spans == (result.span,)
    code = check_citation(GUIDE, "connect(timeout=2.5)")
    assert code.status == "not_checkable" and code.spans == (code.span,)


# --- looser matches (GROUNDING_VERSION 2, issue #42) -------------------------------------


@pytest.mark.parametrize(
    "citation",
    [
        "you\x02re able to see those warnings",  # run 008: qwen wrote \x02 for ’
        "we\x00ve added a top-level function",
        "you're able to see those warnings",
    ],
)
def test_a_control_character_matches_an_apostrophe(citation: str) -> None:
    chunk = _chunk(
        "# A\n\nEnsure you’re able to see those warnings: we’ve added a top-level function.\n"
    )
    assert check_citation(chunk, citation).status == "found"


@pytest.mark.parametrize("dash", ["‐", "‑", "‒", "―", "−"])
def test_hyphen_variants_and_minus_are_plain_hyphens(dash: str) -> None:
    chunk = _chunk("# A\n\nWhen you’re sub-classing an interface, pass -1.\n")
    assert check_citation(chunk, f"you’re sub{dash}classing an interface, pass {dash}1").status == (
        "found"
    )


def test_a_list_marker_after_a_colon_matches_the_next_line() -> None:
    xml = read_sphinx_xml(URLLIB3)
    chunks = [c for d in xml.documents for c in chunk_blocks(d, project="urllib3")]
    start = next(
        c for c in chunks if c.breadcrumb == "urllib3 > Utilities > Timeout > start_connect()"
    )
    citation = (
        "Raises: - `urllib3.exceptions.TimeoutStateError` – if you attempt to start a timer"
        " that has been started already."
    )
    result = check_citation(start, citation)
    assert result.status == "found"
    assert result.span is not None
    assert start.text[result.span[0] : result.span[1]].startswith("**Raises:**\n")


def test_a_list_marker_after_a_colon_in_the_text_still_matches_exactly() -> None:
    chunk = _chunk("# A\n\nThree options: - fast, - safe and - small.\n")
    result = check_citation(chunk, "options: - fast, - safe")
    assert result.status == "found"
    assert result.span is not None
    assert chunk.text[result.span[0] : result.span[1]] == "options: - fast, - safe"


RETRIES = _chunk(
    "# Retries\n"
    "\n"
    "By default, urllib3 will retry requests 3 times and follow up to 3 redirects.\n"
    "\n"
    "Set `retries=False` to disable both.\n"
    "\n"
    "```python\n"
    "Url(scheme='http', host='google.com', ...)\n"
    "```\n"
)


@pytest.mark.parametrize(
    "citation",
    [
        "By default, urllib3 will ... follow up to 3 redirects",
        "By default, urllib3 will…follow up to 3 redirects",
        "By default, ... retry requests ... up to 3 redirects",
        "... retry requests 3 times",  # a leading ellipsis leaves one part
    ],
)
def test_an_ellipsis_matches_its_parts_in_order_in_one_block(citation: str) -> None:
    result = check_citation(RETRIES, citation)
    assert result.status == "found"
    assert result.span is not None


def test_an_ellipsis_span_runs_from_the_first_part_to_the_last() -> None:
    result = check_citation(RETRIES, "urllib3 will ... follow up to 3 redirects")
    assert result.span is not None
    assert RETRIES.text[result.span[0] : result.span[1]] == (
        "urllib3 will retry requests 3 times and follow up to 3 redirects"
    )


@pytest.mark.parametrize(
    "citation",
    [
        "follow up to 3 redirects ... By default, urllib3",  # parts out of order
        "follow up to 3 redirects. ... to disable both",  # parts in two blocks
        "By default ... redirects",  # a one-word part matches too much
        "By default, urllib3 will ... follow up to 5 redirects",  # a part not in the text
    ],
)
def test_an_ellipsis_is_not_found_otherwise(citation: str) -> None:
    assert check_citation(RETRIES, citation).status == "not_found"


def test_an_ellipsis_in_code_is_matched_exactly() -> None:
    result = check_citation(RETRIES, "Url(scheme='http', host='google.com', ...)")
    assert result.status == "not_checkable"
