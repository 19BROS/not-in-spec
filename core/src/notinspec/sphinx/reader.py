"""Read a `sphinx-build -b xml` folder: version check, normalized hashes, documents.

- **Sphinx 9.x only** (MVP). The version is the first line of `build-env.txt`
  (`sphinx-build 9.1.0`); a missing file or another major version is a `SphinxInputError`.
- **Files** are every `*.xml` under the folder plus `build-env.txt`, sorted by their POSIX path
  relative to the folder. Other build output (`_static/*.js`, CSS) is not documentation and
  is neither read nor hashed.
- **Document** `source` = docname = the XML path relative to the folder, without `.xml`.
- **Hash normalization.** The XML holds the absolute path of the build's checkout in
  `source="…"` attributes (on `document`, and on `literal_block` from `literalinclude`), so
  the same docs built in another folder would hash differently. Before hashing, every
  `source=` value inside a tag loses the source-folder prefix (`srcdir` = the `document`'s
  `source` minus `<docname>.<suffix>`); a path outside `srcdir` keeps only its file name and
  gives a warning. Line endings become LF. This is done on the text, so the hash never
  depends on XML re-serialization; the normalized text is also what gets parsed.
  `build-env.txt` is hashed as is.
- **Safe parsing.** `defusedxml` with its defaults: entity declarations and external
  references are rejected (`SphinxInputError`). The DOCTYPE with a public DTD id that Docutils
  writes is fine; the DTD is never fetched.
"""

import hashlib
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from xml.etree.ElementTree import ParseError

import defusedxml
import defusedxml.ElementTree

from notinspec.chunking import BlockDocument, approx_tokens
from notinspec.sphinx.render import render_document

# bump when blocks, text or warnings can change for the same XML
SPHINX_READER_VERSION = 3  # 2: signature data, version directives; 3: whole `: X` types
SUPPORTED_SPHINX_MAJOR = 9
BUILD_ENV = "build-env.txt"

_VERSION = re.compile(r"sphinx-build\s+((\d+)\.\d+(?:\.\d+)?\S*)")
_TAG = re.compile(r"<[A-Za-z_][^<>]*>")  # start tags only: text content never has a raw "<"
_SOURCE_ATTR = re.compile(r'(\ssource=")([^"]*)(")')
_DOCUMENT_SOURCE = re.compile(r'<document\b[^<>]*?\ssource="([^"]*)"')


class SphinxInputError(ValueError):
    """The XML folder cannot be read: missing or unsupported build, unsafe or broken XML."""


@dataclass(frozen=True)
class SphinxXml:
    sphinx_version: str  # "9.1.1", from build-env.txt
    files: tuple[tuple[str, str], ...]  # (path relative to the folder, sha256 of normalized bytes)
    documents: tuple[BlockDocument, ...]  # sorted by source
    warnings: tuple[str, ...]  # sorted, e.g. "unknown node sd_foo (3x)"


def read_sphinx_version(root: Path) -> str:
    """The Sphinx version from the first line of `build-env.txt`. Reads nothing else."""
    path = root / BUILD_ENV
    if not path.is_file():
        raise SphinxInputError(
            f"{BUILD_ENV} is missing; write `sphinx-build --version` into it when you build "
            "the XML (see action/README.md)"
        )
    lines = path.read_bytes().decode("utf-8-sig", "replace").splitlines()
    match = _VERSION.fullmatch(lines[0].strip()) if lines else None
    if match is None:
        raise SphinxInputError(
            f"{BUILD_ENV}: the first line must be the output of `sphinx-build --version` "
            "(e.g. `sphinx-build 9.1.0`)"
        )
    version, major = match[1], int(match[2])
    if major != SUPPORTED_SPHINX_MAJOR:
        raise SphinxInputError(
            f"Sphinx {version} is not supported; build the XML with Sphinx "
            f"{SUPPORTED_SPHINX_MAJOR}.x"
        )
    return version


def read_sphinx_xml(root: Path, *, count_tokens: Callable[[str], int] = approx_tokens) -> SphinxXml:
    """All documents of the folder as blocks. Pure: same files ⇒ equal result."""
    version = read_sphinx_version(root)
    paths = {p.relative_to(root).as_posix(): p for p in root.rglob("*.xml") if p.is_file()}
    if not paths:
        raise SphinxInputError("no *.xml files; build them with `sphinx-build -b xml`")
    warnings: Counter[str] = Counter()
    hashes = {BUILD_ENV: hashlib.sha256((root / BUILD_ENV).read_bytes()).hexdigest()}
    documents = []
    for relative in sorted(paths):
        docname = relative.removesuffix(".xml")
        data = normalize_xml(paths[relative].read_bytes(), docname, warnings, relative)
        hashes[relative] = hashlib.sha256(data).hexdigest()
        try:
            tree = defusedxml.ElementTree.fromstring(data)
        except defusedxml.DefusedXmlException as error:
            raise SphinxInputError(f"{relative}: unsafe XML rejected ({error})") from error
        except ParseError as error:
            raise SphinxInputError(f"{relative}: not well-formed XML ({error})") from error
        if tree.tag != "document":
            raise SphinxInputError(f"{relative}: not a Docutils document (root <{tree.tag}>)")
        documents.append(render_document(tree, docname, warnings, count_tokens))
    return SphinxXml(
        sphinx_version=version,
        files=tuple(sorted(hashes.items())),
        documents=tuple(sorted(documents, key=lambda d: d.source)),
        warnings=tuple(sorted(f"{message} ({n}x)" for message, n in warnings.items())),
    )


def normalize_xml(data: bytes, docname: str, warnings: Counter[str], label: str = "") -> bytes:
    """The bytes that are hashed and parsed: `source=` paths relative to `srcdir`, LF endings."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise SphinxInputError(f"{label or docname}: not UTF-8 ({error})") from error
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    srcdir = _srcdir(text, docname)
    if srcdir is None:
        warnings[f"no Sphinx source folder found in {docname}"] += 1

    def attribute(match: re.Match[str]) -> str:
        value = match[2]
        slashed = value.replace("\\", "/")
        if srcdir is not None and slashed.startswith(srcdir):
            value = slashed[len(srcdir) :]
        elif value:
            value = slashed.rsplit("/", 1)[-1]
            if srcdir is not None:
                warnings[f"source path outside the Sphinx source folder in {docname}"] += 1
        return f"{match[1]}{value}{match[3]}"

    text = _TAG.sub(lambda tag: _SOURCE_ATTR.sub(attribute, tag[0]), text)
    return text.encode("utf-8")


def _srcdir(text: str, docname: str) -> str | None:
    """`/src/docs/` for `<document source="/src/docs/user-guide.rst">` and docname `user-guide`."""
    match = _DOCUMENT_SOURCE.search(text)
    if match is None:
        return None
    source = match[1].replace("\\", "/")
    found = re.fullmatch(rf"(.*/)?{re.escape(docname)}\.[^/.]+", source)
    return (found[1] or "") if found else None
