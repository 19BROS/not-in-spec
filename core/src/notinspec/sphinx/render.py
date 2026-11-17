"""Sphinx doctree → typed blocks, straight from the nodes (SPEC §6.1).

No XML → Markdown → parser round trip: it would lose node types, break on text that looks like
Markdown and could not express one block per parameter. The text built here is Markdown-like
and read-only (for display and citations); block line ranges point into it.

Structure:

- `section` + `title` → `heading`, level = depth (`#` × level, at most 6 shown).
- `desc` (any domain and object type) → `heading` one level below its parent; the title is the
  `desc_name` of the first signature, plus `()` for functions, methods and decorators. Each
  `desc_signature` → one `signature` block (the whole signature in backticks, one line).
  The block also carries the signature as data, input for the inventory (SPEC §6.3):
  `name` = qualified path (`module` + `fullname`), `objtype` = domain + object type
  (`py:method`), `parameters` from the `desc_parameter` node types (name with `*` / `**`,
  annotation, default; `*` and `/` separators as their own entries), `type` = `-> X` or the
  `: X` of an attribute.
  `desc_content` is transparent.
- **Order inside a section or `desc_content`:** first all its own body content in document
  order, then nested `desc`s, then subsections. Prose that follows a `desc` in the source
  stays in the section's own chunk instead of being attached to the last API description.

Body nodes:

| Node | Block |
|---|---|
| `paragraph`, `compact_paragraph` | `text` |
| `versionmodified` (`deprecated`, `versionadded`, ...) | `text` + `directives` (below) |
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

Version directives (`versionmodified`) are prose, and their first block also keeps the
directive's `(type, version)` in `Block.directives`, input for `Change` (SPEC §6.3). Inside a
parameter entry, the `field` block keeps it.

Code inside a list, quote, admonition or field entry is part of that block and is also
recorded as a nested `code` block, so NLI windows leave it out.
"""

import keyword
import unicodedata
from collections import Counter
from collections.abc import Callable, Iterator, Sequence
from xml.etree.ElementTree import Element

from notinspec.chunking import Block, BlockDocument, BlockKind, ParsedBlock, SignatureParameter
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
from notinspec.sphinx.pieces import (
    Composed,
    Nested,
    Piece,
    code_piece,
    compose,
    prefixed,
    text_piece,
)

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
        objtype = ":".join(filter(None, (el.get("domain"), el.get("objtype")))) or None
        out += [_signature_piece(s, objtype) for s in signatures]
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
        if tag == "versionmodified":
            return self.version_modified(el, level)
        if tag in ("paragraph", "compact_paragraph", "glossary"):
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

    def version_modified(self, el: Element, level: int) -> list[Piece]:
        """`deprecated`, `versionadded`, ...: prose, and its first block keeps type and version."""
        pieces = self.children(el, level)
        type_, version = el.get("type"), el.get("version")
        if pieces and type_ and version:
            pieces[0].directives.append((type_, version))
        return pieces

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
        items: list[Composed] = []
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
        lines, nested, directives = compose(self.children(el, level))
        quoted = [f"> {line}" if line else ">" for line in lines]
        return [Piece("quote", quoted, nested=nested, directives=directives)]

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


def _signature_piece(sig: Element, objtype: str | None) -> Piece:
    """One `desc_signature`: the line to show, plus its path, parameters and type as data."""
    params = sig.find("desc_parameterlist")
    return Piece(
        "signature",
        [backticks(_signature(sig))],
        name=_path(sig),
        type=_signature_type(sig),
        objtype=objtype,
        parameters=None if params is None else tuple(_parameters(params, optional=False)),
    )


def _path(sig: Element) -> str | None:
    """Qualified name: `module` + `fullname` (Python domain), else the first id, else the name.

    `ids` is no fallback for Python: overloads have none and some are slugified. Without a
    current module Sphinx 9 writes `module="True"`, so only a dotted Python name counts.
    """
    fullname, module = sig.get("fullname"), sig.get("module")
    if fullname:
        return f"{module}.{fullname}" if module and _module_name(module) else fullname
    ids = sig.get("ids", "").split()
    if ids:
        return ids[0]
    name = sig.find("desc_name")
    return text(name) or None if name is not None else None


def _module_name(value: str) -> bool:
    return all(part.isidentifier() and not keyword.iskeyword(part) for part in value.split("."))


def _signature_type(sig: Element) -> str | None:
    """`-> X` of a callable, or `: X` of an attribute or property."""
    returns = sig.find("desc_returns")
    if returns is not None:
        return text(returns) or None
    for annotation in sig.findall("desc_annotation"):
        children = [c for c in annotation if c.tag != "desc_sig_space"]
        if children and children[0].tag == "desc_sig_punctuation" and text(children[0]) == ":":
            return collapse("".join(text(c) for c in children[1:])) or None
    return None


def _parameters(params: Element, *, optional: bool) -> Iterator[SignatureParameter]:
    """Children of a parameter list. `desc_optional` (`compile(source[, filename])`, used for
    signatures that are not valid Python) is walked into; what is inside it is optional."""
    for child in params:
        if child.tag == "desc_optional":
            yield from _parameters(child, optional=True)
        elif child.tag == "desc_parameter":
            yield _parameter(child, optional=optional)


def _parameter(param: Element, *, optional: bool = False) -> SignatureParameter:
    """`desc_parameter` → name (with `*` / `**`), annotation and default, from the node types."""
    prefix, name = "", None
    annotation: list[str] = []
    default: str | None = None
    part = "name"  # name → annotation (after ":") → default (after "=")
    for child in param:
        value = "".join(child.itertext())
        if child.tag == "desc_sig_operator" and value in ("*", "**", "/") and name is None:
            prefix += value
        elif child.tag == "desc_sig_name" and name is None:
            name = value
        elif child.tag == "desc_sig_punctuation" and value == ":" and part == "name":
            part = "annotation"
        elif child.tag == "desc_sig_operator" and value == "=" and part != "default":
            part = "default"
        elif "default_value" in child.get("classes", "").split():
            default = collapse(value)
        elif part == "annotation":
            annotation.append(value)
    if name is None:
        return SignatureParameter(prefix or collapse("".join(param.itertext())), optional=optional)
    annotated = collapse("".join(annotation)) or None
    return SignatureParameter(prefix + name, annotated, default, optional=optional)


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
    lines, nested, directives = compose(pieces)
    return Piece(kind, lines, nested=nested, directives=directives)


def _join(kind: BlockKind, items: list[Composed]) -> Piece:
    lines: list[str] = []
    nested: list[Nested] = []
    directives: list[tuple[str, str]] = []
    for item in items:
        offset = len(lines)
        lines += item.lines
        nested += [Nested(n.start + offset, n.end + offset, n.lang, n.code) for n in item.nested]
        directives += item.directives
    return Piece(kind, lines, nested=nested, directives=directives)


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
            objtype=piece.objtype,
            parameters=_nfc_parameters(piece.parameters),
            directives=tuple(piece.directives),
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


def _nfc_parameters(
    parameters: tuple[SignatureParameter, ...] | None,
) -> tuple[SignatureParameter, ...] | None:
    if parameters is None:
        return None
    return tuple(
        SignatureParameter(
            _nfc(p.name), _nfc_or_none(p.annotation), _nfc_or_none(p.default), p.optional
        )
        for p in parameters
    )
