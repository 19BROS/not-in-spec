"""Rendered pieces: the lines of one future `Block`, before they get line numbers.

A piece is one block of the document (heading, paragraph, list, code, field entry, ...).
Composite blocks (a list item, an admonition, a quote) are built from the pieces of their
children; code inside them is remembered as `Nested`, so NLI windows can leave it out.
"""

import dataclasses
from dataclasses import dataclass

from notinspec.chunking import BlockKind, SignatureParameter, normalize_text


@dataclass(frozen=True)
class Nested:
    start: int  # 0-based line index into the piece's lines, inclusive
    end: int  # inclusive
    lang: str | None
    code: str


@dataclass
class Piece:
    kind: BlockKind
    lines: list[str]
    heading: tuple[int, str] | None = None
    lang: str | None = None
    code: str | None = None
    name: str | None = None
    field: str | None = None
    type: str | None = None
    objtype: str | None = None
    parameters: tuple[SignatureParameter, ...] | None = None
    directives: list[tuple[str, str]] = dataclasses.field(default_factory=list)
    nested: list[Nested] = dataclasses.field(default_factory=list)


def text_piece(line: str) -> Piece:
    return Piece("text", [line])


def code_piece(code: str, lang: str | None, caption: str | None = None) -> Piece:
    """A fenced code block. `code` is kept as is, apart from `normalize_text`."""
    code = normalize_text(code)
    body = code.rstrip("\n").split("\n")
    fence = "```"
    while any(line.lstrip().startswith(fence) for line in body):
        fence += "`"
    lines = [caption] if caption else []
    lines += [fence + (lang or ""), *body, fence]
    return Piece("code", lines, lang=lang, code=code)


def compose(
    pieces: list[Piece], first: str = "", indent: str = ""
) -> tuple[list[str], list[Nested]]:
    """Lines of several pieces, a blank line between them.

    `first` prefixes the very first line (a list marker), `indent` every other non-blank line.
    """
    lines: list[str] = []
    nested: list[Nested] = []
    for i, piece in enumerate(pieces):
        if i:
            lines.append("")
        offset = len(lines)
        for j, line in enumerate(piece.lines):
            prefix = first if i == 0 and j == 0 else indent
            lines.append(prefix + line if line else "")
        if piece.kind == "code" and piece.code is not None:
            nested.append(Nested(offset, offset + len(piece.lines) - 1, piece.lang, piece.code))
        nested.extend(
            Nested(n.start + offset, n.end + offset, n.lang, n.code) for n in piece.nested
        )
    if not lines:
        lines = [first.rstrip()]
    return lines, nested


def prefixed(label: str, pieces: list[Piece]) -> list[Piece]:
    """Put `label` in front of the first piece when it is a paragraph, else on its own line."""
    if pieces and pieces[0].kind == "text" and pieces[0].lines:
        first = pieces[0]
        head = f"{label} {first.lines[0]}".rstrip()
        return [dataclasses.replace(first, lines=[head, *first.lines[1:]]), *pieces[1:]]
    return [text_piece(label), *pieces]
