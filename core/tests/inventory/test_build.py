from collections.abc import Callable
from pathlib import Path

import pytest

from notinspec.chunking import Chunk, chunk_blocks
from notinspec.inventory import (
    INVENTORY_BUILDER_VERSION,
    Inventory,
    InventoryBuild,
    Source,
    Symbol,
    build_inventory,
)
from notinspec.inventory.build import _constraints
from notinspec.sphinx import read_sphinx_xml

Golden = Callable[[str, object], None]
TESTS = Path(__file__).parents[1]
FIXTURES = TESTS / "fixtures" / "sphinx"
EXAMPLES = TESTS.parent / "examples" / "sphinx"

API = (Path(__file__).parent / "fixtures" / "api-body.xml").read_text("utf-8")


def _read(folder: Path) -> list[Chunk]:
    xml = read_sphinx_xml(folder)
    return [c for d in xml.documents for c in chunk_blocks(d, project="pkg")]


def _api(tmp_path: Path, body: str = API) -> InventoryBuild:
    (tmp_path / "build-env.txt").write_text("sphinx-build 9.1.1\n", encoding="utf-8")
    document = f'<?xml version="1.0"?>\n<document source="/src/docs/api.rst">{body}</document>\n'
    (tmp_path / "api.xml").write_text(document, encoding="utf-8")
    return build_inventory(_read(tmp_path))


def _symbol(inventory: Inventory, path: str) -> Symbol:
    return next(s for s in inventory.symbols if s.path == path)


def test_signature_blocks_give_symbols_with_python_parameter_kinds(tmp_path: Path) -> None:
    built = _api(tmp_path)
    inventory = built.inventory
    assert [(s.path, s.kind) for s in inventory.symbols] == [
        ("pkg.Pool", "class"),
        ("pkg.Pool.close", "method"),
        ("pkg.Pool.size", "property"),  # no parameter list: no signature
        ("pkg.compile", "function"),
        ("pkg.fetch", "function"),
    ]  # std:option is not Python: not in the MVP inventory
    (fetch,) = _symbol(inventory, "pkg.fetch").signatures
    assert [(p.name, p.kind, p.required, p.default, p.type) for p in fetch.parameters] == [
        ("url", "positional_only", True, None, "str"),
        ("mode", "positional_or_keyword", False, "'c'", "Literal['a, b', 'c']"),
        ("args", "var_positional", False, None, None),
        ("timeout", "keyword_only", True, None, "float"),  # type from the parameter entry
        ("retries", "keyword_only", False, "3", None),
        ("kw", "var_keyword", False, None, None),
    ]
    assert fetch.parameters[1].constraints[0].values == ("'a, b'", "'c'")
    assert fetch.returns is not None and fetch.returns.type == "bytes"
    assert fetch.text == "pkg.fetch(url: str, /, mode: Literal['a, b', 'c'] = 'c', *args, " + (
        "timeout, retries=3, **kw) -> bytes"
    )
    (close,) = _symbol(inventory, "pkg.Pool.close").signatures
    assert close.parameters == ()
    assert close.returns is not None and close.returns.type == "None"  # from `Return type`
    assert _symbol(inventory, "pkg.Pool").signatures == ()  # documented without parameters
    (compile_,) = _symbol(inventory, "pkg.compile").signatures  # optional brackets
    assert [(p.name, p.required) for p in compile_.parameters] == [
        ("source", True),
        ("filename", False),
        ("symbol", False),
    ]
    assert compile_.text == "pkg.compile(source, [filename], [symbol])"
    sources = {s.sources for s in inventory.symbols}
    assert all(src[0].type == "signature" and src[0].section_id for src in sources)


def test_version_directives_give_changes(tmp_path: Path) -> None:
    built = _api(tmp_path)
    assert [(c.symbol, c.parameter, c.kind, c.version) for c in built.inventory.changes] == [
        ("pkg.Pool", None, "deprecated", "3.0"),  # inside a note
        ("pkg.fetch", None, "deprecated", "2.0"),
        ("pkg.fetch", "timeout", "added", "1.1"),  # inside the parameter entry
    ]  # versionchanged gives no Change; "next" is not a PEP 440 version
    assert built.warnings == (
        "pkg.fetch: version directive in an unnamed parameter entry",  # not about all of fetch
        "pkg.fetch: versionremoved 'next' is not a PEP 440 version",
    )
    assert built.conflicts == ()
    fetch_section = _symbol(built.inventory, "pkg.fetch").sources
    assert all(c.sources == fetch_section for c in built.inventory.changes[1:])


def test_directive_outside_an_api_description_gives_no_change(tmp_path: Path) -> None:
    body = (
        "<section ids='g'><title>Guide</title><versionmodified type='deprecated' version='2.0'>"
        "<paragraph>Old.</paragraph></versionmodified></section>"
    )
    assert _api(tmp_path, body).inventory == Inventory(())


def test_same_symbol_documented_twice_is_one_symbol(tmp_path: Path) -> None:
    built = _api(
        tmp_path, API + API.replace('ids="api"', 'ids="again"').replace(">API<", ">Again<")
    )
    fetch = _symbol(built.inventory, "pkg.fetch")
    assert len(fetch.sources) == 2 and len(fetch.signatures) == 1
    assert len(fetch.signatures[0].sources) == 2
    assert [len(c.sources) for c in built.inventory.changes] == [2, 2, 2]
    assert built.conflicts == ()


def test_parts_of_a_section_are_read_in_order(tmp_path: Path) -> None:
    """A long description is split into parts; the first `Return type` wins in any input order."""
    filler = "<paragraph>" + "word " * 60 + "</paragraph>"
    returns = (
        "<field_list><field><field_name>Return type</field_name><field_body><paragraph>"
        "<literal_emphasis>{}</literal_emphasis></paragraph></field_body></field></field_list>"
    )
    body = (
        "<section ids='s'><title>S</title><desc domain='py' objtype='function'>"
        "<desc_signature fullname='split' module='pkg'><desc_name>split</desc_name>"
        f"<desc_parameterlist/></desc_signature><desc_content>{returns.format('A')}"
        f"{filler * 3}{returns.format('B')}</desc_content></desc></section>"
    )
    (tmp_path / "build-env.txt").write_text("sphinx-build 9.1.1\n", encoding="utf-8")
    document = f'<?xml version="1.0"?>\n<document source="/src/docs/api.rst">{body}</document>\n'
    (tmp_path / "api.xml").write_text(document, encoding="utf-8")
    xml = read_sphinx_xml(tmp_path)
    chunks = [c for d in xml.documents for c in chunk_blocks(d, project="pkg", soft_limit=80)]
    assert max(c.parts for c in chunks) > 1
    built = build_inventory(chunks)
    assert build_inventory(reversed(chunks)) == built
    (split,) = _symbol(built.inventory, "pkg.split").signatures
    assert split.returns is not None and split.returns.type == "A"


@pytest.mark.parametrize(
    ("annotation", "values"),
    [
        ("Literal['a, b', 'c']", ("'a, b'", "'c'")),
        ("typing.Literal[1, (2, 3)]", ("1", "(2, 3)")),
        (r"Literal['a\\', 'b']", (r"'a\\'", "'b'")),  # escaped backslash ends the string
        (r"Literal['it\'s', 'b']", (r"'it\'s'", "'b'")),  # an escaped quote does not
        ("Literal['a'] | Sequence[str]", None),  # not one Literal: no enum
        ("Literal['a', ]", None),
        ("Literal[]", None),
        ("list[Literal['a']]", None),
    ],
)
def test_literal_annotations_give_enums(annotation: str, values: tuple[str, ...] | None) -> None:
    source = (Source("signature", section_id="s" * 16),)
    constraints = _constraints(annotation, source)
    assert (constraints[0].values if constraints else None) == values


@pytest.mark.parametrize("style", ["napoleon", "numpydoc", "plain"])
def test_fixture_golden(style: str, golden: Golden) -> None:
    chunks = _read(FIXTURES / f"xml-{style}")
    built = build_inventory(chunks)
    assert build_inventory(reversed(chunks)) == built  # order of chunks does not matter
    golden(f"fixture-{style}", {"builder_version": INVENTORY_BUILDER_VERSION, "build": built})


@pytest.fixture(scope="module")
def urllib3() -> InventoryBuild:
    return build_inventory(_read(EXAMPLES / "urllib3" / "xml"))


def test_urllib3_deprecations(urllib3: InventoryBuild) -> None:
    fields = "urllib3.fields."
    assert [(c.symbol, c.parameter, c.kind, c.version) for c in urllib3.inventory.changes] == [
        (f"{fields}format_header_param", None, "deprecated", "2.0.0"),
        (f"{fields}format_header_param_html5", None, "deprecated", "2.0.0"),
        (f"{fields}format_header_param_rfc2231", None, "deprecated", "2.0.0"),
    ]  # the replacement is only in the directive's text: it comes from a change claim (D)
    assert all(c.replacement is None for c in urllib3.inventory.changes)
    assert urllib3.conflicts == () and urllib3.warnings == ()


def test_urllib3_signatures(urllib3: InventoryBuild) -> None:
    inventory = urllib3.inventory
    (request,) = _symbol(inventory, "urllib3.request").signatures
    kinds = {p.name: p.kind for p in request.parameters}
    assert kinds["url"] == "positional_or_keyword" and kinds["timeout"] == "keyword_only"
    assert {p.name: p.default for p in request.parameters}["timeout"] == "3"
    # two overloads that differ only in types stay two signatures
    wrap = _symbol(inventory, "urllib3.util.ssl_wrap_socket").signatures
    assert sorted(s.returns.type for s in wrap if s.returns) == [
        "SSLSocket",
        "ssl.SSLSocket | SSLTransportType",
    ]
    (readline,) = _symbol(inventory, "urllib3.response.HTTPResponse.readline").signatures
    assert [(p.name, p.kind) for p in readline.parameters] == [("size", "positional_only")]
    assert _symbol(inventory, "urllib3.util.Retry").kind == "class"


def test_hydra_zen_parameter_deprecations() -> None:
    built = build_inventory(_read(EXAMPLES / "hydra-zen" / "xml"))
    on_parameters = [(c.symbol, c.parameter) for c in built.inventory.changes if c.parameter]
    assert ("hydra_zen.builds", "frozen") in on_parameters
    assert len(built.inventory.changes) == 6 and len(on_parameters) == 5  # SPEC §6.3


def test_trio_has_no_version_directives() -> None:
    built = build_inventory(_read(EXAMPLES / "trio" / "xml"))
    assert built.inventory.changes == () and built.inventory.symbols
