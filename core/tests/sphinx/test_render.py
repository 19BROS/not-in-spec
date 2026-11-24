from collections import Counter
from xml.etree import ElementTree as ET

from notinspec.chunking import BlockDocument, Chunk, approx_tokens, chunk_blocks, nli_windows
from notinspec.sphinx.render import render_document


def _render(body: str, warnings: Counter[str] | None = None) -> BlockDocument:
    root = ET.fromstring(f"<document>{body}</document>")
    return render_document(root, "page", Counter() if warnings is None else warnings, approx_tokens)


def _chunks(body: str, **kwargs: int) -> tuple[Chunk, ...]:
    return chunk_blocks(_render(body), project="lib", **kwargs)


def _section(title: str, body: str) -> str:
    return f"<section><title>{title}</title>{body}</section>"


def _desc(objtype: str, name: str, content: str = "", signature: str = "") -> str:
    sig = signature or f"<desc_name>{name}</desc_name>"
    return (
        f'<desc objtype="{objtype}"><desc_signature>{sig}</desc_signature>'
        f"<desc_content>{content}</desc_content></desc>"
    )


def _field(name: str, body: str) -> str:
    return f"<field><field_name>{name}</field_name><field_body>{body}</field_body></field>"


# --- inline -----------------------------------------------------------------------------------


def test_inline_code_links_and_whitespace() -> None:
    doc = _render(
        "<paragraph>Call <reference refuri='https://x.org/a'><literal>run()</literal></reference>"
        "  with\n   <emphasis>care</emphasis>, see [<footnote_reference>1</footnote_reference>]"
        "<index entries='x'/>.</paragraph>"
    )
    assert doc.text == "Call `run()` with care, see [[1]]."


def test_neighbouring_code_spans_merge() -> None:
    doc = _render(
        "<paragraph><literal_emphasis>async function</literal_emphasis>"
        "<literal_emphasis> or </literal_emphasis><literal_emphasis>None</literal_emphasis>"
        " and <literal>a`b</literal></paragraph>"
    )
    assert doc.text == "`async function or None` and ``a`b``"


# --- structure --------------------------------------------------------------------------------


def test_rubric_is_bold_text_not_a_heading() -> None:
    chunks = _chunks(_section("Guide", "<paragraph>A.</paragraph><rubric>Examples</rubric>"))
    assert [c.heading_path for c in chunks] == [("Guide",)]
    assert chunks[0].text == "# Guide\n\nA.\n\n**Examples**"


def test_desc_is_a_chunk_one_level_below_its_parent() -> None:
    method = _desc("method", "sleep", "<paragraph>Sleep.</paragraph>")
    attribute = _desc("attribute", "total", "<paragraph>Count.</paragraph>")
    cls = _desc("class", "Retry", f"<paragraph>Retry config.</paragraph>{method}{attribute}")
    chunks = _chunks(_section("API", _section("Utilities", cls)))
    assert [c.breadcrumb for c in chunks] == [
        "lib > API > Utilities > Retry",
        "lib > API > Utilities > Retry > sleep()",
        "lib > API > Utilities > Retry > total",
    ]
    assert [c.heading_level for c in chunks] == [3, 4, 4]
    assert chunks[0].text.endswith("Retry config.")  # the class keeps only its own text


def test_prose_after_a_desc_stays_in_the_section() -> None:
    body = _section(
        "Low-level",
        "<paragraph>Intro.</paragraph>"
        + _desc("function", "ping", "<paragraph>Ping.</paragraph>")
        + "<paragraph>After the function.</paragraph>"
        + _section("Details", "<paragraph>More.</paragraph>"),
    )
    chunks = _chunks(body)
    assert [c.heading_path for c in chunks] == [
        ("Low-level",),
        ("Low-level", "ping()"),
        ("Low-level", "Details"),
    ]
    assert chunks[0].text == "# Low-level\n\nIntro.\n\nAfter the function."


def test_signatures() -> None:
    signature = (
        "<desc_annotation>class </desc_annotation><desc_addname>urllib3.util.</desc_addname>"
        "<desc_name>Retry</desc_name><desc_parameterlist><desc_parameter>total=10</desc_parameter>"
        "<desc_parameter>*</desc_parameter><desc_parameter>read=None</desc_parameter>"
        "</desc_parameterlist><desc_returns>None</desc_returns>"
    )
    second = "<desc_signature><desc_name>Retry</desc_name><desc_parameterlist/></desc_signature>"
    desc = _desc("class", "Retry", signature=signature).replace(
        "</desc_signature>", f"</desc_signature>{second}", 1
    )
    chunk = _chunks(desc)[0]
    assert chunk.text == (
        "# Retry\n\n`class urllib3.util.Retry(total=10, *, read=None) -> None`\n\n`Retry()`"
    )
    assert [b.kind for b in chunk.blocks] == ["heading", "signature", "signature"]


def test_property_type_keeps_spaces_and_bare_text() -> None:
    """urllib3's `Timeout.connect_timeout: float | _TYPE_DEFAULT | None`: `_TYPE_DEFAULT` is
    not in a node of its own but the tail of a space node."""
    space = '<desc_sig_space classes="w"> </desc_sig_space>'
    bar = f"{space}<desc_sig_punctuation>|</desc_sig_punctuation>{space}"
    signature = (
        f"<desc_annotation>property{space}</desc_annotation>"
        "<desc_name>connect_timeout</desc_name>"
        f"<desc_annotation><desc_sig_punctuation>:</desc_sig_punctuation>{space}"
        f"<reference>float</reference>{bar}_TYPE_DEFAULT{bar}<reference>None</reference>"
        "</desc_annotation>"
    )
    chunk = _chunks(_desc("property", "connect_timeout", signature=signature))[0]
    (block,) = [b for b in chunk.blocks if b.kind == "signature"]
    assert block.type == "float | _TYPE_DEFAULT | None"


# --- fields -----------------------------------------------------------------------------------


def test_field_shapes_a_and_b() -> None:
    params = (
        "<bullet_list><list_item><paragraph><literal_strong>timeout</literal_strong> ("
        "<reference><literal_emphasis>float</literal_emphasis></reference><literal_emphasis>"
        " | None</literal_emphasis>) – Seconds.</paragraph></list_item>"
        "<list_item><paragraph><literal_strong>retries</literal_strong> – <paragraph>First."
        "</paragraph><literal_block language='python'>x = 1</literal_block><paragraph>Second."
        "</paragraph></paragraph></list_item></bullet_list>"
    )
    raises = (
        "<paragraph><reference><literal_strong>ValueError</literal_strong></reference>"
        " – if <literal>x</literal> – is bad.</paragraph>"
    )
    returns = "<paragraph>The time – in seconds.</paragraph>"
    rtype = "<paragraph><reference>float</reference></paragraph>"
    fields = "".join(
        [
            _field("Parameters", params),
            _field("Raises", raises),
            _field("Returns", returns),
            _field("Return type", rtype),
        ]
    )
    chunk = _chunks(_desc("function", "wait", f"<field_list>{fields}</field_list>"))[0]
    assert chunk.text == "\n\n".join(
        [
            "# wait()",
            "`wait`",
            "**Parameters:**",
            "- `timeout` (float | None) – Seconds.",
            "- `retries` – First.\n\n  ```python\n  x = 1\n  ```\n\n  Second.",
            "**Raises:**",
            "- `ValueError` – if `x` – is bad.",
            "**Returns:**",
            "- The time – in seconds.",  # no name or type before the dash: plain text
            "Return type: `float`",
        ]
    )
    fields_ = [(b.kind, b.field, b.name, b.type) for b in chunk.blocks if b.field]
    assert fields_ == [
        ("field", "param", "timeout", "float | None"),
        ("field", "param", "retries", None),
        ("field", "raises", "ValueError", None),
        ("field", "returns", None, None),
        ("signature", "return-type", None, "float"),
    ]
    code = [b for b in chunk.blocks if b.nested]
    assert [(b.kind, b.code) for b in code] == [("code", "x = 1")]


def test_field_shape_c() -> None:
    items = (
        "<definition_list><definition_list_item><term><strong>size</strong></term>"
        "<classifier>int, optional</classifier><definition><paragraph>Max.</paragraph>"
        "<paragraph>Positive.</paragraph></definition></definition_list_item></definition_list>"
    )
    returns = (
        "<definition_list><definition_list_item><term>bytes</term><definition><paragraph>Data."
        "</paragraph></definition></definition_list_item></definition_list>"
    )
    fields = _field("Parameters", items) + _field("Returns", returns) + _field("Notes", items)
    warnings: Counter[str] = Counter()
    doc = _render(_desc("function", "read", f"<field_list>{fields}</field_list>"), warnings)
    blocks = [p.block for p in doc.blocks if p.block.kind == "field"]
    assert [(b.field, b.name, b.type) for b in blocks] == [
        ("param", "size", "int, optional"),
        ("returns", None, "bytes"),
        ("notes", "size", "int, optional"),
    ]
    assert "- `size` (int, optional) – Max.\n\n  Positive." in doc.text
    assert "- (bytes) – Data." in doc.text
    assert warnings == Counter({"unknown field Notes": 1})


def test_field_label_stays_with_the_first_entry() -> None:
    entries = "".join(
        f"<list_item><paragraph><literal_strong>p{i}</literal_strong> – {'word ' * 20}"
        "</paragraph></list_item>"
        for i in range(4)
    )
    field = _field("Parameters", f"<bullet_list>{entries}</bullet_list>")
    chunks = _chunks(_desc("function", "f", f"<field_list>{field}</field_list>"), soft_limit=50)
    assert len(chunks) > 2
    for chunk in chunks:
        assert chunk.blocks[-1].kind != "text"  # never a label alone at the end of a part


def test_fields_and_admonitions_are_prose_signatures_are_not() -> None:
    field = _field(
        "Parameters", "<paragraph><literal_strong>x</literal_strong> – The value.</paragraph>"
    )
    content = f"<note><paragraph>Mind it.</paragraph></note><field_list>{field}</field_list>"
    chunk = _chunks(_desc("function", "f", content))[0]
    text = " ".join(w.text for w in nli_windows(chunk))
    assert text == "Note: Mind it. Parameters: x – The value."
    assert "f" not in text.split()


# --- other blocks -----------------------------------------------------------------------------


def test_lists_quotes_admonitions_and_nested_code() -> None:
    body = (
        "<bullet_list><list_item><paragraph>One.</paragraph><literal_block>x()</literal_block>"
        "</list_item><list_item><paragraph>Two.</paragraph><enumerated_list><list_item>"
        "<paragraph>Sub.</paragraph></list_item></enumerated_list></list_item></bullet_list>"
        "<block_quote><paragraph>Quoted.</paragraph></block_quote>"
        "<admonition><title>Heads up</title><paragraph>Careful.</paragraph></admonition>"
        "<seealso><paragraph>Other.</paragraph></seealso>"
        "<definition_list><definition_list_item><term>term:</term><definition><paragraph>Def."
        "</paragraph></definition></definition_list_item></definition_list>"
    )
    doc = _render(body)
    assert doc.text == (
        "- One.\n\n  ```\n  x()\n  ```\n- Two.\n\n  1. Sub.\n\n"
        "> Quoted.\n\nHeads up: Careful.\n\nSee also: Other.\n\n- term: Def."
    )
    kinds = [(p.block.kind, [(n.start_line, n.end_line) for n in p.nested]) for p in doc.blocks]
    assert kinds == [
        ("list", [(3, 5)]),
        ("quote", []),
        ("admonition", []),
        ("admonition", []),
        ("list", []),
    ]


def test_code_tables_footnotes_and_ignored_nodes() -> None:
    body = (
        "<container classes='literal-block-wrapper'><caption>Example <literal>a.py</literal>"
        "</caption><literal_block language='Python'>print(1)\n</literal_block></container>"
        "<doctest_block>&gt;&gt;&gt; 1\n1</doctest_block>"
        "<table><title>Limits</title><tgroup><thead><row><entry><paragraph>A</paragraph></entry>"
        "<entry><paragraph>B</paragraph></entry></row></thead><tbody><row><entry><paragraph>"
        "a|b</paragraph></entry></row></tbody></tgroup></table>"
        "<footnote><label>1</label><paragraph>Note text.</paragraph></footnote>"
        "<comment>hidden</comment><target refid='x'/><compound classes='toctree-wrapper'>"
        "<paragraph>toc</paragraph></compound><meta content='x'/>"
    )
    doc = _render(body)
    assert doc.text == (
        "Example `a.py`\n```python\nprint(1)\n```\n\n```pycon\n>>> 1\n1\n```\n\n"
        "Limits\n| A | B |\n| --- | --- |\n| a\\|b |  |\n\n[1] Note text."
    )
    assert [p.block.lang for p in doc.blocks[:2]] == ["python", "pycon"]
    assert doc.blocks[0].block.code == "print(1)\n"


def test_unknown_nodes_keep_their_text_with_a_warning() -> None:
    warnings: Counter[str] = Counter()
    doc = _render(
        "<sd_card><paragraph>Inside.</paragraph></sd_card><paragraph>A <kbd>Ctrl</kbd>"
        "<problematic>`x`_</problematic>.</paragraph><sd_card><paragraph>Two.</paragraph></sd_card>",
        warnings,
    )
    assert doc.text == "Inside.\n\nA Ctrl`x`_.\n\nTwo."
    assert warnings == Counter(
        {"unknown node sd_card": 2, "unknown node kbd": 1, "unresolved markup in page": 1}
    )
