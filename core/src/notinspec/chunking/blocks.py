"""Split Markdown into top-level blocks (heading, text, code, table, ...) with line ranges.

A real CommonMark parser decides what a block is, so a `# comment` inside a code fence is never
a heading and a table is always one block. Headings inside lists or quotes don't start sections.
"""

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from markdown_it import MarkdownIt
from markdown_it.token import Token

type BlockKind = Literal["heading", "text", "code", "table", "list", "quote", "html", "rule"]

_MD = MarkdownIt("commonmark").enable("table")

_KIND: dict[str, BlockKind] = {
    "heading_open": "heading",
    "paragraph_open": "text",
    "fence": "code",
    "code_block": "code",
    "table_open": "table",
    "bullet_list_open": "list",
    "ordered_list_open": "list",
    "blockquote_open": "quote",
    "html_block": "html",
    "hr": "rule",
}

_FRONT_MATTER = {"---": ("---", "..."), "+++": ("+++",)}  # YAML, TOML (Hugo)


@dataclass(frozen=True)
class Block:
    kind: BlockKind
    start_line: int  # 1-based, inclusive, in the source file
    end_line: int  # 1-based, inclusive
    tokens: int
    lang: str | None = None  # code only: first word of the fence info, lower case ("python")
    code: str | None = None  # code only: the code without the fence lines
    # code inside a list item or quote: its lines are also part of the container block before it
    nested: bool = False


@dataclass(frozen=True)
class ParsedBlock:
    block: Block
    heading: tuple[int, str] | None  # (level 1–6, plain text) for headings
    nested: tuple[Block, ...]  # code blocks inside a list or quote


def parse_blocks(text: str, count_tokens: Callable[[str], int]) -> list[ParsedBlock]:
    """Top-level blocks of normalized Markdown, in order. Front matter is skipped."""
    lines = _blank_front_matter(text.split("\n"))
    tokens = _MD.parse("\n".join(lines))
    result: list[ParsedBlock] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.level != 0 or token.map is None:
            i += 1
            continue
        close = _close_index(tokens, i)
        inner = tokens[i + 1 : close]
        i = close + 1
        kind = _KIND.get(token.type)
        if kind is None:
            continue
        block = _block(kind, token, lines, count_tokens)
        heading = (int(token.tag[1:]), _plain(inner[0])) if kind == "heading" else None
        nested = tuple(
            _block("code", t, lines, count_tokens, nested=True)
            for t in inner
            if t.type in ("fence", "code_block") and t.map is not None
        )
        result.append(ParsedBlock(block, heading, nested))
    return result


def _block(
    kind: BlockKind,
    token: Token,
    lines: list[str],
    count_tokens: Callable[[str], int],
    *,
    nested: bool = False,
) -> Block:
    assert token.map is not None
    start, stop = token.map  # 0-based, stop exclusive; may include trailing blank lines
    while stop > start + 1 and not lines[stop - 1]:
        stop -= 1
    is_code = kind == "code"
    return Block(
        kind=kind,
        start_line=start + 1,
        end_line=stop,
        tokens=count_tokens("\n".join(lines[start:stop])),
        lang=_lang(token.info) if is_code else None,
        code=token.content if is_code else None,
        nested=nested,
    )


def _close_index(tokens: list[Token], i: int) -> int:
    """Index of the token that closes tokens[i] (itself for self-contained blocks)."""
    if tokens[i].nesting != 1:
        return i
    level = tokens[i].level
    return next(
        j for j in range(i + 1, len(tokens)) if tokens[j].level == level and tokens[j].nesting == -1
    )


def _plain(inline: Token) -> str:
    """Heading text without Markdown: "`connect()` **method**" → "connect() method"."""
    parts: list[str] = []
    for child in inline.children or []:
        if child.type in ("text", "code_inline", "image"):  # image content = alt text
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
    return " ".join("".join(parts).split()) or inline.content.strip()


def _lang(info: str) -> str | None:
    match = re.match(r"\{?\.?([\w+#.-]+)", info.strip())
    return match.group(1).lower() if match else None


def _blank_front_matter(lines: list[str]) -> list[str]:
    """Replace leading front matter with empty lines, so line numbers stay the same."""
    closers = _FRONT_MATTER.get(lines[0]) if lines else None
    if closers is None:
        return lines
    end = next((j for j in range(1, len(lines)) if lines[j] in closers), None)
    if end is None:
        return lines
    return [""] * (end + 1) + lines[end + 1 :]
