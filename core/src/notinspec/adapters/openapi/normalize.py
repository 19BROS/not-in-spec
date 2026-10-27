"""Turn a parsed OpenAPI document into flat, complete operation "cards".

Everything downstream (claims, snippets, name index) works on this output, never on raw YAML.
Rules (see docs/input-adapters/Input_Adapters_Role_Guide.md §6):

- path-level and operation-level parameters are merged; the operation wins on the same name + in
  (header names compare case-insensitively)
- the request body is read from the first configured media type the operation offers
- effective security: the operation's `security` if present, else the global one
- body schemas are flattened into fields: `allOf` merges properties and `required`;
  for `oneOf` / `anyOf` a field is required only if it is required in every branch;
  `readOnly` properties are skipped; nested objects go at most MAX_FIELD_DEPTH levels deep and
  use dotted names (`shipping.address`); arrays are not descended into
- recursive schemas stop at the first repeat of a `$ref`

Broken pieces (bad refs, parameters without a name, ...) are skipped and reported in
`problems`; they never stop the whole spec.
"""

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from notinspec.adapters.openapi.refs import RefError, Resolved, Resolver, join

HTTP_METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")
PARAMETER_LOCATIONS = ("path", "query", "header", "cookie")
DEFAULT_BODY_MEDIA_TYPES = ("application/json", "application/x-www-form-urlencoded")
MAX_FIELD_DEPTH = 2
_MAX_UNION_DEPTH = 32  # guards oneOf-inside-oneOf chains that never hit a repeated ref

JsonScalar = str | int | float | bool | None


@dataclass(frozen=True)
class NormalizedField:
    location: str  # path | query | header | cookie | body
    name: str  # dotted for nested body fields: "shipping.address"
    type: str | None  # "string"; unions joined and sorted: "object|string"; None if unknown
    required: bool
    enum: tuple[JsonScalar, ...] | None
    deprecated: bool
    description: str | None
    example: Any  # None when the spec has no example
    source: str  # JSON pointer to where the parameter / property is defined


@dataclass(frozen=True)
class NormalizedOperation:
    method: str  # upper case: "POST"
    path: str
    operation_id: str | None
    summary: str | None
    description: str | None
    tags: tuple[str, ...]  # in spec order; the first one decides the slice
    deprecated: bool
    parameters: tuple[NormalizedField, ...]  # sorted by location, then name
    body_media_type: str | None  # None: no body, or only in media types we don't read
    body_required: bool
    body_fields: tuple[NormalizedField, ...]  # sorted by name
    # alternatives (OR) of scheme sets (AND). () = no auth; ((),) = auth optional
    security: tuple[tuple[str, ...], ...]
    source: str


@dataclass(frozen=True)
class SecurityScheme:
    name: str  # key in components.securitySchemes
    type: str  # apiKey | http | oauth2 | openIdConnect | mutualTLS
    scheme: str | None  # http only, lower case: "bearer", "basic"
    location: str | None  # apiKey only: header | query | cookie
    param_name: str | None  # apiKey only: header / query / cookie name
    source: str


@dataclass(frozen=True)
class NormalizedSpec:
    openapi_version: str
    title: str | None
    api_version: str | None
    operations: tuple[NormalizedOperation, ...]  # sorted by path, then method
    security_schemes: tuple[SecurityScheme, ...]  # sorted by name
    problems: tuple[str, ...]  # sorted, de-duplicated `pointer: message` lines


def normalize(
    document: Mapping[str, Any], *, body_media_types: Sequence[str] = DEFAULT_BODY_MEDIA_TYPES
) -> NormalizedSpec:
    """Normalize a parsed OpenAPI 3.x document. Pure: same document → equal result."""
    return _Normalizer(document, body_media_types).run()


@dataclass(frozen=True)
class _SchemaInfo:
    type: str | None = None
    enum: tuple[JsonScalar, ...] | None = None
    description: str | None = None
    example: Any = None
    deprecated: bool = False
    read_only: bool = False


@dataclass
class _Prop:
    schema: Any
    pointer: str
    required: bool
    stack: tuple[str, ...]  # refs followed on the way here, for the cycle guard


class _Normalizer:
    def __init__(self, document: Mapping[str, Any], body_media_types: Sequence[str]) -> None:
        self.doc = document
        self.resolver = Resolver(document)
        self.media_types = tuple(m.lower() for m in body_media_types)
        self.problems: set[str] = set()

    def run(self) -> NormalizedSpec:
        info = _dict(self.doc.get("info"))
        schemes = self.security_schemes()
        global_security = self.doc.get("security")
        operations: list[NormalizedOperation] = []
        for path, item, pointer in self.path_items():
            path_params = item.get("parameters")
            for method in HTTP_METHODS:
                op = item.get(method)
                if isinstance(op, dict):
                    operations.append(
                        self.operation(
                            path,
                            method,
                            op,
                            join(pointer, method),
                            path_params,
                            join(pointer, "parameters"),
                            global_security,
                        )
                    )
        known = {s.name for s in schemes}
        for op in operations:
            for name in sorted({n for alt in op.security for n in alt} - known):
                self.problem(op.source, f"unknown security scheme {name!r}")
        operations.sort(key=lambda o: (o.path, o.method))
        return NormalizedSpec(
            openapi_version=str(self.doc.get("openapi", "")),
            title=_str(info.get("title")),
            api_version=_str(info.get("version")),
            operations=tuple(operations),
            security_schemes=schemes,
            problems=tuple(sorted(self.problems)),
        )

    # --- helpers -------------------------------------------------------------------------

    def problem(self, pointer: str, message: str) -> None:
        self.problems.add(f"{pointer}: {message}")

    def resolve(self, node: Any, pointer: str) -> Resolved | None:
        try:
            return self.resolver.resolve(node, pointer)
        except RefError as exc:
            self.problem(pointer, str(exc))
            return None

    # --- paths and operations ------------------------------------------------------------

    def path_items(self) -> Iterator[tuple[str, dict[str, Any], str]]:
        paths = self.doc.get("paths")
        if not isinstance(paths, dict):
            return
        for path, raw in paths.items():
            if path.startswith("x-"):
                continue
            pointer = join("#/paths", path)
            if not path.startswith("/"):
                self.problem(pointer, "path does not start with '/'")
                continue
            resolved = self.resolve(raw, pointer)
            if resolved is not None and isinstance(resolved.node, dict):
                yield path, resolved.node, resolved.pointer

    def operation(
        self,
        path: str,
        method: str,
        op: dict[str, Any],
        pointer: str,
        path_params: Any,
        path_params_pointer: str,
        global_security: Any,
    ) -> NormalizedOperation:
        merged: dict[tuple[str, str], NormalizedField] = {}
        for raw, ptr in (
            (path_params, path_params_pointer),
            (op.get("parameters"), join(pointer, "parameters")),
        ):
            for param in self.parameters(raw, ptr):
                key_name = param.name.lower() if param.location == "header" else param.name
                merged[(param.location, key_name)] = param
        parameters = sorted(
            merged.values(), key=lambda f: (PARAMETER_LOCATIONS.index(f.location), f.name)
        )
        media_type, body_required, body_fields = self.request_body(
            op.get("requestBody"), join(pointer, "requestBody")
        )
        security = op["security"] if "security" in op else global_security
        return NormalizedOperation(
            method=method.upper(),
            path=path,
            operation_id=_str(op.get("operationId")),
            summary=_str(op.get("summary")),
            description=_str(op.get("description")),
            tags=tuple(t for t in _list(op.get("tags")) if isinstance(t, str)),
            deprecated=op.get("deprecated") is True,
            parameters=tuple(parameters),
            body_media_type=media_type,
            body_required=body_required,
            body_fields=body_fields,
            security=self.security(security, pointer),
            source=pointer,
        )

    def parameters(self, raw: Any, pointer: str) -> Iterator[NormalizedField]:
        if raw is None:
            return
        if not isinstance(raw, list):
            self.problem(pointer, "parameters is not a list")
            return
        for i, item in enumerate(raw):
            resolved = self.resolve(item, join(pointer, i))
            if resolved is None:
                continue
            node, ptr = resolved.node, resolved.pointer
            name, location = (
                (node.get("name"), node.get("in")) if isinstance(node, dict) else (None, None)
            )
            if not isinstance(name, str) or location not in PARAMETER_LOCATIONS:
                self.problem(ptr, "parameter without a valid name / in")
                continue
            schema, schema_ptr = node.get("schema"), join(ptr, "schema")
            content = node.get("content")
            if schema is None and isinstance(content, dict) and content:
                media_type, media = next(iter(content.items()))
                schema, schema_ptr = (
                    _dict(media).get("schema"),
                    join(ptr, "content", media_type, "schema"),
                )
            info = self.schema_info(schema, schema_ptr, ())
            yield NormalizedField(
                location=location,
                name=name,
                type=info.type,
                required=location == "path" or node.get("required") is True,
                enum=info.enum,
                deprecated=node.get("deprecated") is True or info.deprecated,
                description=_str(node.get("description")) or info.description,
                example=node["example"] if "example" in node else info.example,
                source=ptr,
            )

    def request_body(
        self, raw: Any, pointer: str
    ) -> tuple[str | None, bool, tuple[NormalizedField, ...]]:
        if raw is None:
            return None, False, ()
        resolved = self.resolve(raw, pointer)
        if resolved is None or not isinstance(resolved.node, dict):
            return None, False, ()
        body, ptr = resolved.node, resolved.pointer
        required = body.get("required") is True
        content = body.get("content")
        if not isinstance(content, dict):
            return None, required, ()
        by_base: dict[str, str] = {}
        for media_type in content:
            by_base.setdefault(media_type.split(";")[0].strip().lower(), media_type)
        chosen = next((by_base[m] for m in self.media_types if m in by_base), None)
        if chosen is None:
            return None, required, ()
        schema = _dict(content[chosen]).get("schema")
        fields: list[NormalizedField] = []
        self.body_fields(schema, join(ptr, "content", chosen, "schema"), (), "", 1, True, fields)
        fields.sort(key=lambda f: f.name)
        return chosen, required, tuple(fields)

    # --- schemas -------------------------------------------------------------------------

    def body_fields(
        self,
        schema: Any,
        pointer: str,
        stack: tuple[str, ...],
        prefix: str,
        depth: int,
        parent_required: bool,
        out: list[NormalizedField],
    ) -> None:
        for name, prop in self.properties(schema, pointer, stack).items():
            info = self.schema_info(prop.schema, prop.pointer, prop.stack)
            if info.read_only:
                continue
            required = parent_required and prop.required
            full_name = prefix + name
            out.append(
                NormalizedField(
                    location="body",
                    name=full_name,
                    type=info.type,
                    required=required,
                    enum=info.enum,
                    deprecated=info.deprecated,
                    description=info.description,
                    example=info.example,
                    source=prop.pointer,
                )
            )
            if depth < MAX_FIELD_DEPTH and info.type and "object" in info.type.split("|"):
                self.body_fields(
                    prop.schema, prop.pointer, prop.stack, full_name + ".", depth + 1, required, out
                )

    def properties(self, schema: Any, pointer: str, stack: tuple[str, ...]) -> dict[str, _Prop]:
        """Properties of one object schema, flattened over allOf / oneOf / anyOf (one level)."""
        resolved = self.resolve(schema, pointer)
        if resolved is None or not isinstance(resolved.node, dict):
            return {}
        if any(ref in stack for ref in resolved.refs):
            return {}  # recursive schema: stop at the first repeat
        if len(stack) > _MAX_UNION_DEPTH:
            return {}
        node, ptr, stack = resolved.node, resolved.pointer, stack + resolved.refs
        result: dict[str, _Prop] = {}
        for name, sub in _dict(node.get("properties")).items():
            result[name] = _Prop(sub, join(ptr, "properties", name), False, stack)
        for i, part in enumerate(_list(node.get("allOf"))):
            for name, prop in self.properties(part, join(ptr, "allOf", i), stack).items():
                if name in result:
                    result[name].required = result[name].required or prop.required
                else:
                    result[name] = prop
        for key in ("oneOf", "anyOf"):
            branches = [
                self.properties(b, join(ptr, key, i), stack)
                for i, b in enumerate(_list(node.get(key)))
            ]
            for name in _ordered_names(branches):
                present = [b[name] for b in branches if name in b]
                required = len(present) == len(branches) and all(p.required for p in present)
                if name in result:
                    result[name].required = result[name].required or required
                else:
                    first = present[0]
                    result[name] = _Prop(first.schema, first.pointer, required, first.stack)
        for name in _list(node.get("required")):
            if isinstance(name, str) and name in result:
                result[name].required = True
        return result

    def schema_info(self, schema: Any, pointer: str, stack: tuple[str, ...]) -> _SchemaInfo:
        """Type, enum and docs of one schema, looking through refs and oneOf / anyOf / allOf."""
        resolved = self.resolve(schema, pointer)
        if resolved is None or not isinstance(resolved.node, dict):
            return _SchemaInfo()
        node, ptr = resolved.node, resolved.pointer
        recursive = any(ref in stack for ref in resolved.refs) or len(stack) > _MAX_UNION_DEPTH
        stack = stack + resolved.refs

        types: set[str] = set()
        raw_type = node.get("type")
        if isinstance(raw_type, str):
            types.add(raw_type)
        elif isinstance(raw_type, list):
            types.update(t for t in raw_type if isinstance(t, str))
        types.discard("null")
        if not types and isinstance(node.get("properties"), dict):
            types.add("object")
        elif not types and "items" in node:
            types.add("array")
        enum = _enum(node)

        if not types and not recursive:
            for key in ("oneOf", "anyOf", "allOf"):
                parts = [
                    self.schema_info(b, join(ptr, key, i), stack)
                    for i, b in enumerate(_list(node.get(key)))
                ]
                if not parts:
                    continue
                for part in parts:
                    types.update(part.type.split("|") if part.type else ())
                if enum is None and key != "allOf" and all(p.enum is not None for p in parts):
                    enum = _dedupe(v for p in parts for v in (p.enum or ()))
                elif enum is None and key == "allOf":
                    enum = next((p.enum for p in parts if p.enum is not None), None)
                break

        # in 3.1 a description may sit next to a $ref; it describes this use, so it wins
        wrapper = schema if isinstance(schema, dict) else {}
        description = _str(wrapper.get("description")) or _str(node.get("description"))
        examples = node.get("examples")
        if "example" in node:
            example = node["example"]
        elif isinstance(examples, list) and examples:
            example = examples[0]
        else:
            example = None
        return _SchemaInfo(
            type="|".join(sorted(types)) or None,
            enum=enum,
            description=description,
            example=example,
            deprecated=node.get("deprecated") is True,
            read_only=node.get("readOnly") is True or wrapper.get("readOnly") is True,
        )

    # --- security ------------------------------------------------------------------------

    def security(self, raw: Any, pointer: str) -> tuple[tuple[str, ...], ...]:
        if raw is None:
            return ()
        if not isinstance(raw, list):
            self.problem(pointer, "security is not a list")
            return ()
        alternatives: list[tuple[str, ...]] = []
        for requirement in raw:
            if isinstance(requirement, dict):
                alt = tuple(sorted(str(k) for k in requirement))
                if alt not in alternatives:
                    alternatives.append(alt)
        return tuple(alternatives)

    def security_schemes(self) -> tuple[SecurityScheme, ...]:
        raw = _dict(_dict(self.doc.get("components")).get("securitySchemes"))
        schemes: list[SecurityScheme] = []
        for name, item in sorted(raw.items()):
            resolved = self.resolve(item, join("#/components/securitySchemes", name))
            if resolved is None or not isinstance(resolved.node, dict):
                continue
            node = resolved.node
            kind = _str(node.get("type"))
            if kind is None:
                self.problem(resolved.pointer, "security scheme without a type")
                continue
            scheme = _str(node.get("scheme")) if kind == "http" else None
            schemes.append(
                SecurityScheme(
                    name=name,
                    type=kind,
                    scheme=scheme.lower() if scheme else None,
                    location=_str(node.get("in")) if kind == "apiKey" else None,
                    param_name=_str(node.get("name")) if kind == "apiKey" else None,
                    source=resolved.pointer,
                )
            )
        return tuple(schemes)


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _str(value: Any) -> str | None:
    return value if isinstance(value, str) and value != "" else None


def _ordered_names(branches: list[dict[str, _Prop]]) -> list[str]:
    names: dict[str, None] = {}
    for branch in branches:
        names.update(dict.fromkeys(branch))
    return list(names)


def _enum(node: dict[str, Any]) -> tuple[JsonScalar, ...] | None:
    if isinstance(node.get("enum"), list):
        return _dedupe(node["enum"])
    if "const" in node:
        return _dedupe([node["const"]])
    return None


def _dedupe(values: Any) -> tuple[JsonScalar, ...]:
    """Keep scalar values, first occurrence wins. `True` and `1` are kept apart."""
    seen: set[tuple[str, JsonScalar]] = set()
    result: list[JsonScalar] = []
    for value in values:
        if value is not None and not isinstance(value, str | int | float | bool):
            continue
        key = (type(value).__name__, value)
        if key not in seen:
            seen.add(key)
            result.append(value)
    return tuple(result)
