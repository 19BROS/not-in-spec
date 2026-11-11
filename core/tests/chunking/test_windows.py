from collections.abc import Callable
from pathlib import Path

import pytest

from notinspec.chunking import (
    Chunk,
    Document,
    NliWindow,
    chunk_document,
    chunk_documents,
    find_citation,
    load_documents,
    nli_windows,
    prose_sentences,
)
from notinspec.chunking.windows import clean_markdown

Golden = Callable[[str, object], None]
GUIDE = Path(__file__).parent / "fixtures" / "guide"


@pytest.fixture
def guide() -> dict[str, Chunk]:
    chunks = chunk_documents(load_documents(GUIDE, ["*.md"]))
    return {c.heading_path[-1] if c.heading_path else "": c for c in chunks}


def _chunk(text: str) -> Chunk:
    return chunk_document(Document("docs/a.md", text))[0]


def _sentences(text: str) -> list[str]:
    return [s.text for s in prose_sentences(_chunk(f"# A\n\n{text}\n"))]


def _small(chunk: Chunk) -> tuple[NliWindow, ...]:
    return nli_windows(chunk, max_tokens=60, overlap_tokens=12)


# --- golden files and determinism -------------------------------------------------------


def test_guide_chunks_golden(guide: dict[str, Chunk], golden: Golden) -> None:
    golden("chunks-guide", tuple(guide.values()))


def test_guide_windows_golden(guide: dict[str, Chunk], golden: Golden) -> None:
    golden("windows-guide-60", {c.id: _small(c) for c in guide.values()})


def test_same_chunk_same_windows(guide: dict[str, Chunk]) -> None:
    chunk = guide["Migrating from 1.x"]
    assert _small(chunk) == _small(chunk)


def test_window_id_is_chunk_id_plus_offset(guide: dict[str, Chunk]) -> None:
    chunk = guide["Timeouts"]
    for window in _small(chunk):
        assert window.chunk_id == chunk.id
        assert window.id == f"{chunk.id}@{window.start}"


# --- what goes into a window -------------------------------------------------------------


def test_code_and_tables_are_left_out(guide: dict[str, Chunk]) -> None:
    text = " ".join(w.text for w in nli_windows(guide["Timeouts"]))
    assert "TCP and TLS handshake" not in text  # table cell
    assert "A slow server is fine" not in text  # comment inside the code block
    assert "A timeout of 0 is not allowed" in text  # prose after the code


def test_code_inside_a_list_item_is_left_out(guide: dict[str, Chunk]) -> None:
    text = " ".join(w.text for w in nli_windows(guide["Retries"]))
    assert "within the read timeout:" in text
    assert "status=[429, 503]" not in text


def test_quote_markers_and_emphasis_are_removed(guide: dict[str, Chunk]) -> None:
    sentences = [s.text for s in prose_sentences(guide["Retries"])]
    assert "Note: a retried request is sent again from scratch." in sentences
    assert "Use bytes or a file object when you need retries." in sentences


def test_offsets_point_into_the_raw_chunk_text(guide: dict[str, Chunk]) -> None:
    chunk = guide["Retries"]
    for sentence in prose_sentences(chunk):
        raw = chunk.text[sentence.start : sentence.end]
        assert clean_markdown(raw) == sentence.text


def test_headings_are_not_prose() -> None:
    assert _sentences("Body text.") == ["Body text."]


def test_chunk_without_prose_has_no_windows() -> None:
    assert (
        nli_windows(_chunk("# A\n\n```python\nf()\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |\n")) == ()
    )


# --- sentence boundaries -----------------------------------------------------------------


def test_sentence_split() -> None:
    assert _sentences("One. Two! Three? Four") == ["One.", "Two!", "Three?", "Four"]


def test_abbreviations_and_decimals_do_not_end_a_sentence() -> None:
    text = "Use a factor, e.g. 0.5 here. The wait is approx. 1.5 s. Done."
    assert _sentences(text) == [
        "Use a factor, e.g. 0.5 here.",
        "The wait is approx. 1.5 s.",
        "Done.",
    ]


def test_lower_case_next_word_does_not_start_a_sentence() -> None:
    assert _sentences("Wait 2 s. or more. Then stop.") == ["Wait 2 s. or more.", "Then stop."]


def test_period_inside_inline_code_does_not_end_a_sentence() -> None:
    assert _sentences("Call `a. B()` first. Then go.") == ["Call a. B() first.", "Then go."]


def test_a_sentence_never_spans_two_list_items_or_paragraphs() -> None:
    assert _sentences("- first item\n- second item\n\nlast paragraph") == [
        "first item",
        "second item",
        "last paragraph",
    ]


def test_wrapped_sentence_becomes_one_line() -> None:
    assert _sentences("A long\nwrapped sentence.") == ["A long wrapped sentence."]


def test_links_and_images_keep_only_their_text() -> None:
    text = "See [the guide](https://x.org/g) and ![logo](l.png) or <https://x.org>."
    assert _sentences(text) == ["See the guide and logo or https://x.org."]


def test_link_with_code_as_its_text() -> None:
    assert _sentences("Build a [`Request`](../api.md#request) first.") == ["Build a Request first."]


# --- size and overlap --------------------------------------------------------------------


def test_windows_respect_the_size_limit(guide: dict[str, Chunk]) -> None:
    for chunk in guide.values():
        for window in _small(chunk):
            assert window.tokens <= 60 and not window.oversized


def test_windows_overlap_and_always_move_forward(guide: dict[str, Chunk]) -> None:
    windows = _small(guide["Migrating from 1.x"])
    assert len(windows) > 2
    for before, after in zip(windows, windows[1:], strict=False):
        assert after.start > before.start
        assert after.end > before.end
        assert after.start < before.end  # shares the last sentence(s) of the previous window


def test_every_sentence_is_in_some_window(guide: dict[str, Chunk]) -> None:
    for chunk in guide.values():
        covered = {s.start for w in _small(chunk) for s in w.sentences}
        assert covered == {s.start for s in prose_sentences(chunk)}


def test_one_sentence_over_the_limit_is_its_own_oversized_window() -> None:
    long = "Long " + "word " * 80
    windows = nli_windows(
        _chunk(f"# A\n\nShort one. {long}end. Short two."), max_tokens=60, overlap_tokens=10
    )
    assert [w.oversized for w in windows] == [False, True, False]


def test_overlap_must_be_smaller_than_the_window() -> None:
    with pytest.raises(ValueError):
        nli_windows(_chunk("# A\n\ntext\n"), max_tokens=50, overlap_tokens=50)


# --- citations --------------------------------------------------------------------------


def test_citation_found_across_a_line_wrap(guide: dict[str, Chunk]) -> None:
    chunk = guide["Timeouts"]
    span = find_citation(chunk.text, "for the connection and 30 seconds for the response")
    assert span is not None
    assert "\n" in chunk.text[span[0] : span[1]]


def test_citation_not_in_the_chunk_is_none(guide: dict[str, Chunk]) -> None:
    assert find_citation(guide["Timeouts"].text, "waits 15 seconds") is None
    assert find_citation(guide["Timeouts"].text, "   ") is None
