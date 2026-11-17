"""Sphinx doctree → typed blocks, straight from the nodes (SPEC §6.1).

No XML → Markdown → parser round trip: it would lose node types, break on text that looks like
Markdown and could not express one block per parameter. The text built here is Markdown-like
and read-only (for display and citations); block line ranges point into it.

Structure:

- `section` + `title` → `heading`, level = depth (`#` × level, at most 6 shown).
- `desc` (any domain and object type) → `heading` one level below its parent; the title is the
  `desc_name` of the first signature, plus `()` for functions, methods and decorators. Each
  `desc_signature` → one `signature` block (the whole signature in backticks, one line).
  `desc_content` is transparent.
- **Order inside a section or `desc_content`:** first all its own body content in document
  order, then nested `desc`s, then subsections. Prose that follows a `desc` in the source
  stays in the section's own chunk instead of being attached to the last API description.

Body nodes:

| Node | Block |
|---|---|
| `paragraph`, `compact_paragraph`, `versionmodified` | `text` |
| `bullet_list`, `enumerated_list`, `definition_list`, `glossary` | `list` (never cut), `- ` items |
| `literal_block`, `doctest_block` (`pycon`), `math_block` (`math`) | `code`, fenced, text as is |
| `container.literal-block-wrapper` | one `code` block, the `caption` above the fence |
| other `container`s (`sd-tab-*`, ...) | transparent |
| `rubric` | `text` in bold: never a heading, never starts a section |
| `note`, `warning`, `seealso`, ..., generic `admonition` | `admonition` (`Note: ...`) |
| `block_quote` | `quote` (`> `) |
| `table`, `autosummary_table` | `table` (pipe table, never cut) |
| `footnote`, `citation` | `text` (`[label] text`) |
| `field_list` in a `desc` | one block per entry (`fields.py`); elsewhere a `list` |
| `index`, `target`, `comment`, `meta`, `image`, `raw`, ... (`_IGNORED`) | ignored |
| toctree `compound` and `compact_paragraph` | ignored (navigation, not content) |
| anything else | its children (or its text) with a warning `unknown node <tag>` |

Code inside a list, quote, admonition or field entry is part of that block and is also
recorded as a nested `code` block, so NLI windows leave it out.
"""

import unicodedata
from collections import Counter
from collections.abc import Callable, Sequence
from xml.etree.ElementTree import Element

from notinspec.chunking import Block, BlockDocument, BlockKind, ParsedBlock
from notinspec.sphinx import fields
from notinspec.sphinx.fields import Atom, atoms
from notinspec.sphinx.inline import (
    CODE_TAGS,
    SKIP_TAGS,
    TEXT_TAGS,
    Context,
    Run,
    backticks,
    collapse,
    element_runs,
    inline,
    render,
    text,
)
from notinspec.sphinx.pieces import Nested, Piece, code_piece, compose, prefixed, text_piece

_INLINE = (
    CODE_TAGS | TEXT_TAGS | SKIP_TAGS | {"footnote_reference", "citation_reference", "problematic"}
)
_IGNORED = frozenset(
    {
        "index",
        "target",
        "comment",
        "meta",
        "substitution_definition",
        "autosummary_toc",
        "tabular_col_spec",
        "image",
        "raw",
        "label",
        "colspec",
    }
)
_ADMONITIONS = {
    "note": "Note",
    "warning": "Warning",
    "caution": "Caution",
    "attention": "Attention",
    "tip": "Tip",
    "important": "Important",
    "hint": "Hint",
    "danger": "Danger",
    "error": "Error",
    "seealso": "See also",
    "admonition": "",  # generic: its own title
}
_CALLABLE = frozenset({"function", "method", "classmethod", "staticmethod", "decorator"})


def render_document(
    root: Element, docname: str, warnings: Counter[str], count_tokens: Callable[[str], int]
) -> BlockDocument:
    """Blocks of one `<document>`. Pure apart from adding to `warnings`."""
    renderer = _Renderer(Context(docname, warnings))
    return _layout(docname, renderer.ordered(list(root), 0), count_tokens)


class _Renderer:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.in_desc = 0

    # --- structure ---------------------------------------------------------------------

    def ordered(self, children: list[Element], level: int) -> list[Piece]:
        """Own body content first, then nested `desc`s, then subsections."""
        body = [c for c in children if c.tag not in ("desc", "section", "title")]
        out = self.content(body, level)
        for child in children:
            if child.tag == "desc":
                out += self.desc(child, level + 1)
        for child in children:
            if child.tag == "section":
                out += self.section(child, level + 1)
        return out

    def section(self, el: Element, level: int) -> list[Piece]:
        title = el.find("title")
        out = [self.heading(level, title)] if title is not None else []
        return out + self.ordered(list(el), level)

    def heading(self, level: int, title: Element) -> Piece:
        line = inline(title, self.ctx)
        plain = inline(title, self.ctx, code=False)
        return Piece("heading", [f"{'#' * min(level, 6)} {line}"], heading=(level, plain))

    def desc(self, el: Element, level: int) -> list[Piece]:
        signatures = el.findall("desc_signature")
        name = signatures[0].find("desc_name") if signatures else None
        title = text(name) if name is not None else ""
        if not title:
            title = _signature(signatures[0]) if signatures else el.get("objtype", "")
        if el.get("objtype") in _CALLABLE:
            title += "()"
        out = [Piece("heading", [f"{'#' * min(level, 6)} {title}"], heading=(level, title))]
        out += [Piece("signature", [backticks(_signature(s))]) for s in signatures]
        content = el.find("desc_content")
        if content is not None:
            self.in_desc += 1
            out += self.ordered(list(content), level)  # nested descs: level + 1
            self.in_desc -= 1
        return out

    # --- body --------------------------------------------------------------------------

    def content(self, items: Sequence[Atom], level: int) -> list[Piece]:
        """Mixed content: text and inline nodes become paragraphs, block nodes blocks."""
        out: list[Piece] = []
        buffer: list[Run] = []

        def flush() -> None:
            line = render(buffer)
            if line:
                out.append(text_piece(line))
            buffer.clear()

        for item in items:
            if isinstance(item, str):
                buffer.append((False, item))
            elif _is_inline(item):
                buffer.extend(element_runs(item, self.ctx))
            else:
                flush()
                out += self.block(item, level)
        flush()
        return out

    def children(self, el: Element, level: int, skip: tuple[str, ...] = ()) -> list[Piece]:
        return self.content([a for a in atoms(el) if not _tagged(a, skip)], level)

    def block(self, el: Element, level: int) -> list[Piece]:
        tag = el.tag
        if tag in _IGNORED:
            return []
        if tag in ("paragraph", "compact_paragraph", "versionmodified", "glossary"):
            if el.get("toctree") == "1":
                return []
            return self.children(el, level)
        if tag == "section":
            return self.section(el, level + 1)
        if tag == "desc":
            return self.desc(el, level + 1)
        if tag in ("bullet_list", "enumerated_list"):
            return self.bullets(el, level)
        if tag == "definition_list":
            return self.definition_list(el, level)
        if tag == "field_list":
            if self.in_desc:
                return fields.field_list(el, self.ctx, lambda a: self.content(a, level))
            return self.field_list(el, level)
        if tag == "literal_block":
            return [code_piece("".join(el.itertext()), _lang(el.get("language")))]
        if tag == "doctest_block":
            return [code_piece("".join(el.itertext()), "pycon")]
        if tag == "math_block":
            return [code_piece("".join(el.itertext()), "math")]
        if tag == "container":
            return self.container(el, level)
        if tag == "rubric":
            line = inline(el, self.ctx)
            return [text_piece(f"**{line}**")] if line else []
        if tag in _ADMONITIONS:
            return self.admonition(el, level)
        if tag == "block_quote":
            return self.quote(el, level)
        if tag == "autosummary_table":
            return [p for t in el.findall("table") for p in self.table(t, level)]
        if tag == "table":
            return self.table(el, level)
        if tag in ("footnote", "citation"):
            label = el.find("label")
            pieces = self.children(el, level, skip=("label",))
            mark = f"[{text(label)}]" if label is not None else ""
            return [_merge("text", prefixed(mark, pieces) if mark else pieces)]
        if tag == "compound":
            return (
                []
                if "toctree-wrapper" in el.get("classes", "").split()
                else self.children(el, level)
            )
        if tag in ("title", "caption", "attribution"):
            line = inline(el, self.ctx)
            return [text_piece(line)] if line else []
        self.ctx.unknown(tag)
        if len(el):
            return self.children(el, level)
        line = inline(el, self.ctx)
        return [text_piece(line)] if line else []

    def container(self, el: Element, level: int) -> list[Piece]:
        if "literal-block-wrapper" not in el.get("classes", "").split():
            return self.children(el, level)
        caption = el.find("caption")
        code = el.find("literal_block")
        if code is None:
            return self.children(el, level)
        label = inline(caption, self.ctx) if caption is not None else None
        return [code_piece("".join(code.itertext()), _lang(code.get("language")), label)]

    def bullets(self, el: Element, level: int) -> list[Piece]:
        try:
            number = int(el.get("start", "1"))
        except ValueError:
            number = 1
        items: list[tuple[list[str], list[Nested]]] = []
        for i, item in enumerate(el.findall("list_item")):
            marker = "- " if el.tag == "bullet_list" else f"{number + i}. "
            items.append(compose(self.children(item, level), marker, " " * len(marker)))
        return [_join("list", items)] if items else []

    def definition_list(self, el: Element, level: int) -> list[Piece]:
        items = []
        for item in el.findall("definition_list_item"):
            term = item.find("term")
            head = inline(term, self.ctx) if term is not None else ""
            for classifier in item.findall("classifier"):
                head += f" ({inline(classifier, self.ctx)})"
            definition = item.find("definition")
            pieces = self.children(definition, level) if definition is not None else []
            items.append(compose(_labelled(head, pieces), "- ", "  "))
        return [_join("list", items)] if items else []

    def field_list(self, el: Element, level: int) -> list[Piece]:
        """A field list outside an API description (rare): a plain list."""
        items = []
        for item in el.findall("field"):
            name, body = item.find("field_name"), item.find("field_body")
            head = inline(name, self.ctx) if name is not None else ""
            pieces = self.children(body, level) if body is not None else []
            items.append(compose(_labelled(head, pieces), "- ", "  "))
        return [_join("list", items)] if items else []

    def admonition(self, el: Element, level: int) -> list[Piece]:
        label = _ADMONITIONS[el.tag]
        title = el.find("title")
        if not label:
            label = inline(title, self.ctx) if title is not None else "Note"
        pieces = self.children(el, level, skip=("title",) if el.tag == "admonition" else ())
        return [_merge("admonition", prefixed(f"{label}:", pieces))]

    def quote(self, el: Element, level: int) -> list[Piece]:
        lines, nested = compose(self.children(el, level))
        quoted = [f"> {line}" if line else ">" for line in lines]
        return [Piece("quote", quoted, nested=nested)]

    def table(self, el: Element, level: int) -> list[Piece]:
        head: list[list[str]] = []
        body: list[list[str]] = []
        for tgroup in el.findall("tgroup"):
            for part, rows in (("thead", head), ("tbody", body)):
                for section in tgroup.findall(part):
                    rows += [self.row(r, level) for r in section.findall("row")]
        rows = head + body
        if not rows:
            return []
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        lines = [_row(rows[0]), _row(["---"] * width), *(_row(r) for r in rows[1:])]
        title = el.find("title")
        caption = inline(title, self.ctx) if title is not None else ""
        return [Piece("table", [caption, *lines] if caption else lines)]

    def row(self, row: Element, level: int) -> list[str]:
        cells = []
        for entry in row.findall("entry"):
            pieces = self.children(entry, level)
            words = " ".join(line.strip() for p in pieces for line in p.lines if line.strip())
            cells.append(words.replace("|", "\\|"))
        return cells


def _signature(sig: Element) -> str:
    """`desc_signature` → one line: `trio.run(async_fn, *args, clock=None) -> RetT`."""
    parts: list[str] = []
    for child in sig:
        if child.tag == "desc_parameterlist":
            params = ", ".join(collapse("".join(p.itertext())) for p in child)
            parts.append(f"({params})")
        elif child.tag == "desc_returns":
            parts.append(f" -> {text(child)}")
        elif child.tag not in _IGNORED:
            parts.append("".join(child.itertext()))
    return collapse("".join(parts))


def _is_inline(el: Element) -> bool:
    if el.tag in _INLINE or el.tag.startswith("desc_sig"):
        return True
    known = el.tag in _IGNORED or el.tag in _BLOCK_TAGS
    return not known and len(el) == 0  # unknown leaf: its text inline (warned)


_BLOCK_TAGS = frozenset(
    {
        "paragraph",
        "compact_paragraph",
        "versionmodified",
        "glossary",
        "section",
        "desc",
        "bullet_list",
        "enumerated_list",
        "definition_list",
        "field_list",
        "literal_block",
        "doctest_block",
        "math_block",
        "container",
        "rubric",
        "block_quote",
        "autosummary_table",
        "table",
        "footnote",
        "citation",
        "compound",
        "title",
        "caption",
        "attribution",
        *_ADMONITIONS,
    }
)


def _tagged(atom: Atom, tags: tuple[str, ...]) -> bool:
    return not isinstance(atom, str) and atom.tag in tags


def _labelled(head: str, pieces: list[Piece]) -> list[Piece]:
    """`term: definition` on one line when the definition starts with a paragraph."""
    if not head:
        return pieces
    if not pieces:
        return [text_piece(head)]
    return prefixed(head if head.endswith(":") else f"{head}:", pieces)


def _merge(kind: BlockKind, pieces: list[Piece]) -> Piece:
    lines, nested = compose(pieces)
    return Piece(kind, lines, nested=nested)


def _join(kind: BlockKind, items: list[tuple[list[str], list[Nested]]]) -> Piece:
    lines: list[str] = []
    nested: list[Nested] = []
    for item_lines, item_nested in items:
        offset = len(lines)
        lines += item_lines
        nested += [Nested(n.start + offset, n.end + offset, n.lang, n.code) for n in item_nested]
    return Piece(kind, lines, nested=nested)


def _row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def _lang(value: str | None) -> str | None:
    return value.lower() if value else None


def _layout(docname: str, pieces: list[Piece], count_tokens: Callable[[str], int]) -> BlockDocument:
    """Number the lines: one blank line between blocks, NFC, no trailing whitespace."""
    lines: list[str] = []
    blocks: list[ParsedBlock] = []
    for piece in pieces:
        if not piece.lines or not any(line.strip() for line in piece.lines):
            continue
        if lines:
            lines.append("")
        start = len(lines) + 1
        own = [_nfc(line).rstrip() for line in piece.lines]
        lines += own
        block = Block(
            kind=piece.kind,
            start_line=start,
            end_line=len(lines),
            tokens=count_tokens("\n".join(own)),
            lang=piece.lang,
            code=piece.code,
            name=_nfc_or_none(piece.name),
            field=piece.field,
            type=_nfc_or_none(piece.type),
        )
        nested = tuple(
            Block(
                kind="code",
                start_line=start + n.start,
                end_line=start + n.end,
                tokens=count_tokens("\n".join(own[n.start : n.end + 1])),
                lang=n.lang,
                code=n.code,
                nested=True,
            )
            for n in piece.nested
        )
        heading = (piece.heading[0], _nfc(piece.heading[1])) if piece.heading else None
        blocks.append(ParsedBlock(block, heading, nested))
    return BlockDocument(docname, "\n".join(lines), tuple(blocks))


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def _nfc_or_none(value: str | None) -> str | None:
    return _nfc(value) if value is not None else None
