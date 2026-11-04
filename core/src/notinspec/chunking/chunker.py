"""Split Markdown documents into `Chunk`s (SPEC §6.1).

Rules:

- every heading starts a new chunk; the heading path ("breadcrumb") says where it is
- code blocks, tables, lists and quotes are never cut
- a section longer than `max_tokens` is split between blocks into parts; a heading stays with
  the block after it, and a paragraph stays with the code block right after it ("Example:")
- a single block longer than `max_tokens` becomes its own part, marked `oversized`
- short sections are never merged, so one section's boundaries don't depend on its neighbours
- a heading with no content of its own (directly followed by a sub-heading) gives no chunk

Three IDs, all derived from content, never from run order (64-bit hex):

- `id`: source + heading path + text (SPEC §6.1). Any edit gives a new `id`.
- `location_id`: source + heading path only. Survives edits of the text, so a PR diff can tell
  "this section changed" from "this is a new section".
- `content_hash`: text only.
"""

from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass

from notinspec.adapters.canonical import content_hash
from notinspec.chunking.blocks import Block, ParsedBlock, parse_blocks
from notinspec.chunking.documents import Document, normalize_text
from notinspec.chunking.tokens import approx_tokens

# bump when chunk boundaries or IDs change for the same input
CHUNKER_VERSION = 1

DEFAULT_MAX_TOKENS = 400  # upper end of SPEC's ~150–400, below the 512-token NLI limit

BREADCRUMB_SEPARATOR = " > "


@dataclass(frozen=True)
class Chunk:
    id: str
    location_id: str
    content_hash: str
    source: str  # document path
    heading_path: tuple[str, ...]  # () for text before the first heading
    breadcrumb: str  # "docs/client.md > Connecting > connect()"
    heading_level: int  # level of the section's own heading, 0 before the first heading
    occurrence: int  # 0, or 1, 2, ... for later sections with the same heading path
    part: int  # 1-based; > 1 only when a long section was split
    parts: int
    start_line: int  # 1-based, inclusive, in the source file
    end_line: int
    tokens: int
    oversized: bool  # one block alone is longer than max_tokens
    text: str  # exact Markdown of the chunk, heading line included in part 1
    blocks: tuple[Block, ...]


def chunk_document(
    document: Document,
    *,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    count_tokens: Callable[[str], int] = approx_tokens,
) -> tuple[Chunk, ...]:
    """Chunks of one document, in document order. Pure: same input → equal output."""
    lines = normalize_text(document.text).split("\n")
    parsed = parse_blocks("\n".join(lines), count_tokens)
    chunks: list[Chunk] = []
    seen: dict[tuple[str, ...], int] = {}
    for path, level, section in _sections(parsed):
        if all(p.heading is not None for p in section):
            continue
        occurrence = seen.get(path, 0)
        seen[path] = occurrence + 1
        parts = _pack(_units(section, max_tokens), max_tokens)
        for number in range(1, len(parts) + 1):
            chunks.append(
                _chunk(document.source, lines, path, level, occurrence, number, parts, max_tokens)
            )
    return tuple(chunks)


def chunk_documents(
    documents: Sequence[Document],
    *,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    count_tokens: Callable[[str], int] = approx_tokens,
) -> tuple[Chunk, ...]:
    return tuple(
        chunk
        for document in documents
        for chunk in chunk_document(document, max_tokens=max_tokens, count_tokens=count_tokens)
    )


type _Section = list[ParsedBlock]
type _Unit = list[ParsedBlock]


def _sections(parsed: list[ParsedBlock]) -> Iterator[tuple[tuple[str, ...], int, _Section]]:
    stack: list[tuple[int, str]] = []
    path: tuple[str, ...] = ()
    level = 0
    current: _Section = []
    for block in parsed:
        if block.heading is None:
            current.append(block)
            continue
        if current:
            yield path, level, current
        level, title = block.heading
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))
        path = tuple(t for _, t in stack)
        current = [block]
    if current:
        yield path, level, current


def _units(section: _Section, max_tokens: int) -> list[_Unit]:
    """Group blocks that must stay in the same part."""
    units: list[_Unit] = []
    i = 0
    while i < len(section):
        unit = [section[i]]
        i += 1
        while i < len(section) and _glue(unit, section[i], max_tokens):
            unit.append(section[i])
            i += 1
        units.append(unit)
    return units


def _glue(unit: _Unit, following: ParsedBlock, max_tokens: int) -> bool:
    last = unit[-1].block.kind
    if last == "heading":
        return True
    if last == "text" and following.block.kind == "code":
        return _tokens(unit) + following.block.tokens <= max_tokens
    return False


def _pack(units: list[_Unit], max_tokens: int) -> list[_Unit]:
    """Fill parts greedily, in order, without going over max_tokens unless one unit does."""
    parts: list[_Unit] = []
    current: _Unit = []
    for unit in units:
        if current and _tokens(current) + _tokens(unit) > max_tokens:
            parts.append(current)
            current = []
        current = current + unit
    if current:
        parts.append(current)
    return parts


def _tokens(blocks: _Unit) -> int:
    return sum(p.block.tokens for p in blocks)


def _chunk(
    source: str,
    lines: list[str],
    path: tuple[str, ...],
    level: int,
    occurrence: int,
    number: int,
    parts: list[_Unit],
    max_tokens: int,
) -> Chunk:
    part = parts[number - 1]
    start, end = part[0].block.start_line, part[-1].block.end_line
    text = "\n".join(lines[start - 1 : end])
    tokens = _tokens(part)
    location = [source, list(path), occurrence, number]
    return Chunk(
        id=_hash([*location, text]),
        location_id=_hash(location),
        content_hash=_hash(text),
        source=source,
        heading_path=path,
        breadcrumb=BREADCRUMB_SEPARATOR.join((source, *path)),
        heading_level=level,
        occurrence=occurrence,
        part=number,
        parts=len(parts),
        start_line=start,
        end_line=end,
        tokens=tokens,
        oversized=tokens > max_tokens,
        text=text,
        blocks=tuple(b for p in part for b in (p.block, *p.nested)),
    )


def _hash(obj: object) -> str:
    return content_hash(obj)[:16]
