"""Chunks → `Example`s: every code block of a chunk is one example (SPEC §4, §6.2 component C).

Code blocks come already typed from the reader (Sphinx `literal_block`, `doctest_block`,
captioned code; Markdown fences), including code nested in a list item, quote, admonition or
parameter entry. A `math` block is not code and gives no example.

IDs, derived from the input, never from run order (64-bit hex, as chunk IDs):

- `id`: chunk ID + the block's position among the chunk's code blocks. An edit inside the
  code keeps the ID, as an edit inside a section keeps the chunk ID.
- `content_hash`: language + code. Tells that the example changed.
"""

from collections.abc import Iterable
from dataclasses import dataclass

from notinspec.adapters.canonical import content_hash
from notinspec.chunking import Chunk

# bump when example IDs or boundaries change for the same chunks
EXAMPLES_VERSION = 1

_NOT_CODE = frozenset({"math"})


@dataclass(frozen=True)
class Example:
    id: str  # identity: chunk ID + position; survives edits of the code
    chunk_id: str
    section_id: str  # `Chunk.section_id`: the whole section, for `Source` and gold context
    position: int  # 0-based, among the chunk's code blocks in document order
    content_hash: str
    lang: str | None  # as the docs give it, lower case: "python", "pycon", "default"; None = none
    code: str  # as in the docs: prompts and output of a `pycon` block included
    start_line: int  # 1-based, inclusive, in the chunk's source document (as `Block`)
    end_line: int
    nested: bool  # inside a list item, quote, admonition or parameter entry


def chunk_examples(chunk: Chunk) -> tuple[Example, ...]:
    """The examples of one chunk, in document order. Pure."""
    blocks = [
        b
        for b in chunk.blocks
        if b.kind == "code" and b.code is not None and b.lang not in _NOT_CODE
    ]
    examples = []
    for position, block in enumerate(blocks):
        assert block.code is not None
        examples.append(
            Example(
                id=_hash([chunk.id, position]),
                chunk_id=chunk.id,
                section_id=chunk.section_id,
                position=position,
                content_hash=_hash([block.lang, block.code]),
                lang=block.lang,
                code=block.code,
                start_line=block.start_line,
                end_line=block.end_line,
                nested=block.nested,
            )
        )
    return tuple(examples)


def extract_examples(chunks: Iterable[Chunk]) -> tuple[Example, ...]:
    """The examples of all chunks, in chunk order. Pure."""
    return tuple(example for chunk in chunks for example in chunk_examples(chunk))


def _hash(obj: object) -> str:
    return content_hash(obj)[:16]
