"""Sphinx reader: `sphinx-build -b xml` output (the Docutils doctree) → `BlockDocument`s.

MVP reads Sphinx 9.x only (SPEC §6.1). `read_sphinx_xml` reads a whole XML folder; pass each
document to `notinspec.chunking.chunk_blocks` to get the same `Chunk`s as from Markdown.
Rules: `reader.py` (files, version, hash), `render.py` (nodes → blocks), `fields.py`
(parameter / returns / raises entries), `inline.py` (inline nodes → text).
"""

from notinspec.sphinx.reader import (
    BUILD_ENV,
    SPHINX_READER_VERSION,
    SUPPORTED_SPHINX_MAJOR,
    SphinxInputError,
    SphinxXml,
    read_sphinx_version,
    read_sphinx_xml,
)

__all__ = [
    "BUILD_ENV",
    "SPHINX_READER_VERSION",
    "SUPPORTED_SPHINX_MAJOR",
    "SphinxInputError",
    "SphinxXml",
    "read_sphinx_version",
    "read_sphinx_xml",
]
