"""Python adapter: code → raw call records (SPEC §6.2, component C)."""

import pytest

from notinspec.adapters.python import Keyword, RawCallRecord, Value, accepts, parse_python


def calls(code: str, lang: str | None = "python") -> tuple[RawCallRecord, ...]:
    result = parse_python(code, lang)
    assert result.status == "ok", result.error
    return result.calls


def imported(path: str, source: str | None = None) -> Value:
    return Value("import", source or path, path=path)


def literal(value: object, source: str) -> Value:
    return Value("literal", source, literal=value)  # type: ignore[arg-type]


def test_import_forms_resolve_to_dotted_paths() -> None:
    code = """\
import urllib3
import urllib3.contrib.pyopenssl
import urllib3.util as u
from urllib3.util import Timeout as T, Retry
from . import local
from .pkg import thing
urllib3.contrib.pyopenssl.inject_into_urllib3()
u.make_headers()
T(10)
Retry()
local.f()
thing()
"""
    callees = [c.callee for c in calls(code)]
    assert callees == [
        imported("urllib3.contrib.pyopenssl.inject_into_urllib3"),
        imported("urllib3.util.make_headers", "u.make_headers"),
        imported("urllib3.util.Timeout", "T"),
        imported("urllib3.util.Retry", "Retry"),
        imported(".local.f", "local.f"),
        imported(".pkg.thing", "thing"),
    ]
    assert [c.symbol for c in calls(code)][:3] == [
        "urllib3.contrib.pyopenssl.inject_into_urllib3",
        "u.make_headers",
        "T",
    ]


def test_variable_holding_a_call_result_points_to_that_call() -> None:
    code = """\
import urllib3

http = urllib3.PoolManager(num_pools=50)
resp = http.request("GET", "https://example.com/")
print(resp.status)
"""
    pool, request, printed = calls(code)
    assert pool == RawCallRecord(
        index=0,
        line=3,
        end_line=3,
        symbol="urllib3.PoolManager",
        callee=imported("urllib3.PoolManager"),
        args=(),
        kwargs=(Keyword("num_pools", literal(50, "50")),),
    )
    assert request.callee == Value("call", "http.request", call=0, attrs=("request",))
    assert request.args == (
        literal("GET", "'GET'"),
        literal("https://example.com/", "'https://example.com/'"),
    )
    assert printed.callee == Value("name", "print", name="print")
    assert printed.args == (Value("call", "resp.status", call=1, attrs=("status",)),)


def test_calls_are_numbered_in_evaluation_order() -> None:
    code = """\
import urllib3
urllib3.request(
    "GET",
    "https://httpbin.org/redirect/3",
    retries=urllib3.Retry(3, redirect=2),
)
"""
    retry, request = calls(code)
    assert (retry.index, retry.symbol, retry.line, retry.end_line) == (0, "urllib3.Retry", 5, 5)
    assert (request.index, request.symbol, request.line, request.end_line) == (
        1,
        "urllib3.request",
        2,
        6,
    )
    assert request.kwargs == (
        Keyword("retries", Value("call", "urllib3.Retry(3, redirect=2)", call=0)),
    )


def test_chained_call_uses_the_inner_result_as_base() -> None:
    (inner, outer) = calls("make().close()\n")
    assert inner.callee == Value("name", "make", name="make")
    assert outer.callee == Value("call", "make().close", call=0, attrs=("close",))


def test_literal_variable_gives_the_same_value_as_the_literal() -> None:
    direct = calls("f(timeout=3.0)\n")[0].kwargs[0].value
    through = calls("t = 3.0\nf(timeout=t)\n")[0].kwargs[0].value
    assert direct == literal(3.0, "3.0")
    assert through == literal(3.0, "t")
    assert through.literal == direct.literal


def test_latest_binding_wins() -> None:
    code = """\
from urllib3 import PoolManager, ProxyManager
http = PoolManager()
http = ProxyManager("http://proxy")
http.request("GET", "/")
"""
    assert calls(code)[-1].callee == Value("call", "http.request", call=1, attrs=("request",))


def test_with_as_walrus_and_alias_bind_names() -> None:
    code = """\
from urllib3 import PoolManager
with PoolManager() as pool:
    pool.request("GET", "/")
other = pool
other.clear()
if (h := PoolManager()):
    h.clear()
"""
    records = calls(code)
    assert records[1].callee.call == 0
    assert records[2].callee == Value("call", "other.clear", call=0, attrs=("clear",))
    assert records[4].callee.call == 3


def test_attributes_of_variables_accumulate() -> None:
    code = "import io\nr = io.open('x')\nd = r.raw\nd.read(4)\n"
    assert calls(code)[-1].callee == Value("call", "d.read", call=0, attrs=("raw", "read"))


def test_unbound_names_keep_their_attributes() -> None:
    (record,) = calls('logging.getLogger("urllib3")\n')
    assert record.callee == Value("name", "logging.getLogger", name="logging", attrs=("getLogger",))


@pytest.mark.parametrize(
    "code",
    [
        "for http in items:\n    http.get()\n",
        "def f(http):\n    http.get()\n",
        "try:\n    pass\nexcept E as http:\n    http.get()\n",
        "[http.get() for http in items]\n",
        "lambda http: http.get()\n",
        "a, http = pair\nhttp.get()\n",
        "http += 1\nhttp.get()\n",
    ],
)
def test_local_rebinding_shadows_the_import(code: str) -> None:
    record = calls("import http\n" + code)[-1]
    assert record.symbol == "http.get"
    assert record.callee.kind == "expr"


def test_del_unbinds_a_name() -> None:
    record = calls("import http\ndel http\nhttp.get()\n")[-1]
    assert record.callee == Value("name", "http.get", name="http", attrs=("get",))


def test_calls_inside_functions_classes_and_control_flow_are_read() -> None:
    code = """\
import urllib3
@decorate(1)
def fetch(url=urllib3.util.Timeout(5)):
    return urllib3.request("GET", url)
class C(Base, metaclass=meta()):
    x = make()
try:
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass
while check():
    step()
match pick():
    case 1 if ok():
        done()
"""
    assert [c.symbol for c in calls(code)] == [
        "decorate",
        "urllib3.util.Timeout",
        "urllib3.request",
        "meta",
        "make",
        "urllib3.contrib.pyopenssl.inject_into_urllib3",
        "check",
        "step",
        "pick",
        "ok",
        "done",
    ]


def test_calls_in_assignment_targets_and_containers_are_read() -> None:
    code = "get().x = 1\nitems[key()] = [a(), {'k': b()}]\nf(*args(), **kw())\n"
    assert [c.symbol for c in calls(code)] == ["get", "a", "b", "key", "args", "kw", "f"]


def test_unpacking_arguments() -> None:
    (record,) = calls("f(1, *rest, key=2, **options)\n")
    assert record.args == (literal(1, "1"), Value("unpack", "*rest"))
    assert record.kwargs == (
        Keyword("key", literal(2, "2")),
        Keyword(None, Value("unpack", "**options")),
    )


def test_json_safe_literals() -> None:
    (record,) = calls(
        "f((1, [2.5, None]), {'a': True}, -3, b'x', {1}, 1j, 2**70, 99999999999999999999, ...)\n"
    )
    a, b, c, *rest = record.args
    assert a == literal((1, (2.5, None)), "(1, [2.5, None])")
    assert b == literal({"a": True}, "{'a': True}")
    assert c == literal(-3, "-3")
    assert [v.kind for v in rest] == ["expr"] * 6
    assert rest[0].source == "b'x'"


def test_prompts_are_stripped_and_lines_point_into_the_original() -> None:
    code = """\
>>> import urllib3
>>> resp = urllib3.request("GET",
...     "https://httpbin.org/robots.txt")
>>> resp.status
200
>>> resp.data
b"User-agent: *"
"""
    for lang in ("pycon", "python", "default", None):
        (record,) = calls(code, lang)
        assert (record.symbol, record.line, record.end_line) == ("urllib3.request", 2, 3)


def test_indented_code_is_dedented() -> None:
    (record,) = calls("    import a\n    a.b()\n")
    assert (record.callee, record.line) == (imported("a.b"), 2)


def test_syntax_error_in_python_is_invalid() -> None:
    result = parse_python('import urllib3\n\nresp.json()\n{\n  "num": 1,\n  ...\n}\n', "python")
    assert result.status == "invalid"
    assert result.calls == ()
    assert result.error is not None and result.error.startswith("SyntaxError")
    assert result.error.endswith("(line 6)")


def test_syntax_error_in_doctest_maps_the_line() -> None:
    result = parse_python(">>> a = 1\n>>> b = (\n...   2\n...   3)\n", "pycon")
    assert result.status == "invalid"
    assert result.error is not None and result.error.endswith("(line 3)")


def test_bad_prompt_indentation_is_invalid() -> None:
    result = parse_python("  >>> if x:\n... y()\n", "pycon")  # `...` less indented than `>>>`
    assert (result.status, result.calls) == ("invalid", ())
    assert result.error is not None and result.error.startswith("ValueError")


@pytest.mark.parametrize("lang", ["default", "none", None])
def test_shell_in_auto_language_is_not_python(lang: str | None) -> None:
    result = parse_python("$ python -m pip install urllib3\n", lang)
    assert result.status == "not-python"
    assert result.calls == ()


def test_null_bytes_are_rejected_not_raised() -> None:
    result = parse_python("f()\x00\n", "python")
    assert result.status == "invalid"


def test_deep_nesting_is_rejected_not_raised() -> None:
    result = parse_python("f(" * 10_000 + ")" * 10_000 + "\n", "python")
    assert result.status == "invalid"


def test_language_routing() -> None:
    for lang in ("python", "py", "python3", "pycon", "ipython", "default", None):
        assert accepts(lang)
    for lang in ("bash", "text", "json", "console", "math"):
        assert not accepts(lang)
    with pytest.raises(ValueError):
        parse_python("ls\n", "bash")


def test_same_code_same_records() -> None:
    code = "import urllib3\nurllib3.request('GET', 'https://x', retries=urllib3.Retry(3))\n"
    assert parse_python(code, "python") == parse_python(code, "python")
