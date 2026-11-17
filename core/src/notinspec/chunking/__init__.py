"""Reading and chunking: Markdown documentation → `Chunk`s and NLI windows (SPEC §6.1).

A chunk is one whole documentation section. NLI windows are short prose-only excerpts of a
chunk, input for NLI grounding. Input here is Markdown (also llms.txt and most MDX);
other readers (Sphinx) produce the same `Chunk`s.
"""

from notinspec.chunking.blocks import Block, BlockKind, ParsedBlock, parse_blocks
from notinspec.chunking.chunker import (
    CHUNKER_VERSION,
    DEFAULT_SOFT_LIMIT,
    BlockDocument,
    Chunk,
    chunk_blocks,
    chunk_document,
    chunk_documents,
)
from notinspec.chunking.documents import Document, load_documents, normalize_text
from notinspec.chunking.tokens import approx_tokens
from notinspec.chunking.windows import (
    DEFAULT_OVERLAP_TOKENS,
    DEFAULT_WINDOW_TOKENS,
    WINDOWS_VERSION,
    NliWindow,
    Sentence,
    find_citation,
    nli_windows,
    prose_sentences,
)

__all__ = [
    "CHUNKER_VERSION",
    "DEFAULT_OVERLAP_TOKENS",
    "DEFAULT_SOFT_LIMIT",
    "DEFAULT_WINDOW_TOKENS",
    "WINDOWS_VERSION",
    "Block",
    "BlockDocument",
    "BlockKind",
    "Chunk",
    "Document",
    "NliWindow",
    "Sentence",
    "ParsedBlock",
    "approx_tokens",
    "chunk_blocks",
    "chunk_document",
    "chunk_documents",
    "find_citation",
    "load_documents",
    "nli_windows",
    "normalize_text",
    "parse_blocks",
    "prose_sentences",
]
