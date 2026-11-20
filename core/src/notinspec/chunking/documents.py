"""Read documentation files into `Document`s with normalized text."""

import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    source: str  # path relative to the docs root, "/"-separated; in chunk IDs, not breadcrumbs
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

    Raises `ValueError` for a match that resolves outside `root`, through `..` in a pattern
    or a symlink: patterns may come from an uploaded config, and the worker holds secrets.
    """
    real_root = root.resolve()
    found: dict[str, Path] = {}
    for pattern in patterns:
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            source = path.relative_to(root).as_posix()
            if not path.resolve().is_relative_to(real_root):
                raise ValueError(f"input resolves outside the docs root: {source}")
            found[source] = path
    return tuple(
        Document(source, normalize_text(found[source].read_bytes().decode("utf-8", "replace")))
        for source in sorted(found)
    )
