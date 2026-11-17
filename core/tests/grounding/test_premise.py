import pytest

from notinspec.chunking import Chunk, Document, chunk_document
from notinspec.grounding import PREMISE_RULE, check_citation, nli_premise


def _chunk(text: str) -> Chunk:
    return chunk_document(Document("docs/a.md", text), project="acme")[0]


def _premise(chunk: Chunk, citation: str) -> str:
    result = check_citation(chunk, citation)
    assert result.status == "found" and result.span is not None
    premise = nli_premise(chunk, result.span)
    assert premise.rule == PREMISE_RULE
    return premise.text


def test_cited_sentence_plus_one_on_each_side_within_the_block() -> None:
    chunk = _chunk(
        "# Retries\n\nOne. Two. Three. Four. Five.\n\nNext paragraph is another block.\n"
    )
    assert _premise(chunk, "Three.") == "acme > Retries: Two. Three. Four."
    assert _premise(chunk, "Five.") == "acme > Retries: Four. Five."
    assert _premise(chunk, "Two. Three.") == "acme > Retries: One. Two. Three. Four."


def test_list_item_gets_the_lead_in_and_stays_in_its_item() -> None:
    chunk = _chunk(
        "# Retry\n\n"
        "Some text. The following values are allowed:\n\n"
        "- `0` fails on the first error.\n"
        "- `None` retries forever. It never stops.\n"
        "- `3` retries three times.\n"
    )
    assert _premise(chunk, "retries three times") == (
        "acme > Retry: The following values are allowed: 3 retries three times."
    )
    assert _premise(chunk, "It never stops.") == (
        "acme > Retry: The following values are allowed: None retries forever. It never stops."
    )


def test_no_lead_in_without_a_colon_or_with_code_in_between() -> None:
    no_colon = _chunk("# A\n\nSome values.\n\n- one is first.\n- two is second.\n")
    assert _premise(no_colon, "two is second.") == "acme > A: two is second."
    code_between = _chunk("# A\n\nValues:\n\n```\nx\n```\n\n- one is first.\n")
    assert _premise(code_between, "one is first.") == "acme > A: one is first."


def test_span_covers_the_sentences_used() -> None:
    chunk = _chunk("# A\n\nValues:\n\n- one is first.\n")
    result = check_citation(chunk, "one is first.")
    assert result.span is not None
    premise = nli_premise(chunk, result.span)
    assert chunk.text[premise.span[0] : premise.span[1]] == "Values:\n\n- one is first."


def test_span_outside_prose_is_an_error() -> None:
    chunk = _chunk("# A\n\nText.\n\n```\ncode here\n```\n")
    result = check_citation(chunk, "code here")
    assert result.status == "not_checkable" and result.span is not None
    with pytest.raises(ValueError, match="not in the prose"):
        nli_premise(chunk, result.span)
