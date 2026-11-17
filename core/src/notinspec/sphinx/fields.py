"""API description fields (`field_list` in a `desc`) → one block per entry (SPEC §6.1).

The three XML shapes Sphinx produces for the same docstring field:

- **A** (reST or napoleon, several entries): `field_body > bullet_list > list_item > paragraph`
- **B** (reST or napoleon, one entry): `field_body > paragraph`
- **C** (numpydoc): `field_body > definition_list > definition_list_item`

In A and B the first `literal_strong` of the paragraph is the name (for Raises the exception,
possibly inside a `reference`), what follows up to the separator ` – ` (en dash) is the type,
without its parentheses, and the rest is the text. In C `term` is the name, `classifier` the
type and `definition` the text; a Returns / Yields term without a classifier is the type.
Nested paragraphs are joined with a blank line.

Each group of entries gets a label line (`**Parameters:**`, a `text` block) before its first
entry; the chunker keeps the two together. An entry is rendered as ``- `name` (type) – text``.
`Return type` and `Type` are not prose: one `signature` block (``Return type: `float` ``).
"""

import re
from collections.abc import Callable, Sequence
from xml.etree.ElementTree import Element

from notinspec.sphinx.inline import Context, Run, backticks, element_runs, render, text
from notinspec.sphinx.pieces import Piece, compose, prefixed, text_piece

type Atom = str | Element  # paragraph content in order: text, child, child's tail, ...
type Content = Callable[[Sequence[Atom]], list[Piece]]

FIELDS: dict[str, str] = {
    "parameters": "param",
    "keyword arguments": "param",
    "other parameters": "param",
    "attributes": "param",
    "returns": "returns",
    "yields": "returns",
    "raises": "raises",
    "warns": "raises",
    "return type": "return-type",
    "type": "type",
}
_TYPE_FIELDS = frozenset({"return-type", "type"})
_UNNAMED = frozenset({"returns"})  # numpydoc: a term without classifier is the type
_SEPARATOR = re.compile(r"\s–(?:\s|$)")  # U+2013 between the name/type and the text
_HEAD_TAGS = frozenset({"literal_strong", "literal_emphasis"})


def atoms(el: Element) -> list[Atom]:
    out: list[Atom] = [el.text] if el.text else []
    for child in el:
        out.append(child)
        if child.tail:
            out.append(child.tail)
    return out


def field_list(el: Element, ctx: Context, content: Content) -> list[Piece]:
    pieces: list[Piece] = []
    for item in el.findall("field"):
        label_el, body = item.find("field_name"), item.find("field_body")
        label = text(label_el) if label_el is not None else ""
        field = FIELDS.get(label.lower())
        if field is None:
            field = label.lower()
            ctx.warn(f"unknown field {label}")
        if body is None:
            continue
        if field in _TYPE_FIELDS:
            type_ = render([r for a in atoms(body) for r in _runs(a, ctx)], code=False)
            line = f"{label}: {backticks(type_)}" if type_ else f"{label}:"
            pieces.append(Piece("signature", [line], field=field, type=type_ or None))
            continue
        entries = list(_entries(body, field, ctx, content))
        if entries:
            pieces.append(text_piece(f"**{label}:**"))
            pieces.extend(entries)
    return pieces


def _entries(body: Element, field: str, ctx: Context, content: Content) -> list[Piece]:
    children = list(body)
    if not children:
        return []
    first = children[0].tag
    if first == "bullet_list":  # A
        out = []
        for list_item in children[0].findall("list_item"):
            out.append(_paragraph_entry(list(list_item), field, ctx, content))
        if len(children) > 1:  # text after the list: keep it with the last entry
            out.append(_entry(field, None, None, content(list(children[1:]))))
        return out
    if first == "paragraph":  # B
        return [_paragraph_entry(children, field, ctx, content)]
    if first == "definition_list":  # C
        out = []
        for child in children:
            if child.tag != "definition_list":
                out.append(_entry(field, None, None, content([child])))
                continue
            for item in child.findall("definition_list_item"):
                out.append(_definition_entry(item, field, ctx, content))
        return out
    return [_entry(field, None, None, content(list(children)))]


def _paragraph_entry(children: list[Element], field: str, ctx: Context, content: Content) -> Piece:
    """Shapes A and B: the head of the first paragraph is name and type, the rest is text."""
    if not children or children[0].tag != "paragraph":
        return _entry(field, None, None, content(list(children)))
    parts = atoms(children[0])
    rest: list[Atom] = list(children[1:])
    head, tail = _split_head(parts)
    if head is None:
        return _entry(field, None, None, content(parts + rest))
    name_el = next((a for a in head if isinstance(a, Element) and _strong(a) is not None), None)
    strong = _strong(name_el) if name_el is not None else None
    name = text(strong) if strong is not None else None
    type_runs = [r for a in head if a is not name_el for r in _runs(a, ctx)]
    type_ = _strip_parens(render(type_runs, code=False))
    return _entry(field, name or None, type_ or None, content(tail + rest))


def _split_head(parts: list[Atom]) -> tuple[list[Atom] | None, list[Atom]]:
    """(head, text) at the first separator. No head when it would not be a name or type."""
    for i, atom in enumerate(parts):
        if isinstance(atom, str) and (match := _SEPARATOR.search(atom)):
            head = [*parts[:i], atom[: match.start()]]
            if any(isinstance(a, Element) and _has_head_tag(a) for a in head):
                after = atom[match.end() :]
                return head, ([after] if after.strip() else []) + parts[i + 1 :]
            break
    first = next((a for a in parts if not (isinstance(a, str) and not a.strip())), None)
    if isinstance(first, Element) and _strong(first) is not None:
        # "`ValueError`" alone, or a parameter without a description
        if not any(isinstance(a, Element) and a.tag == "paragraph" for a in parts):
            return parts, []
    return None, parts


def _definition_entry(item: Element, field: str, ctx: Context, content: Content) -> Piece:
    """Shape C (numpydoc)."""
    term = item.find("term")
    term_text = render(_runs(term, ctx), code=False) if term is not None else ""
    classifiers = [render(_runs(c, ctx), code=False) for c in item.findall("classifier")]
    type_ = " : ".join(c for c in classifiers if c)
    name: str | None = term_text
    if field in _UNNAMED and not type_:
        name, type_ = None, term_text
    definition = item.find("definition")
    pieces = content(atoms(definition)) if definition is not None else []
    return _entry(field, name or None, type_ or None, pieces)


def _entry(field: str, name: str | None, type_: str | None, pieces: list[Piece]) -> Piece:
    head = backticks(name) if name else ""
    if type_:
        head = f"{head} ({type_})" if head else f"({type_})"
    if head:
        pieces = prefixed(f"{head} –", pieces) if pieces else [text_piece(head)]
    directives = [d for p in pieces for d in p.directives]  # deprecated parameter, ...
    lines, nested = compose(pieces, "- ", "  ")
    return Piece(
        "field", lines, name=name, field=field, type=type_, directives=directives, nested=nested
    )


def _runs(atom: Atom | Element, ctx: Context) -> list[Run]:
    if isinstance(atom, str):
        return [(False, atom)]
    if atom.tag in ("term", "classifier", "paragraph", "field_body"):
        out: list[Run] = [(False, atom.text)] if atom.text else []
        for child in atom:
            out.extend(_runs(child, ctx))
            if child.tail:
                out.append((False, child.tail))
        return out
    return element_runs(atom, ctx)


def _strong(el: Element) -> Element | None:
    return el if el.tag == "literal_strong" else el.find(".//literal_strong")


def _has_head_tag(el: Element) -> bool:
    return el.tag in _HEAD_TAGS or any(d.tag in _HEAD_TAGS for d in el.iter())


def _strip_parens(value: str) -> str:
    """ "(int, optional)" → "int, optional"; "(a) or (b)" stays as is."""
    value = value.strip()
    if not (value.startswith("(") and value.endswith(")")):
        return value
    depth = 0
    for i, char in enumerate(value):
        depth += {"(": 1, ")": -1}.get(char, 0)
        if depth == 0 and i < len(value) - 1:
            return value
    return value[1:-1].strip()
