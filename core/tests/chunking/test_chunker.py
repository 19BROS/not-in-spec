from collections.abc import Callable
from pathlib import Path

import pytest

from notinspec.chunking import (
    Chunk,
    Document,
    chunk_document,
    chunk_documents,
    load_documents,
    normalize_text,
)

Golden = Callable[[str, object], None]
FIXTURES = Path(__file__).parent / "fixtures"


def _doc(text: str, source: str = "docs/guide.md") -> Document:
    return Document(source, text)


def _chunks(text: str, **kwargs: int) -> tuple[Chunk, ...]:
    return chunk_document(_doc(text), **kwargs)


def _by_path(chunks: tuple[Chunk, ...]) -> dict[tuple[str, ...], Chunk]:
    return {c.heading_path: c for c in chunks}


@pytest.fixture
def client() -> tuple[Chunk, ...]:
    return chunk_documents(load_documents(FIXTURES, ["*.md"]))


# --- golden file and determinism -------------------------------------------------------


def test_client_golden(client: tuple[Chunk, ...], golden: Golden) -> None:
    golden("chunks-client", client)


def test_small_parts_golden(golden: Golden) -> None:
    chunks = chunk_documents(load_documents(FIXTURES, ["*.md"]), soft_limit=40)
    golden("chunks-client-soft40", chunks)


def test_same_input_same_chunks() -> None:
    text = (FIXTURES / "client.md").read_text(encoding="utf-8")
    assert _chunks(text) == _chunks(text)


def test_line_endings_bom_and_unicode_form_do_not_change_ids() -> None:
    nfc = "# Pripojenie\n\nČas v sekundách.  \n"
    nfd = "﻿# Pripojenie\r\n\r\nČas v sekundách.\r\n"
    assert [c.id for c in _chunks(nfc)] == [c.id for c in _chunks(nfd)]


# --- sections and headings -------------------------------------------------------------


def test_heading_paths_and_breadcrumbs(client: tuple[Chunk, ...]) -> None:
    assert [c.heading_path for c in client] == [
        (),
        ("Client", "Connecting"),
        ("Client", "Connecting", "Parameters"),
        ("Client", "Connecting", "Example"),
        ("Client", "Charges", "Example"),
        ("Client", "Errors"),
    ]
    assert client[1].breadcrumb == "client.md > Client > Connecting"
    assert client[0].breadcrumb == "client.md"


def test_text_before_first_heading_is_its_own_chunk(client: tuple[Chunk, ...]) -> None:
    intro = client[0]
    assert intro.heading_level == 0
    assert intro.text == "The Acme Python client wraps the Acme Payments REST API."


def test_heading_without_own_content_gives_no_chunk(client: tuple[Chunk, ...]) -> None:
    # "# Client" and "## Charges" go straight into a sub-heading
    paths = {c.heading_path for c in client}
    assert ("Client",) not in paths
    assert ("Client", "Charges") not in paths


def test_front_matter_is_skipped_and_line_numbers_still_match(client: tuple[Chunk, ...]) -> None:
    lines = (FIXTURES / "client.md").read_text(encoding="utf-8").split("\n")
    assert "sidebar_position" not in "".join(c.text for c in client)
    for chunk in client:
        assert chunk.text == "\n".join(lines[chunk.start_line - 1 : chunk.end_line])


def test_hash_inside_code_is_not_a_heading() -> None:
    chunks = _chunks("# A\n\n```python\n# not a heading\nx = 1\n```\n")
    assert [c.heading_path for c in chunks] == [("A",)]


def test_setext_heading_and_markdown_in_heading_text(client: tuple[Chunk, ...]) -> None:
    assert client[-1].heading_path == ("Client", "Errors")  # "Errors\n------" is an h2
    chunks = _chunks("# The `connect()` **method**\n\ntext\n")
    assert chunks[0].heading_path == ("The connect() method",)


def test_heading_inside_a_list_does_not_start_a_section() -> None:
    chunks = _chunks("# A\n\n- item\n\n  # still in the list\n")
    assert [c.heading_path for c in chunks] == [("A",)]


def test_skipped_heading_levels() -> None:
    chunks = _chunks("# A\n\n### C\n\ntext\n\n## B\n\ntext\n")
    assert [c.heading_path for c in chunks] == [("A", "C"), ("A", "B")]
    assert chunks[0].heading_level == 3


# --- blocks ----------------------------------------------------------------------------


def test_block_kinds(client: tuple[Chunk, ...]) -> None:
    by_path = _by_path(client)
    connecting = by_path[("Client", "Connecting")]
    assert [b.kind for b in connecting.blocks] == ["heading", "text", "text", "code"]
    code = connecting.blocks[-1]
    assert code.lang == "python"
    assert code.code is not None and code.code.startswith("# create a client")
    assert [b.kind for b in by_path[("Client", "Errors")].blocks] == ["heading", "text", "html"]


def test_code_inside_a_list_is_reported_as_nested(client: tuple[Chunk, ...]) -> None:
    example = _by_path(client)[("Client", "Connecting", "Example")]
    assert [(b.kind, b.nested, b.lang) for b in example.blocks] == [
        ("heading", False, None),
        ("list", False, None),
        ("code", True, "sh"),
    ]
    listing, nested = example.blocks[1], example.blocks[2]
    assert listing.start_line <= nested.start_line <= nested.end_line <= listing.end_line


def test_duplicate_heading_paths_get_an_occurrence_number() -> None:
    chunks = _chunks("# A\n\n## Example\n\none\n\n## Example\n\ntwo\n")
    assert [c.occurrence for c in chunks] == [0, 1]
    assert len({c.id for c in chunks}) == len({c.location_id for c in chunks}) == 2


# --- long sections ---------------------------------------------------------------------


def test_long_section_is_split_between_blocks() -> None:
    paragraphs = "\n\n".join(f"Paragraph {i} " + "word " * 20 for i in range(6))
    chunks = _chunks(f"# Long\n\n{paragraphs}\n", soft_limit=60)
    assert len(chunks) > 1
    assert [c.part for c in chunks] == list(range(1, len(chunks) + 1))
    assert {c.parts for c in chunks} == {len(chunks)}
    assert all(c.tokens <= 60 and not c.oversized for c in chunks)
    assert chunks[0].text.startswith("# Long")  # the heading stays with what follows it
    assert all(c.heading_path == ("Long",) for c in chunks)


def test_section_under_the_soft_limit_stays_whole() -> None:
    paragraphs = "\n\n".join(f"Paragraph {i} " + "word " * 100 for i in range(10))
    chunks = _chunks(f"# Guide\n\n{paragraphs}\n")  # ~1,000 tokens, default soft limit 2,000
    assert len(chunks) == 1
    assert chunks[0].parts == 1
    assert chunks[0].tokens > 1000


def test_parts_are_about_equal_not_full_plus_a_tiny_tail() -> None:
    paragraphs = "\n\n".join(f"Paragraph {i} " + "word " * 18 for i in range(11))
    chunks = _chunks(f"# Long\n\n{paragraphs}\n", soft_limit=200)  # ~225 tokens
    assert [c.parts for c in chunks] == [2, 2]
    sizes = [c.tokens for c in chunks]
    assert max(sizes) - min(sizes) <= 25  # greedy would give ~200 + ~25


def test_all_parts_of_a_section_share_the_section_id() -> None:
    paragraphs = "\n\n".join(f"Paragraph {i} " + "word " * 20 for i in range(6))
    chunks = _chunks(f"# Long\n\n{paragraphs}\n\n# Other\n\ntext\n", soft_limit=60)
    long = [c for c in chunks if c.heading_path == ("Long",)]
    assert len(long) > 1
    assert len({c.section_id for c in long}) == 1
    assert len({c.location_id for c in long}) == len(long)
    assert chunks[-1].section_id != long[0].section_id


def test_section_id_survives_text_edits() -> None:
    before = _chunks("# A\n\nold text\n")[0]
    after = _chunks("# A\n\nnew text\n")[0]
    assert before.section_id == after.section_id
    assert before.id != after.id


def test_code_block_is_never_cut() -> None:
    code = "\n".join(f"x{i} = {i}" for i in range(50))
    chunks = _chunks(f"# A\n\nintro\n\n```python\n{code}\n```\n\nafter\n", soft_limit=30)
    big = [c for c in chunks if any(b.kind == "code" for b in c.blocks)]
    assert len(big) == 1
    assert big[0].oversized
    assert big[0].blocks[-1].code == code + "\n"


def test_paragraph_stays_with_the_code_after_it() -> None:
    text = "# A\n\n" + "filler " * 25 + "\n\nExample:\n\n```python\nf(1)\n```\n"
    chunks = _chunks(text, soft_limit=30)
    with_code = next(c for c in chunks if any(b.kind == "code" for b in c.blocks))
    assert with_code.text.startswith("Example:")


def test_table_is_never_cut() -> None:
    rows = "\n".join(f"| p{i} | int | {i} |" for i in range(40))
    chunks = _chunks(f"# A\n\n| Name | Type | Default |\n|---|---|---|\n{rows}\n", soft_limit=50)
    tables = [b for c in chunks for b in c.blocks if b.kind == "table"]
    assert len(tables) == 1
    assert tables[0].end_line - tables[0].start_line + 1 == 42


# --- IDs -------------------------------------------------------------------------------


def test_editing_text_changes_id_but_not_location_id() -> None:
    before = _by_path(_chunks("# A\n\nold text\n\n# B\n\nsame\n"))
    after = _by_path(_chunks("# A\n\nnew text\n\n# B\n\nsame\n"))
    assert before[("A",)].id != after[("A",)].id
    assert before[("A",)].location_id == after[("A",)].location_id
    assert before[("A",)].content_hash != after[("A",)].content_hash
    assert before[("B",)].id == after[("B",)].id  # line numbers moved, nothing else did


def test_source_is_part_of_the_id() -> None:
    text = "# A\n\ntext\n"
    first = chunk_document(_doc(text, "a.md"))[0]
    second = chunk_document(_doc(text, "b.md"))[0]
    assert first.id != second.id
    assert first.content_hash == second.content_hash


# --- documents -------------------------------------------------------------------------


def test_load_documents_sorts_and_deduplicates(tmp_path: Path) -> None:
    (tmp_path / "docs" / "sub").mkdir(parents=True)
    (tmp_path / "docs" / "b.md").write_text("# B\n", encoding="utf-8")
    (tmp_path / "docs" / "sub" / "a.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "docs" / "notes.txt").write_text("skip", encoding="utf-8")
    (tmp_path / "docs" / "bad.md").write_bytes(b"# Bad \xff\n")
    docs = load_documents(tmp_path, ["docs/**/*.md", "docs/*.md"])
    assert [d.source for d in docs] == ["docs/b.md", "docs/bad.md", "docs/sub/a.md"]
    assert docs[1].text == "# Bad �\n"


def test_normalize_text_keeps_line_count() -> None:
    text = "a  \r\nb\rc\n"
    assert normalize_text(text) == "a\nb\nc\n"
    assert normalize_text(text).count("\n") == 3


def test_empty_document() -> None:
    assert _chunks("") == ()
    assert _chunks("---\ntitle: x\n---\n") == ()
