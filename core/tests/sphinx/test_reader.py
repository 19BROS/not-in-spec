import re
import shutil
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from notinspec.chunking import Chunk, chunk_blocks
from notinspec.sphinx import (
    SPHINX_READER_VERSION,
    SphinxInputError,
    SphinxXml,
    read_sphinx_version,
    read_sphinx_xml,
)
from notinspec.sphinx.reader import normalize_xml

Golden = Callable[[str, object], None]
FIXTURES = Path(__file__).parents[1] / "fixtures" / "sphinx"
EXAMPLES = Path(__file__).parents[2] / "examples" / "sphinx"
STYLES = ("napoleon", "numpydoc", "plain")
LIBRARIES = ("urllib3", "trio", "hydra-zen")

_DOC = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<document source="/src/docs/{name}.rst">{body}</document>\n'
)


def _chunks(xml: SphinxXml, project: str) -> tuple[Chunk, ...]:
    return tuple(c for d in xml.documents for c in chunk_blocks(d, project=project))


def _folder(tmp_path: Path, env: str = "sphinx-build 9.1.1\n", **docs: str) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "build-env.txt").write_text(env, encoding="utf-8")
    for name, body in (docs or {"index": "<paragraph>Hi.</paragraph>"}).items():
        (tmp_path / f"{name}.xml").write_text(_DOC.format(name=name, body=body), encoding="utf-8")
    return tmp_path


# --- golden fixture: one tiny project built three ways ------------------------------------


@pytest.mark.parametrize("style", STYLES)
def test_fixture_golden(style: str, golden: Golden) -> None:
    xml = read_sphinx_xml(FIXTURES / f"xml-{style}")
    golden(
        f"fixture-{style}",
        {
            "reader_version": SPHINX_READER_VERSION,
            "sphinx_version": xml.sphinx_version,
            "files": xml.files,
            "warnings": xml.warnings,
            "chunks": _chunks(xml, "fixturelib"),
        },
    )


def _fields(style: str, breadcrumb: str) -> list[tuple[str | None, str | None, str | None]]:
    chunks = _chunks(read_sphinx_xml(FIXTURES / f"xml-{style}"), "fixturelib")
    chunk = next(c for c in chunks if c.breadcrumb == breadcrumb)
    return [(b.field, b.name, b.type) for b in chunk.blocks if b.kind == "field"]


def test_three_field_shapes_give_the_same_entries() -> None:
    numpy = "fixturelib > API Reference > receive()"
    expected = [("param", "size", "int, optional"), ("param", "strict", "bool")]
    assert _fields("napoleon", numpy)[:2] == expected  # shape A, from napoleon
    assert _fields("numpydoc", numpy)[:2] == expected  # shape C
    assert _fields("numpydoc", numpy)[2] == ("returns", None, "bytes")  # C: term is the type
    assert _fields("plain", "fixturelib > API Reference > Connection") == [
        ("param", "host", None)  # shape B: one parameter
    ]
    assert _fields("plain", "fixturelib > API Reference > connect()") == [
        ("param", "host", None),
        ("param", "timeout", "float or None"),
        ("param", "retries", None),
        ("returns", None, None),
        ("raises", "ValueError", None),
        ("raises", "TimeoutError", None),
    ]


def test_google_style_without_napoleon_is_a_plain_list() -> None:
    chunks = _chunks(read_sphinx_xml(FIXTURES / "xml-plain"), "fixturelib")
    send = next(c for c in chunks if c.breadcrumb == "fixturelib > API Reference > send()")
    assert [b.kind for b in send.blocks] == ["heading", "signature", "text", "list"]
    assert "- Args: data: The payload. flush (bool): Flush after sending." in send.text


# --- build-env.txt: Sphinx 9.x only ---------------------------------------------------------


def test_version_is_the_first_line_of_build_env(tmp_path: Path) -> None:
    folder = _folder(tmp_path, "﻿sphinx-build 9.1.0\r\nPython 3.12.15\r\n")
    assert read_sphinx_version(folder) == "9.1.0"
    assert read_sphinx_xml(folder).sphinx_version == "9.1.0"


@pytest.mark.parametrize(
    ("env", "message"),
    [
        ("sphinx-build 8.2.3\n", "Sphinx 8.2.3 is not supported"),
        ("sphinx-build 10.0.0\n", "not supported"),
        ("Python 3.12.15\nsphinx-build 9.1.0\n", "first line"),
        ("", "first line"),
    ],
)
def test_other_sphinx_versions_are_rejected(tmp_path: Path, env: str, message: str) -> None:
    folder = _folder(tmp_path, env)
    with pytest.raises(SphinxInputError, match=message):
        read_sphinx_xml(folder)


def test_missing_build_env_is_rejected(tmp_path: Path) -> None:
    folder = _folder(tmp_path)
    (folder / "build-env.txt").unlink()
    with pytest.raises(SphinxInputError, match="build-env.txt is missing"):
        read_sphinx_version(folder)


def test_version_alone_reads_no_xml(tmp_path: Path) -> None:
    folder = _folder(tmp_path)
    (folder / "index.xml").write_text("<not xml", encoding="utf-8")
    assert read_sphinx_version(folder) == "9.1.1"


# --- unsafe or broken XML ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "xml",
    [
        # external entity (XXE)
        '<?xml version="1.0"?><!DOCTYPE document [<!ENTITY x SYSTEM "file:///etc/passwd">]>'
        "<document><paragraph>&x;</paragraph></document>",
        # entity expansion ("billion laughs")
        '<?xml version="1.0"?><!DOCTYPE document [<!ENTITY a "aaaa"><!ENTITY b "&a;&a;">]>'
        "<document><paragraph>&b;</paragraph></document>",
    ],
)
def test_entities_are_rejected(tmp_path: Path, xml: str) -> None:
    folder = _folder(tmp_path)
    (folder / "index.xml").write_text(xml, encoding="utf-8")
    with pytest.raises(SphinxInputError, match="index.xml: unsafe XML"):
        read_sphinx_xml(folder)


def test_docutils_doctype_is_accepted(tmp_path: Path) -> None:
    folder = _folder(tmp_path)
    (folder / "index.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE document PUBLIC "+//IDN '
        'docutils.sourceforge.net//DTD Docutils Generic//EN//XML" '
        '"http://docutils.sourceforge.net/docs/ref/docutils.dtd">\n'
        '<document source="/src/index.rst"><paragraph>Hi.</paragraph></document>',
        encoding="utf-8",
    )
    assert read_sphinx_xml(folder).documents[0].text == "Hi."


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("<document><paragraph></document>", "not well-formed"),
        ("<html><p>Hi</p></html>", "not a Docutils document"),
    ],
)
def test_broken_xml_is_rejected(tmp_path: Path, content: str, message: str) -> None:
    folder = _folder(tmp_path)
    (folder / "index.xml").write_text(content, encoding="utf-8")
    with pytest.raises(SphinxInputError, match=message):
        read_sphinx_xml(folder)


def test_folder_without_xml_is_rejected(tmp_path: Path) -> None:
    folder = _folder(tmp_path)
    (folder / "index.xml").unlink()
    with pytest.raises(SphinxInputError, match="no \\*.xml files"):
        read_sphinx_xml(folder)


# --- files, docnames and hashes -------------------------------------------------------------


def test_docnames_files_and_static_output(tmp_path: Path) -> None:
    folder = _folder(tmp_path, index="<paragraph>A</paragraph>")
    (folder / "generated").mkdir()
    (folder / "generated" / "pkg.f.xml").write_text(
        _DOC.format(name="generated/pkg.f", body="<paragraph>B</paragraph>"), encoding="utf-8"
    )
    (folder / "_static").mkdir()
    (folder / "_static" / "theme.js").write_text("alert(1)", encoding="utf-8")
    xml = read_sphinx_xml(folder)
    assert [d.source for d in xml.documents] == ["generated/pkg.f", "index"]
    assert [path for path, _ in xml.files] == ["build-env.txt", "generated/pkg.f.xml", "index.xml"]


def test_hash_ignores_checkout_path_and_line_endings(tmp_path: Path) -> None:
    original = FIXTURES / "xml-napoleon"
    moved = tmp_path / "moved"
    shutil.copytree(original, moved)
    for path in moved.glob("*.xml"):
        text = path.read_text(encoding="utf-8").replace('source="/src/', 'source="C:\\work\\x/')
        path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
    first, second = read_sphinx_xml(original), read_sphinx_xml(moved)
    assert first.files == second.files
    assert first.documents == second.documents
    assert first.warnings == second.warnings


def test_build_env_is_hashed_as_is(tmp_path: Path) -> None:
    folder = _folder(tmp_path)
    before = dict(read_sphinx_xml(folder).files)
    (folder / "build-env.txt").write_text("sphinx-build 9.1.1\nfoo==2\n", encoding="utf-8")
    after = dict(read_sphinx_xml(folder).files)
    assert before["index.xml"] == after["index.xml"]
    assert before["build-env.txt"] != after["build-env.txt"]


def test_source_paths_are_relative_to_the_source_folder() -> None:
    warnings: Counter[str] = Counter()
    xml = (
        '<document source="/home/a/proj/docs/guide/intro.rst">'
        '<literal_block source="/home/a/proj/docs/snippets/x.py">x</literal_block>'
        '<literal_block source="/home/a/proj/src/lib.py">source="/home/a/keep"</literal_block>'
        "</document>"
    )
    out = normalize_xml(xml.encode(), "guide/intro", warnings).decode()
    assert out == (
        '<document source="guide/intro.rst">'
        '<literal_block source="snippets/x.py">x</literal_block>'
        '<literal_block source="lib.py">source="/home/a/keep"</literal_block>'  # text unchanged
        "</document>"
    )
    assert warnings == Counter({"source path outside the Sphinx source folder in guide/intro": 1})


def test_unknown_source_folder_keeps_file_names_only() -> None:
    warnings: Counter[str] = Counter()
    out = normalize_xml(b'<document source="/x/other.rst"/>', "index", warnings).decode()
    assert out == '<document source="other.rst"/>'
    assert warnings == Counter({"no Sphinx source folder found in index": 1})


def test_reading_twice_is_equal() -> None:
    folder = FIXTURES / "xml-numpydoc"
    assert read_sphinx_xml(folder) == read_sphinx_xml(folder)


# --- the three real libraries -----------------------------------------------------------------


@pytest.fixture(scope="module", params=LIBRARIES)
def library(request: pytest.FixtureRequest) -> tuple[str, SphinxXml]:
    name: str = request.param
    return name, read_sphinx_xml(EXAMPLES / name / "xml")


def test_real_libraries_read_without_unknown_nodes(library: tuple[str, SphinxXml]) -> None:
    name, xml = library
    assert xml.sphinx_version.startswith("9.")
    assert not [w for w in xml.warnings if w.startswith("unknown")]
    chunks = _chunks(xml, name)
    with_text = {d.source for d in xml.documents if any(p.heading is None for p in d.blocks)}
    assert {c.source for c in chunks} == with_text
    assert not [c.breadcrumb for c in chunks if "/src/" in c.text]
    assert not [c.breadcrumb for c in chunks if c.oversized]


def test_real_libraries_are_deterministic(library: tuple[str, SphinxXml]) -> None:
    name, xml = library
    assert read_sphinx_xml(EXAMPLES / name / "xml") == xml


def test_hydra_zen_numpydoc_fields() -> None:
    xml = read_sphinx_xml(EXAMPLES / "hydra-zen" / "xml")
    fields = [p.block for d in xml.documents for p in d.blocks if p.block.kind == "field"]
    groups = sum(1 for d in xml.documents for line in d.text.split("\n") if _label(line))
    assert groups == 63  # every numpydoc field (census: 32 + 22 + 6 + 3) gives a group
    assert len(fields) == 193
    assert all(b.name or b.type for b in fields)
    assert all(b.name for b in fields if b.field in ("param", "raises"))
    assert all(b.type for b in fields if b.field == "returns" and b.name is None)


def _plain(node: ET.Element | str | None) -> str:
    text = node if isinstance(node, str) else "".join(node.itertext()) if node is not None else ""
    return " ".join(text.replace("`", "").split())


def _label(line: str) -> bool:
    return re.fullmatch(r"\*\*[A-Z][\w ]*:\*\*", line) is not None


def test_trio_prose_after_a_desc_stays_in_its_section() -> None:
    folder = EXAMPLES / "trio" / "xml"
    chunks = _chunks(read_sphinx_xml(folder), "trio")
    found = 0
    for path in sorted(folder.glob("*.xml")):
        for section in ET.parse(path).iter("section"):
            tags = [child.tag for child in section]
            if "desc" not in tags:
                continue
            last = max(i for i, tag in enumerate(tags) if tag == "desc")
            after = [c for c in list(section)[last:] if c.tag == "paragraph" and c.text]
            if not after:
                continue
            found += 1
            title = _plain(section.find("title"))
            words = _plain(after[0])
            owner = next(c for c in chunks if words in _plain(c.text))
            assert owner.heading_path[-1] == title, words
    assert found == 6
