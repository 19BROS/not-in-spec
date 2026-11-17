"""Python adapter: raw call records → `CallRecord`s through the inventory (SPEC §6.2, §6.10)."""

from collections.abc import Callable, Mapping
from typing import Any

import pytest

from notinspec.adapters.python import (
    ApiIndex,
    Argument,
    CallIssue,
    CallRecord,
    NormalizedCalls,
    Value,
    example_additions,
    merge_additions,
    normalize_calls,
    parse_python,
)
from notinspec.inventory import Inventory, Source, Symbol

type MakeInventory = Callable[[Mapping[str, Mapping[str, Any]]], Inventory]

ACME: dict[str, dict[str, Any]] = {
    "acme.request": {
        "kind": "function",
        "params": ["method", "url", "*", "timeout=3", "retries=None"],
        "returns": "Response",
    },
    "acme.Client": {"kind": "class", "params": ["host", "port=80", "**options"]},
    "acme.Client.get": {"kind": "method", "params": ["url", "*paths"], "returns": "Response"},
    "acme.Client.copy": {"kind": "method", "params": [], "returns": "Self"},
    "acme.Client.maybe": {"kind": "method", "params": [], "returns": "Response | None"},
    "acme.Client.status": {"kind": "attribute"},
    "acme.connect": {"kind": "function", "params": [], "returns": "Client"},
    "acme.response.Response": {"kind": "class", "params": ["body"]},
    "acme.response.Response.json": {"kind": "method", "params": []},
    "acme.util.Timeout": {"kind": "class", "params": ["connect=None", "read=None"]},
    "acme.util.Timeout.from_float": {"kind": "method", "params": ["value"], "returns": "Timeout"},
    "acme.a.Twin": {"kind": "class", "params": []},
    "acme.b.Twin": {"kind": "class", "params": []},
    "acme.pick": {
        "kind": "function",
        "signatures": [["a", "b"], ["a", "/", "*", "c"]],
    },
    "acme.legacy": {"kind": "function"},
    "acme.open_pool": {
        "kind": "function",
        "signatures": [["url"], {"params": ["url", "pool"], "returns": "Client"}],
    },
}


@pytest.fixture
def api(make_inventory: MakeInventory) -> ApiIndex:
    return ApiIndex(make_inventory(ACME))


def normalize(code: str, api: ApiIndex) -> NormalizedCalls:
    parsed = parse_python(code, "python")
    assert parsed.status == "ok", parsed.error
    return normalize_calls(parsed.calls, api)


def symbols(result: NormalizedCalls) -> list[tuple[str, str]]:
    return [(c.symbol, c.resolved_by) for c in result.calls]


def lit(value: object, source: str | None = None) -> Value:
    return Value("literal", source or repr(value), literal=value)  # type: ignore[arg-type]


def test_import_paths_exact_alias_and_through_a_class(api: ApiIndex) -> None:
    code = """\
import acme
from acme import Timeout
acme.request("GET", "/")
acme.util.Timeout()
Timeout(1)
acme.Timeout.from_float(2.0)
"""
    assert symbols(normalize(code, api)) == [
        ("acme.request", "exact"),
        ("acme.util.Timeout", "exact"),
        ("acme.util.Timeout", "alias"),
        ("acme.util.Timeout.from_float", "alias"),
    ]


def test_alias_with_several_candidates_is_ambiguous(api: ApiIndex) -> None:
    result = normalize("import acme\nacme.Twin()\n", api)
    assert result.calls == ()
    (unresolved,) = result.unresolved
    assert (unresolved.reason, unresolved.candidates) == (
        "ambiguous",
        ("acme.a.Twin", "acme.b.Twin"),
    )


def test_variable_type_from_class_and_return_types(api: ApiIndex) -> None:
    code = """\
import acme
client = acme.Client("example.com")
resp = client.get("/")
resp.json()
client.copy().get("/")
client.maybe().json()
acme.connect().get("/")
acme.util.Timeout.from_float(1.0).from_float(2.0)
"""
    assert symbols(normalize(code, api)) == [
        ("acme.Client", "exact"),
        ("acme.Client.get", "variable"),
        ("acme.response.Response.json", "variable"),
        ("acme.Client.copy", "variable"),
        ("acme.Client.get", "variable"),  # Self → Client
        ("acme.Client.maybe", "variable"),
        ("acme.response.Response.json", "variable"),  # Response | None → Response
        ("acme.connect", "exact"),
        ("acme.Client.get", "variable"),
        ("acme.util.Timeout.from_float", "exact"),
        ("acme.util.Timeout.from_float", "variable"),
    ]


def test_unknown_types_are_not_guessed(api: ApiIndex) -> None:
    code = """\
import acme, json
client = acme.Client("h")
client.status.upper()
client.missing()
json.loads("{}").get("a")
http.request("GET", "/")
"""
    result = normalize(code, api)
    assert symbols(result) == [("acme.Client", "exact")]
    assert [(u.symbol, u.reason, u.path) for u in result.unresolved] == [
        ("client.status.upper", "unknown-type", None),
        ("client.missing", "not-in-inventory", "acme.Client.missing"),
        ("json.loads", "not-in-inventory", "json.loads"),
        ("json.loads('{}').get", "unknown-type", None),
        ("http.request", "unknown-type", None),  # never matched to acme.request by its last name
    ]


def test_unbound_names(api: ApiIndex) -> None:
    code = """\
acme.request("GET", "/")
Client("h")
Timeout.from_float(1.0)
Twin()
print(1)
request("GET", "/")
"""
    result = normalize(code, api)
    assert symbols(result) == [
        ("acme.request", "name"),
        ("acme.Client", "name"),
        ("acme.util.Timeout.from_float", "name"),
        ("acme.request", "name"),
    ]
    assert [(u.symbol, u.reason) for u in result.unresolved] == [
        ("Twin", "ambiguous"),
        ("print", "not-in-inventory"),
    ]


def test_arguments_bind_like_python(api: ApiIndex) -> None:
    code = """\
import acme
acme.Client("h", 8080, verify=False, cert="c.pem")
acme.Client("h").get("/a", "b", "c")
"""
    client, _, get = normalize(code, api).calls
    assert client.args == (
        Argument("host", "host", (lit("h", "'h'"),)),
        Argument("port", "port", (lit(8080),)),
        Argument("cert", "options", (lit("c.pem", "'c.pem'"),)),  # extra keywords by name
        Argument("verify", "options", (lit(False),)),
    )
    assert (client.signature, client.issues, client.unmapped) == (0, (), ())
    assert get.args == (
        Argument("url", "url", (lit("/a", "'/a'"),)),
        Argument("paths", "paths", (lit("b", "'b'"), lit("c", "'c'"))),
    )


def test_keyword_order_does_not_matter(api: ApiIndex) -> None:
    one = normalize("import acme\nacme.Client(host='h', b=1, a=2)\n", api).calls[0]
    two = normalize("import acme\nacme.Client(a=2, b=1, host='h')\n", api).calls[0]
    assert one.args == two.args


def test_mismatches_are_issues_and_the_record_is_kept(api: ApiIndex) -> None:
    code = """\
import acme
acme.request("GET", "/", 10)
acme.request("GET", url="/", method="POST", timout=5)
acme.request(method="GET")
acme.request(*args)
acme.request("GET", **kw)
"""
    calls = normalize(code, api).calls
    assert [c.issues for c in calls] == [
        (CallIssue("too-many-positional", "10"),),
        (CallIssue("multiple-values", "method"), CallIssue("unknown-parameter", "timout")),
        (CallIssue("missing-required", "url"),),
        (CallIssue("unpacked", "*args"),),
        (CallIssue("unpacked", "**kw"),),
    ]
    assert calls[0].unmapped == (lit(10),)
    assert [a.name for a in calls[1].args] == ["method", "url"]
    assert calls[3].unmapped == (Value("unpack", "*args"),)


def test_the_first_signature_that_binds_cleanly_wins(api: ApiIndex) -> None:
    code = "import acme\nacme.pick(1, 2)\nacme.pick(1, c=3)\nacme.pick(1)\n"
    signatures = api.symbols["acme.pick"].signatures
    chosen = [
        ([p.name for p in signatures[c.signature].parameters], len(c.issues))
        for c in normalize(code, api).calls
        if c.signature is not None
    ]
    assert chosen == [(["a", "b"], 0), (["a", "c"], 0), (["a", "c"], 1)]  # a tie: the first


def test_symbol_without_signature_keeps_keywords(api: ApiIndex) -> None:
    (call,) = normalize("import acme\nacme.legacy(1, b=2, a=3)\n", api).calls
    assert call.signature is None
    assert [(a.name, a.parameter) for a in call.args] == [("a", None), ("b", None)]
    assert call.unmapped == (lit(1),)


def test_nested_call_values_point_to_their_records(api: ApiIndex) -> None:
    code = "import acme\nacme.request('GET', '/', timeout=acme.util.Timeout(read=2))\n"
    timeout, request = normalize(code, api).calls
    assert timeout.index == 0
    assert request.args[-1] == Argument(
        "timeout", "timeout", (Value("call", "acme.util.Timeout(read=2)", call=0),)
    )


def test_model_answer_and_example_give_the_same_record(api: ApiIndex) -> None:
    example = normalize('import acme\nc = acme.Client("h")\nc.get("/x")\n', api)
    answer = normalize('from acme import Client\nClient(host="h").get(url="/x")\n', api)
    assert [(c.symbol, c.args) for c in example.calls] == [(c.symbol, c.args) for c in answer.calls]


def test_additions_for_missing_symbols_of_the_project(api: ApiIndex) -> None:
    code = """\
import acme, json
acme.Session(retries=3, pool=2)
acme.Session(pool=4)
acme.helper(1)
acme.Client("h").close(force=True)
acme.Client("h", nope=1)
json.loads("{}")
print("x")
"""
    parsed = parse_python(code, "python")
    normalized = normalize_calls(parsed.calls, api)
    additions = example_additions(parsed.calls, normalized, api, "e" * 16)
    assert [(s.path, s.kind, [p.name for p in s.signatures[0].parameters]) for s in additions] == [
        ("acme.Client.close", "method", ["force"]),
        ("acme.Session", "class", ["pool", "retries"]),
        ("acme.helper", "function", []),
    ]
    source = Source("example", section_id="e" * 16)
    assert all(s.sources == (source,) for s in additions)
    assert all(
        p.sources == (source,) and not p.required for p in additions[1].signatures[0].parameters
    )


def issues(record: CallRecord) -> list[tuple[str, str]]:
    return [(i.kind, i.detail) for i in record.issues]


@pytest.mark.parametrize(
    ("code", "written"),
    [
        ("from acme.fake import Client\nClient('h')\n", "acme.fake.Client"),
        ("from acme.response import Timeout\nTimeout()\n", "acme.response.Timeout"),
        ("import acme\nacme.nonexistent.Timeout()\n", "acme.nonexistent.Timeout"),
        ("import acme.util.timeout as t\nt.Timeout()\n", "acme.util.timeout.Timeout"),
        ("import acme\nacme.fake.Timeout.from_float(1)\n", "acme.fake.Timeout.from_float"),
    ],
)
def test_alias_from_a_module_the_docs_do_not_name_is_wrong_module(
    code: str, written: str, api: ApiIndex
) -> None:
    (call,) = normalize(code, api).calls
    assert call.resolved_by == "alias"
    assert issues(call) == [("wrong-module", written)]


@pytest.mark.parametrize(
    "code",
    [
        "import acme\nacme.Timeout()\n",  # re-export at the package root
        "from acme import Timeout\nTimeout.from_float(1)\n",
        "from acme.util import Timeout\nTimeout()\n",  # the documented module itself
    ],
)
def test_reexport_above_the_documented_module_is_clean(code: str, api: ApiIndex) -> None:
    assert all(c.issues == () for c in normalize(code, api).calls)


def test_attribute_is_not_callable(api: ApiIndex) -> None:
    code = "import acme\nacme.Client.status()\nc = acme.Client('h')\nc.status()\n"
    direct, _, variable = normalize(code, api).calls
    assert (direct.symbol, issues(direct)) == (
        "acme.Client.status",
        [("not-callable", "attribute")],
    )
    assert (variable.resolved_by, issues(variable)) == ("variable", [("not-callable", "attribute")])


def test_return_type_comes_only_from_the_bound_signature(api: ApiIndex) -> None:
    code = "import acme\nacme.open_pool('u').get('/')\nacme.open_pool('u', 1).get('/')\n"
    result = normalize(code, api)
    signatures = api.symbols["acme.open_pool"].signatures
    assert [
        len(signatures[c.signature].parameters) for c in result.calls[:2] if c.signature is not None
    ] == [1, 2]
    assert [c.symbol for c in result.calls] == [
        "acme.open_pool",
        "acme.open_pool",
        "acme.Client.get",
    ]
    # the one-parameter overload documents no return type: not borrowed from the other one
    assert [(u.symbol, u.reason) for u in result.unresolved] == [
        ("acme.open_pool('u').get", "unknown-type")
    ]


def test_additions_for_a_symbol_without_signature(api: ApiIndex) -> None:
    parsed = parse_python("import acme\nacme.legacy(1, b=2)\nacme.request('GET', '/')\n", "python")
    normalized = normalize_calls(parsed.calls, api)
    (addition,) = example_additions(parsed.calls, normalized, api, "e" * 16)
    assert (addition.path, addition.kind) == ("acme.legacy", "function")  # the inventory's kind
    assert [p.name for p in addition.signatures[0].parameters] == ["b"]


def test_merge_additions_gives_one_symbol_per_path(api: ApiIndex) -> None:
    def additions(code: str, section: str) -> tuple[Symbol, ...]:
        parsed = parse_python(code, "python")
        return example_additions(parsed.calls, normalize_calls(parsed.calls, api), api, section)

    first = additions("import acme\nacme.Session(pool=1)\nacme.legacy(a=1)\n", "a" * 16)
    second = additions("import acme\nacme.Session(retries=2)\n", "b" * 16)
    merged = merge_additions([*first, *second])
    assert merged == merge_additions([*second, *first])
    session = next(s for s in merged.symbols if s.path == "acme.Session")
    (signature,) = session.signatures
    assert [p.name for p in signature.parameters] == ["pool", "retries"]
    sections = [s.section_id for s in session.sources]
    assert sections == ["a" * 16, "b" * 16]
    assert all(p.sources == signature.sources for p in signature.parameters)
    assert [s.path for s in merged.symbols] == ["acme.Session", "acme.legacy"]
