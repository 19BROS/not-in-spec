"""Read documentation files into `Document`s with normalized text."""

import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    source: str  # path relative to the docs root, "/"-separated; part of breadcrumbs and chunk IDs
    text: str  # Markdown


def normalize_text(text: str) -> str:
    """Make text that differs only in invisible ways identical, so chunk IDs don't change.

    Drops a BOM, turns CRLF / CR into LF, applies Unicode NFC (so "á" typed two ways is one
    string) and strips trailing whitespace from every line. The number of lines never changes,
    so line numbers still point into the original file.
    """
    text = text.removeprefix("﻿").replace("\r\n", "\n").replace("\r", "\n")
    text = unicodedata.normalize("NFC", text)
    return "\n".join(line.rstrip() for line in text.split("\n"))


def load_documents(root: Path, patterns: Sequence[str]) -> tuple[Document, ...]:
    """Read every file under `root` matching any glob in `patterns` (e.g. `docs/**/*.md`).

    Sorted by path, each file once. Bytes that aren't UTF-8 are replaced, not fatal: one bad
    file must not stop the whole run.
    """
    found: dict[str, Path] = {}
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file():
                found[path.relative_to(root).as_posix()] = path
    return tuple(
        Document(source, normalize_text(found[source].read_bytes().decode("utf-8", "replace")))
        for source in sorted(found)
    )
