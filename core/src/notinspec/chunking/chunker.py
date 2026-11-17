"""Split documents into `Chunk`s: one chunk per documentation section (SPEC §6.1).

Two steps: a reader turns a document into a `BlockDocument` (text + typed blocks with line
ranges into that text), then `chunk_blocks` cuts it into sections. Markdown goes through
`parse_blocks` (`chunk_document`); the Sphinx reader (`notinspec.sphinx`) builds the blocks
straight from the doctree. The rules below are the same for both.

Rules:

- a section runs from its heading to the next heading; the breadcrumb (project + heading
  path) says where it is. The file path is not in the breadcrumb, it stays in `source`.
  There is no small token limit: the NLI size limit lives in `windows.py`.
- code blocks, tables, lists and quotes are never cut
- soft-limit fallback: a section longer than `soft_limit` is split between blocks (paragraph
  boundaries) into parts of about equal size. A heading stays with the block after it, and a
  paragraph stays with the code block right after it ("Example:"). The parts keep the
  section's breadcrumb and `section_id`. A field label ("**Parameters:**") stays with the
  first field entry after it.
- a single block longer than `soft_limit` becomes its own part, marked `oversized`
- short sections are never merged, so one section's boundaries don't depend on its neighbours
- a heading with no content of its own (directly followed by a sub-heading) gives no chunk

IDs, derived from the input, never from run order (64-bit hex). The project name is not
part of them, so renaming the project keeps every ID:

- `id`: source + heading path + occurrence + part (SPEC §6.1). The chunk's identity: it
  survives edits of the text, so a typo fix keeps the chunk and everything derived from it.
- `section_id`: source + heading path + occurrence, no part. Same for every part of one
  section: the key for "the whole section" (gold context, retrieval results, `Source`).
- `content_hash`: text only. Tells that a chunk changed (CI diff, regenerating test items).
"""

from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass

from notinspec.adapters.canonical import content_hash
from notinspec.chunking.blocks import Block, ParsedBlock, parse_blocks
from notinspec.chunking.documents import Document, normalize_text
from notinspec.chunking.tokens import approx_tokens

# bump when chunk boundaries or IDs change for the same input
CHUNKER_VERSION = 3

DEFAULT_SOFT_LIMIT = 2000  # SPEC §6.1 candidate; sections above it are split into parts

BREADCRUMB_SEPARATOR = " > "


@dataclass(frozen=True)
class Chunk:
    id: str  # identity: survives text edits
    section_id: str  # equal for all parts of one section
    content_hash: str
    source: str  # document path
    heading_path: tuple[str, ...]  # () for text before the first heading
    breadcrumb: str  # "acme > Client > Connecting"
    heading_level: int  # level of the section's own heading, 0 before the first heading
    occurrence: int  # 0, or 1, 2, ... for later sections with the same heading path
    part: int  # 1-based; > 1 only when a long section was split
    parts: int
    start_line: int  # 1-based, inclusive, in the source file
    end_line: int
    tokens: int
    oversized: bool  # one block alone is longer than soft_limit
    text: str  # exact Markdown of the chunk, heading line included in part 1
    blocks: tuple[Block, ...]


@dataclass(frozen=True)
class BlockDocument:
    """A document already split into blocks: the input of `chunk_blocks`."""

    source: str  # Markdown: file path; Sphinx: docname ("reference-core"); in IDs, not breadcrumbs
    text: str  # normalized text; block line ranges point into it
    blocks: tuple[ParsedBlock, ...]


def chunk_document(
    document: Document,
    *,
    project: str,
    soft_limit: int = DEFAULT_SOFT_LIMIT,
    count_tokens: Callable[[str], int] = approx_tokens,
) -> tuple[Chunk, ...]:
    """Chunks of one Markdown document, in document order. Pure: same input → equal output."""
    text = normalize_text(document.text)
    blocks = tuple(parse_blocks(text, count_tokens))
    return chunk_blocks(
        BlockDocument(document.source, text, blocks), project=project, soft_limit=soft_limit
    )


def chunk_blocks(
    document: BlockDocument, *, project: str, soft_limit: int = DEFAULT_SOFT_LIMIT
) -> tuple[Chunk, ...]:
    """Chunks of one document from its blocks, in document order. Pure.

    Block sizes come from the blocks (`Block.tokens`), so no token counter is needed here.
    """
    lines = document.text.split("\n")
    chunks: list[Chunk] = []
    seen: dict[tuple[str, ...], int] = {}
    for path, level, section in _sections(document.blocks):
        if all(p.heading is not None for p in section):
            continue
        occurrence = seen.get(path, 0)
        seen[path] = occurrence + 1
        parts = _pack(_units(section, soft_limit), soft_limit)
        for number in range(1, len(parts) + 1):
            chunks.append(
                _chunk(
                    document.source,
                    project,
                    lines,
                    path,
                    level,
                    occurrence,
                    number,
                    parts,
                    soft_limit,
                )
            )
    return tuple(chunks)


def chunk_documents(
    documents: Sequence[Document],
    *,
    project: str,
    soft_limit: int = DEFAULT_SOFT_LIMIT,
    count_tokens: Callable[[str], int] = approx_tokens,
) -> tuple[Chunk, ...]:
    return tuple(
        chunk
        for document in documents
        for chunk in chunk_document(
            document, project=project, soft_limit=soft_limit, count_tokens=count_tokens
        )
    )


type _Section = list[ParsedBlock]
type _Unit = list[ParsedBlock]


def _sections(parsed: Sequence[ParsedBlock]) -> Iterator[tuple[tuple[str, ...], int, _Section]]:
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


def _units(section: _Section, soft_limit: int) -> list[_Unit]:
    """Group blocks that must stay in the same part."""
    units: list[_Unit] = []
    i = 0
    while i < len(section):
        unit = [section[i]]
        i += 1
        while i < len(section) and _glue(unit, section[i], soft_limit):
            unit.append(section[i])
            i += 1
        units.append(unit)
    return units


def _glue(unit: _Unit, following: ParsedBlock, soft_limit: int) -> bool:
    last = unit[-1].block.kind
    if last == "heading":
        return True
    if last == "text" and following.block.kind in ("code", "field"):  # "Example:", label
        return _tokens(unit) + following.block.tokens <= soft_limit
    return False


def _pack(units: list[_Unit], soft_limit: int) -> list[_Unit]:
    """Split into as few parts as `soft_limit` allows, of about equal size.

    Greedy packing alone gives e.g. 2,000 + 100 tokens; a tiny last part is a poor gold
    context. So find the smallest cap that still needs no more parts, and pack with that.
    """
    parts = _greedy(units, soft_limit)
    low = max(_tokens(u) for u in units)
    if len(parts) < 2 or low > soft_limit:  # one part, or an oversized unit: nothing to even out
        return parts
    high = soft_limit
    while low < high:
        cap = (low + high) // 2
        if len(_greedy(units, cap)) <= len(parts):
            high = cap
        else:
            low = cap + 1
    return _greedy(units, low)


def _greedy(units: list[_Unit], cap: int) -> list[_Unit]:
    """Fill parts in order, without going over `cap` unless one unit does."""
    parts: list[_Unit] = []
    current: _Unit = []
    for unit in units:
        if current and _tokens(current) + _tokens(unit) > cap:
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
    project: str,
    lines: list[str],
    path: tuple[str, ...],
    level: int,
    occurrence: int,
    number: int,
    parts: list[_Unit],
    soft_limit: int,
) -> Chunk:
    part = parts[number - 1]
    start, end = part[0].block.start_line, part[-1].block.end_line
    text = "\n".join(lines[start - 1 : end])
    tokens = _tokens(part)
    section = [source, list(path), occurrence]
    return Chunk(
        id=_hash([*section, number]),
        section_id=_hash(section),
        content_hash=_hash(text),
        source=source,
        heading_path=path,
        breadcrumb=BREADCRUMB_SEPARATOR.join((project, *path)),
        heading_level=level,
        occurrence=occurrence,
        part=number,
        parts=len(parts),
        start_line=start,
        end_line=end,
        tokens=tokens,
        oversized=tokens > soft_limit,
        text=text,
        blocks=tuple(b for p in part for b in (p.block, *p.nested)),
    )


def _hash(obj: object) -> str:
    return content_hash(obj)[:16]
