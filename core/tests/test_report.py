import re
from dataclasses import replace

from notinspec.chunking import Block, Document, chunk_documents
from notinspec.ingestion import INGESTION_SCHEMA_VERSION, Ingestion, InputFile, SphinxInput
from notinspec.inventory import (
    INVENTORY_BUILDER_VERSION,
    Change,
    Conflict,
    Inventory,
    Signature,
    Source,
    Symbol,
    build_inventory,
)
from notinspec.report import render_report

GUIDE = """\
# Guide `<b>`

Intro with <script>alert(1)</script> & more.

## Install

```python
x = "<img src=x onerror=alert(1)>"
```

## Use

Text.
"""


def ingestion(documents: list[Document], warnings: tuple[str, ...] = ()) -> Ingestion:
    chunks = chunk_documents(documents, project="<proj>", soft_limit=2000)
    return Ingestion(
        schema_version=INGESTION_SCHEMA_VERSION,
        config_hash="c" * 64,
        input_hash="a" * 64,
        project="<proj>",
        chunker_version=3,
        soft_limit=2000,
        sphinx=None,
        files=tuple(InputFile(d.source, "markdown", "0" * 64) for d in documents),
        chunks=chunks,
        openapi=(),
        inventory_builder_version=INVENTORY_BUILDER_VERSION,
        inventory=build_inventory(chunks).inventory,
        conflicts=(),
        warnings=warnings,
    )


def test_all_input_text_is_escaped_and_there_is_no_script() -> None:
    report = render_report(
        ingestion(
            [Document("docs/<x>.md", GUIDE)],
            warnings=("<script>bad()</script>",),
        )
    )
    assert re.search(r"<script|<img|<b>|<x>|<proj>", report) is None
    assert "&lt;script&gt;alert(1)&lt;/script&gt; &amp; more" in report
    assert "&lt;proj&gt; &gt; Guide &lt;b&gt; &gt; Install" in report
    assert "docs/&lt;x&gt;.md" in report
    assert not re.search(r"(src|href)=['\"]?(https?:)?//", report)  # nothing external


def test_every_chunk_is_shown_grouped_by_document() -> None:
    data = ingestion([Document("b.md", GUIDE), Document("a.md", "# A\n\nText of A.\n")])
    report = render_report(data)
    assert len(data.chunks) == 4
    for chunk in data.chunks:
        assert f"id='c-{chunk.id}'" in report
    # document order follows the chunks, not the alphabet
    assert report.index("<h2 id=d1>b.md</h2>") < report.index("<h2 id=d2>a.md</h2>")
    assert "heading 1 · code 1" in report  # block-kind counts of "Install"
    assert "part 1/1" in report
    assert "<tr><th>documents with chunks<td>2" in report


def test_warnings_show_count_and_unknown_nodes_first() -> None:
    report = render_report(
        ingestion(
            [Document("a.md", "Text.\n")],
            warnings=(
                "a problem",
                "xml: unknown node sd_foo (3x)",
                "xml: unresolved markup in api (2x)",
            ),
        )
    )
    rows = re.findall(r"<tr><td>(.*?)<td>(\d+)", report)
    assert rows == [
        ("xml: unknown node sd_foo", "3"),
        ("a problem", "1"),
        ("xml: unresolved markup in api", "2"),
    ]


def test_oversized_chunk_is_marked_and_empty_input_is_explained() -> None:
    documents = [Document("big.md", "# Big\n\n" + "word " * 3000 + "\n")]
    chunks = chunk_documents(documents, project="p", soft_limit=100)
    assert any(c.oversized for c in chunks)
    data = replace(ingestion(documents), soft_limit=100, chunks=chunks)
    report = render_report(data)
    assert "<span class=over>oversized</span>" in report
    assert "<h2>Warnings</h2><p>None.</p>" in report
    assert "No chunks." in render_report(replace(data, chunks=()))


def test_sphinx_version_and_field_table() -> None:
    data = ingestion([Document("api.md", "# Retry\n\nText.\n")])
    (chunk,) = data.chunks
    fields = (
        Block("field", 3, 3, 5, name="<total>", field="param", type="int | None"),
        Block("field", 4, 4, 5, field="returns"),
        Block("signature", 5, 5, 2, field="return-type"),
    )
    chunk = replace(chunk, blocks=chunk.blocks + fields)
    report = render_report(replace(data, chunks=(chunk,), sphinx=SphinxInput("9.1.1", 1)))
    assert "<tr><th>Sphinx<td>9.1.1 (reader v1)" in report
    assert "<tr><td>param<td>&lt;total&gt;<td>int | None<td>field" in report
    assert "<tr><td>returns<td><td><td>field" in report
    assert "<tr><td>return-type<td><td><td>signature" in report
    assert "field 2 · signature 1" in report
    assert "Sphinx" not in render_report(data).split("<h2>")[0]


def test_inventory_section_links_to_chunks_and_escapes() -> None:
    data = ingestion([Document("api.md", "# Retry\n\nText.\n")])
    (chunk,) = data.chunks
    source = (Source("signature", section_id=chunk.section_id),)
    symbol = Symbol(
        "pkg.<b>", "function", source, (Signature((), source, text="pkg.<b>() -> <i>"),)
    )
    change = Change("pkg.<b>", "deprecated", "2.0", source, replacement="pkg.<new>")
    conflict = Conflict(
        "pkg.<b>", "kind", "function", "<m>", (Source("changelog", section_id="x"),)
    )
    report = render_report(
        replace(data, inventory=Inventory((symbol,), (change,)), conflicts=(conflict,))
    )
    assert "<tr><th>inventory symbols<td>1" in report
    assert "<h3>Changes (1)</h3>" in report and "<td>pkg.&lt;new&gt;" in report
    assert f"<a href='#c-{chunk.id}'>signature</a>" in report
    assert "<td>&lt;m&gt;<td>changelog" in report  # a section that is no chunk: no link
    assert "<code>pkg.&lt;b&gt;() -&gt; &lt;i&gt;</code>" in report
    assert "<b>" not in report and "<i>" not in report and "<m>" not in report
    assert "No API descriptions." in render_report(data)
