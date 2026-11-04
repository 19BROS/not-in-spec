"""Normalization and chunking: Markdown documentation → `Chunk`s (SPEC §6.1).

Input is Markdown (also llms.txt and most MDX). Converting HTML, PDF or DOCX to Markdown is a
separate step that runs before this one.
"""

from notinspec.chunking.blocks import Block, BlockKind
from notinspec.chunking.chunker import (
    CHUNKER_VERSION,
    DEFAULT_MAX_TOKENS,
    Chunk,
    chunk_document,
    chunk_documents,
)
from notinspec.chunking.documents import Document, load_documents, normalize_text
from notinspec.chunking.tokens import approx_tokens

__all__ = [
    "CHUNKER_VERSION",
    "DEFAULT_MAX_TOKENS",
    "Block",
    "BlockKind",
    "Chunk",
    "Document",
    "approx_tokens",
    "chunk_document",
    "chunk_documents",
    "load_documents",
    "normalize_text",
]
