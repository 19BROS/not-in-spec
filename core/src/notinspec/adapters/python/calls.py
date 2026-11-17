"""Python code → raw call records, with Python's own `ast` (SPEC §6.2, component C).

A **raw** call record keeps the call as written: the callee and the positional and named
arguments. It knows nothing about the API. Mapping it onto the inventory (variable → class,
positional argument → `Parameter`, dropping calls that are not the documented API) is the
next step and needs the inventory; this module never sees it.

What the adapter does resolve is the code's own, purely syntactic data flow, in source order:
a name refers to its latest binding in the example, which is

- an import: `import urllib3` / `from urllib3.util import Timeout as T` → `import` value with
  the dotted path (`urllib3`, `urllib3.util.Timeout`); attributes extend the path;
- the result of a call: `http = urllib3.PoolManager()` (also `with … as`, `:=`, `x = y`) →
  `call` value with the index of that call; attributes read from it go to `attrs`
  (`http.request` → call 0, attrs `("request",)`);
- a literal: `timeout = 3.0` → `literal` value 3.0 (so `f(timeout=timeout)` and
  `f(timeout=3.0)` give the same record);
- anything else (loop variable, `except … as e`, computed value) → `expr`.

A name never bound in the example (`print`, or `http` in a snippet that starts mid-way) is a
`name` value. Control flow is ignored: statements are read top to bottom, function and class
bodies in place, so the latest binding in the text wins.

Calls are numbered in evaluation order: the callee's base and the arguments come before the
call itself (`request(retries=Retry(3))` → `Retry` is 0, `request` is 1), so a record only
ever refers to earlier records.

Rules for one example's code (`parse_python`):

- `>>>` prompts are stripped with `doctest`'s own parser; output lines are dropped. A `pycon`
  block (also Sphinx `doctest_block`) is read as a session when any line is a prompt, any
  other block when its first line is one; otherwise it is plain code. Line numbers always
  point into the original code.
- An explicit Python language that does not parse is `invalid` (a `Finding` later, SPEC §6.2).
  The error is only its kind and line (`SyntaxError (line 3)`): CPython's wording changes
  between minor versions, and the same code must give the same record.
  Sphinx's `default` language (and no language) means "Python if it parses", so a shell
  session or program output there is `not-python`, not an error.
"""

import ast
import math
import re
import textwrap
import warnings
from dataclasses import dataclass, field, replace
from typing import Literal

from notinspec.adapters.python.prompts import Source, has_prompts, plain, strip_prompts

# bump when the records for the same code change
PYTHON_ADAPTER_VERSION = 1

# lower-case code-block languages (Sphinx `language`, Markdown fence info)
PYTHON_LANGS = frozenset({"python", "python3", "py", "py3", "pycon", "ipython", "ipython3"})
PROMPT_LANGS = frozenset({"pycon"})
# Sphinx `highlight_language` default: Python if it parses, else plain text
AUTO_LANGS = frozenset({"default", "none"})

type JsonValue = str | int | float | bool | None | tuple["JsonValue", ...] | dict[str, "JsonValue"]
type ValueKind = Literal["literal", "call", "import", "name", "unpack", "expr"]
type ParseStatus = Literal["ok", "invalid", "not-python"]

_INT_LIMIT = 2**63  # orjson (canonical JSON) serializes 64-bit integers only


@dataclass(frozen=True)
class Value:
    """An argument, a callee or what a name is bound to. Only the fields of `kind` are set."""

    kind: ValueKind
    source: str  # as written, spelled by `ast.unparse`: "urllib3.Timeout(connect=1.0)", "http"
    # literal: the value; tuples and lists both become tuples. Not hashed: it can hold a dict
    literal: JsonValue = field(default=None, hash=False)
    call: int | None = None  # call: index of the call record whose result this is
    path: str | None = None  # import: dotted path ("urllib3.util.Timeout"), attributes included
    name: str | None = None  # name: identifier not bound in the example ("print", "http")
    attrs: tuple[str, ...] = ()  # call, name: attributes read after the base ("request",)


@dataclass(frozen=True)
class Keyword:
    name: str | None  # None for `**mapping` (then `value` is an `unpack` value)
    value: Value


@dataclass(frozen=True)
class RawCallRecord:
    index: int  # 0-based, evaluation order within the example
    line: int  # 1-based, inclusive, in the example's code (prompts included)
    end_line: int
    symbol: str  # the callee as written: "urllib3.PoolManager", "http.request", "print"
    callee: Value
    args: tuple[Value, ...]  # positional, in order; `*xs` is an `unpack` value
    kwargs: tuple[Keyword, ...]  # in source order


@dataclass(frozen=True)
class PythonCode:
    status: ParseStatus
    calls: tuple[RawCallRecord, ...]
    error: str | None = None  # invalid / not-python: why it did not parse


def accepts(lang: str | None) -> bool:
    """True if a code block in this language goes to the Python adapter."""
    return lang is None or lang in PYTHON_LANGS or lang in AUTO_LANGS


def parse_python(code: str, lang: str | None) -> PythonCode:
    """Raw call records of one code block. Pure: same code + language ⇒ equal result."""
    if not accepts(lang):
        raise ValueError(f"not a Python language: {lang!r}")
    failed: ParseStatus = "invalid" if lang in PYTHON_LANGS else "not-python"
    try:
        prompts = has_prompts(code, anywhere=lang in PROMPT_LANGS)
        source = strip_prompts(code) if prompts else plain(textwrap.dedent(code))
    except ValueError as error:  # inconsistent indentation after a prompt
        match = re.search(r"\bline (\d+)\b", str(error))
        return PythonCode(failed, (), f"bad prompt ({match[0] if match else 'line ?'})")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # SyntaxWarning for invalid escapes in examples
            tree = ast.parse(source.text)
    except SyntaxError as error:
        # never `error.msg`: CPython rewords it between minor versions
        return PythonCode(failed, (), f"SyntaxError (line {_map_line(source, error.lineno or 1)})")
    except (ValueError, RecursionError, MemoryError) as error:  # null bytes, deep nesting
        return PythonCode(failed, (), type(error).__name__)
    try:
        calls = _Reader(source).module(tree)
    except RecursionError:
        return PythonCode(failed, (), "RecursionError")
    return PythonCode("ok", calls)


def _map_line(source: Source, line: int) -> int:
    if not source.line_map:
        return line
    return source.line_map[min(max(line, 1), len(source.line_map)) - 1]


type _Env = dict[str, Value]


class _Reader:
    def __init__(self, source: Source) -> None:
        self.source = source
        self.calls: list[RawCallRecord] = []
        # inside a class body: the scope its methods see (Python skips the class scope)
        self.function_scope: _Env | None = None

    def module(self, tree: ast.Module) -> tuple[RawCallRecord, ...]:
        self.block(tree.body, {})
        return tuple(self.calls)

    # statements

    def block(self, body: list[ast.stmt], env: _Env) -> None:
        for statement in body:
            self.statement(statement, env)

    def statement(self, node: ast.stmt, env: _Env) -> None:
        match node:
            case ast.Import(names=names):
                for alias in names:
                    if alias.asname:
                        env[alias.asname] = _imported(alias.name)
                    else:
                        top = alias.name.split(".")[0]
                        env[top] = _imported(top)
            case ast.ImportFrom(module=module, names=names, level=level):
                base = "." * level + (module or "")
                for alias in names:
                    if alias.name == "*":
                        continue
                    path = alias.name if not base else _join(base, alias.name)
                    env[alias.asname or alias.name] = _imported(path)
            case ast.Assign(targets=targets, value=value):
                bound = self.expr(value, env)
                for target in targets:
                    self.bind(target, bound, env)
            case ast.AnnAssign(target=target, value=value):
                if value is not None:
                    self.bind(target, self.expr(value, env), env)
            case ast.AugAssign(target=target, value=value):
                self.expr(value, env)
                self.bind(target, _opaque(target), env)
            case ast.With(items=items, body=body) | ast.AsyncWith(items=items, body=body):
                for item in items:
                    bound = self.expr(item.context_expr, env)
                    if item.optional_vars is not None:
                        self.bind(item.optional_vars, bound, env)
                self.block(body, env)
            case (
                ast.For(target=target, iter=it, body=body, orelse=orelse)
                | ast.AsyncFor(target=target, iter=it, body=body, orelse=orelse)
            ):
                self.expr(it, env)
                self.bind(target, _opaque(target), env)
                self.block(body, env)
                self.block(orelse, env)
            case ast.Try() | ast.TryStar():
                self.block(node.body, env)
                for handler in node.handlers:
                    if handler.type is not None:
                        self.expr(handler.type, env)
                    if handler.name:
                        env[handler.name] = Value("expr", handler.name)
                    self.block(handler.body, env)
                self.block(node.orelse, env)
                self.block(node.finalbody, env)
            case ast.FunctionDef() | ast.AsyncFunctionDef():
                for decorator in node.decorator_list:
                    self.expr(decorator, env)
                inner = self.arguments(node.args, env)
                outer, self.function_scope = self.function_scope, None
                self.block(node.body, inner)
                self.function_scope = outer
                env[node.name] = Value("expr", node.name)
            case ast.ClassDef():
                for expression in (*node.decorator_list, *node.bases):
                    self.expr(expression, env)
                for keyword in node.keywords:
                    self.expr(keyword.value, env)
                outer = self.function_scope
                self.function_scope = env if outer is None else outer
                self.block(node.body, dict(env))
                self.function_scope = outer
                env[node.name] = Value("expr", node.name)
            case ast.Delete(targets=targets):
                for target in targets:
                    if isinstance(target, ast.Name):
                        env.pop(target.id, None)
                    else:
                        self.children(target, env)
            case _:  # Expr, If, While, Return, Raise, Assert, Match, ...: in order
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, ast.stmt):
                        self.statement(child, env)
                    elif isinstance(child, ast.expr):
                        self.expr(child, env)
                    elif isinstance(child, ast.match_case):
                        if child.guard is not None:
                            self.expr(child.guard, env)
                        self.block(child.body, env)

    def bind(self, target: ast.expr, value: Value, env: _Env) -> None:
        match target:
            case ast.Name(id=name):
                env[name] = value
            case ast.Tuple(elts=elts) | ast.List(elts=elts):
                for element in elts:
                    self.bind(element, _opaque(element), env)
            case ast.Starred(value=inner):
                self.bind(inner, _opaque(inner), env)
            case _:  # attribute or item assignment: binds no name, may contain calls
                self.children(target, env)

    def arguments(self, args: ast.arguments, env: _Env) -> _Env:
        """Evaluate defaults in `env`; return the body's scope with the parameters unbound.

        In a class body the body's scope starts from the enclosing scope, not the class's.
        """
        for default in (*args.defaults, *(d for d in args.kw_defaults if d is not None)):
            self.expr(default, env)
        inner = dict(env if self.function_scope is None else self.function_scope)
        every = (*args.posonlyargs, *args.args, *args.kwonlyargs, args.vararg, args.kwarg)
        for arg in every:
            if arg is not None:
                inner[arg.arg] = Value("expr", arg.arg)
        return inner

    # expressions

    def expr(self, node: ast.expr, env: _Env) -> Value:
        match node:
            case ast.Call():
                return self.call(node, env)
            case ast.Name(id=name):
                bound = env.get(name)
                if bound is None:
                    return Value("name", name, name=name)
                return replace(bound, source=name)
            case ast.Attribute():
                return self.attribute(node, env)
            case ast.NamedExpr(target=target, value=value):
                bound = self.expr(value, env)
                self.bind(target, bound, env)
                return replace(bound, source=ast.unparse(node))
            case ast.Lambda(args=args, body=body):
                self.expr(body, self.arguments(args, env))
                return _opaque(node)
            case ast.ListComp() | ast.SetComp() | ast.GeneratorExp() | ast.DictComp():
                self.comprehension(node, env)
                return _opaque(node)
            case ast.Constant() | ast.List() | ast.Tuple() | ast.Dict() | ast.UnaryOp():
                literal = _literal(node)
                if literal is not None:
                    return literal
        self.children(node, env)
        return _opaque(node)

    def children(self, node: ast.AST, env: _Env) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.expr):
                self.expr(child, env)
            elif isinstance(child, ast.keyword):
                self.expr(child.value, env)

    def comprehension(
        self, node: ast.ListComp | ast.SetComp | ast.GeneratorExp | ast.DictComp, env: _Env
    ) -> None:
        inner = dict(env)
        for number, generator in enumerate(node.generators):
            self.expr(generator.iter, env if number == 0 else inner)
            self.bind(generator.target, _opaque(generator.target), inner)
            for condition in generator.ifs:
                self.expr(condition, inner)
        if isinstance(node, ast.DictComp):
            self.expr(node.key, inner)
            self.expr(node.value, inner)
        else:
            self.expr(node.elt, inner)

    def attribute(self, node: ast.Attribute, env: _Env) -> Value:
        attrs: list[str] = []
        base: ast.expr = node
        while isinstance(base, ast.Attribute):
            attrs.append(base.attr)
            base = base.value
        attrs.reverse()
        value = self.expr(base, env)
        source = ast.unparse(node)
        if value.kind == "import" and value.path is not None:
            return Value("import", source, path=".".join((value.path, *attrs)))
        if value.kind in ("call", "name"):
            return replace(value, source=source, attrs=(*value.attrs, *attrs))
        return _opaque(node)

    def call(self, node: ast.Call, env: _Env) -> Value:
        callee = self.expr(node.func, env)
        args = tuple(self.argument(arg, env) for arg in node.args)
        kwargs = tuple(
            Keyword(k.arg, self.expr(k.value, env))
            if k.arg is not None
            else Keyword(None, self.unpack(k.value, "**", env))
            for k in node.keywords
        )
        index = len(self.calls)
        self.calls.append(
            RawCallRecord(
                index=index,
                line=_map_line(self.source, node.lineno),
                end_line=_map_line(self.source, node.end_lineno or node.lineno),
                symbol=ast.unparse(node.func),
                callee=callee,
                args=args,
                kwargs=kwargs,
            )
        )
        return Value("call", ast.unparse(node), call=index)

    def argument(self, node: ast.expr, env: _Env) -> Value:
        if isinstance(node, ast.Starred):
            return self.unpack(node.value, "*", env)
        return self.expr(node, env)

    def unpack(self, node: ast.expr, stars: str, env: _Env) -> Value:
        self.expr(node, env)
        return Value("unpack", stars + ast.unparse(node))


def _imported(path: str) -> Value:
    return Value("import", path, path=path)


def _join(base: str, name: str) -> str:
    return base + name if base.endswith(".") else f"{base}.{name}"


def _opaque(node: ast.AST) -> Value:
    return Value("expr", ast.unparse(node))


def _literal(node: ast.expr) -> Value | None:
    try:
        value = ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return None
    ok, converted = _json(value)
    return Value("literal", ast.unparse(node), literal=converted) if ok else None


def _json(value: object) -> tuple[bool, JsonValue]:
    """The value in a form canonical JSON keeps exactly, or (False, None)."""
    if value is None or isinstance(value, (bool, str)):
        return True, value
    if isinstance(value, int):
        return (True, value) if -_INT_LIMIT <= value < _INT_LIMIT else (False, None)
    if isinstance(value, float):
        return (True, value) if math.isfinite(value) else (False, None)
    if isinstance(value, (tuple, list)):
        items = [_json(item) for item in value]
        if all(ok for ok, _ in items):
            return True, tuple(item for _, item in items)
        return False, None
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        pairs = {key: _json(item) for key, item in value.items()}
        if all(ok for ok, _ in pairs.values()):
            return True, {key: item for key, (_, item) in pairs.items()}
    return False, None
