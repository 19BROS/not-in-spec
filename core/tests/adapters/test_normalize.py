from collections.abc import Callable
from pathlib import Path

import pytest

from notinspec.adapters.canonical import canonical_json, content_hash
from notinspec.adapters.openapi import (
    NormalizedField,
    NormalizedOperation,
    NormalizedSpec,
    load_spec,
    normalize,
)

Golden = Callable[[str, object], None]


def _normalized(fixtures: Path, name: str) -> NormalizedSpec:
    return normalize(load_spec(fixtures / f"{name}.yaml", validate=False).document)


def _op(spec: NormalizedSpec, method: str, path: str) -> NormalizedOperation:
    return next(o for o in spec.operations if (o.method, o.path) == (method, path))


def _fields(op: NormalizedOperation) -> dict[str, NormalizedField]:
    return {f"{f.location}:{f.name}": f for f in (*op.parameters, *op.body_fields)}


@pytest.fixture
def acme(fixtures: Path) -> NormalizedSpec:
    return _normalized(fixtures, "acme")


@pytest.fixture
def composition(fixtures: Path) -> NormalizedSpec:
    return _normalized(fixtures, "composition")


# --- golden files and determinism ------------------------------------------------------


@pytest.mark.parametrize("name", ["acme", "composition"])
def test_golden(fixtures: Path, golden: Golden, name: str) -> None:
    golden(f"normalize-{name}", _normalized(fixtures, name))


def test_golden_shared_prism_fixture(repo_root: Path, golden: Golden) -> None:
    spec = load_spec(repo_root / "deploy" / "fixtures" / "openapi.yaml")
    assert spec.problems == ()
    golden("normalize-deploy-fixture", normalize(spec.document))


@pytest.mark.parametrize("name", ["acme", "composition"])
def test_same_input_gives_identical_bytes(fixtures: Path, name: str) -> None:
    first, second = _normalized(fixtures, name), _normalized(fixtures, name)
    assert canonical_json(first) == canonical_json(second)
    assert content_hash(first) == content_hash(second)


def test_key_order_in_the_source_does_not_matter(fixtures: Path) -> None:
    doc = load_spec(fixtures / "acme.yaml", validate=False).document
    shuffled = dict(reversed(list(doc.items())))
    shuffled["paths"] = dict(reversed(list(doc["paths"].items())))
    assert canonical_json(normalize(shuffled)) == canonical_json(normalize(doc))


# --- operations, parameters, security --------------------------------------------------


def test_operations_are_sorted_by_path_then_method(acme: NormalizedSpec) -> None:
    assert [(o.path, o.method) for o in acme.operations] == [
        ("/health", "GET"),
        ("/v1/charges", "GET"),
        ("/v1/charges", "POST"),
        ("/v1/charges/{id}", "DELETE"),
        ("/v1/charges/{id}", "GET"),
    ]


def test_path_level_parameters_are_merged_and_operation_wins(acme: NormalizedSpec) -> None:
    listed = _fields(_op(acme, "GET", "/v1/charges"))
    assert list(listed) == ["query:expand", "query:limit", "header:Idempotency-Key"]
    assert not listed["header:Idempotency-Key"].required
    created = _op(acme, "POST", "/v1/charges")
    headers = [p for p in created.parameters if p.location == "header"]
    assert [(h.name, h.required) for h in headers] == [("idempotency-key", True)]


def test_parameter_ref_keeps_its_definition_as_source(acme: NormalizedSpec) -> None:
    expand = _fields(_op(acme, "GET", "/v1/charges"))["query:expand"]
    assert expand.source == "#/components/parameters/Expand"
    assert expand.enum == ("customer", "refunds")
    assert expand.description == "Related objects to include."


def test_path_parameters_are_always_required(acme: NormalizedSpec) -> None:
    assert _fields(_op(acme, "GET", "/v1/charges/{id}"))["path:id"].required


def test_effective_security(acme: NormalizedSpec) -> None:
    assert _op(acme, "POST", "/v1/charges").security == (("bearerAuth",),)  # global
    assert _op(acme, "GET", "/v1/charges/{id}").security == (("apiKey",), ("bearerAuth",))
    assert _op(acme, "GET", "/health").security == ()  # security: [] means no auth


def test_security_schemes(acme: NormalizedSpec) -> None:
    bearer, api_key = acme.security_schemes[1], acme.security_schemes[0]
    assert (bearer.name, bearer.type, bearer.scheme) == ("bearerAuth", "http", "bearer")
    assert (api_key.location, api_key.param_name) == ("header", "X-Api-Key")


def test_tags_and_deprecated(acme: NormalizedSpec) -> None:
    assert _op(acme, "GET", "/health").tags == ()
    assert _op(acme, "DELETE", "/v1/charges/{id}").deprecated


# --- request bodies --------------------------------------------------------------------


def test_body_fields_match_the_role_guide_example(acme: NormalizedSpec) -> None:
    op = _op(acme, "POST", "/v1/charges")
    assert op.body_media_type == "application/json"
    assert op.body_required
    summary = [(f.name, f.type, f.required, f.enum) for f in op.body_fields]
    assert summary == [
        ("amount", "integer", True, None),
        ("capture", "string", False, ("automatic", "manual")),
        ("currency", "string", True, None),
        ("customer", "string", False, None),
        ("metadata", "object", False, None),
        ("shipping", "object", False, None),
        ("shipping.address", "object", False, None),  # required inside an optional parent
        ("shipping.name", "string", False, None),
    ]


def test_read_only_fields_are_skipped(acme: NormalizedSpec) -> None:
    assert "body:id" not in _fields(_op(acme, "POST", "/v1/charges"))


def test_nesting_stops_at_two_levels(acme: NormalizedSpec) -> None:
    names = _fields(_op(acme, "POST", "/v1/charges"))
    assert "body:shipping.address" in names
    assert not any(n.startswith("body:shipping.address.") for n in names)


def test_body_field_source_points_at_the_definition(acme: NormalizedSpec) -> None:
    amount = _fields(_op(acme, "POST", "/v1/charges"))["body:amount"]
    assert amount.source == "#/components/schemas/ChargeCreate/properties/amount"
    assert amount.example == 1000


def test_all_of_merges_properties_and_required(composition: NormalizedSpec) -> None:
    fields = _fields(_op(composition, "POST", "/payments"))
    assert fields["body:kind"].required  # from the Base part
    assert fields["body:method"].required  # from the inline part


def test_one_of_required_only_if_required_in_every_branch(composition: NormalizedSpec) -> None:
    fields = _fields(_op(composition, "POST", "/payments"))
    assert fields["body:method.number"].required
    assert not fields["body:method.exp"].required
    assert not fields["body:method.iban"].required


def test_enums_across_branches(composition: NormalizedSpec) -> None:
    fields = _fields(_op(composition, "POST", "/payments"))
    assert fields["body:mode"].enum is None  # one branch accepts any string
    assert fields["body:status"].enum == ("on", "off", 1, 2)
    assert fields["body:status"].type == "integer|string"
    assert fields["body:flag"].enum == (True,)  # const


def test_null_is_dropped_from_type_lists(composition: NormalizedSpec) -> None:
    assert _fields(_op(composition, "POST", "/payments"))["body:nullable_note"].type == "string"


def test_recursive_schema_stops(composition: NormalizedSpec) -> None:
    names = [f.name for f in _op(composition, "POST", "/tree").body_fields]
    assert names == ["children", "label", "parent"]


def test_form_encoded_body_is_read(composition: NormalizedSpec) -> None:
    op = _op(composition, "POST", "/form")
    assert op.body_media_type == "application/x-www-form-urlencoded"
    assert [f.name for f in op.body_fields] == ["amount", "expand"]


def test_media_type_parameters_are_ignored_when_matching(composition: NormalizedSpec) -> None:
    op = _op(composition, "POST", "/payments")
    assert op.body_media_type == "application/json; charset=utf-8"


def test_unsupported_body_media_type_gives_no_fields(composition: NormalizedSpec) -> None:
    op = _op(composition, "PUT", "/upload")
    assert (op.body_media_type, op.body_fields) == (None, ())


def test_body_media_types_are_configurable(fixtures: Path) -> None:
    doc = load_spec(fixtures / "composition.yaml", validate=False).document
    spec = normalize(doc, body_media_types=["multipart/form-data"])
    assert [f.name for f in _op(spec, "PUT", "/upload").body_fields] == ["file"]


# --- broken input ----------------------------------------------------------------------


def test_broken_pieces_are_reported_and_skipped(composition: NormalizedSpec) -> None:
    op = _op(composition, "GET", "/broken")
    assert [p.name for p in op.parameters] == ["loop"]
    assert op.parameters[0].type is None
    assert composition.problems == (
        "#/paths/~1broken/get/parameters/0: parameter without a valid name / in",
        "#/paths/~1broken/get/parameters/1: $ref target not found: "
        "#/components/parameters/DoesNotExist",
        "#/paths/~1broken/get/parameters/2/schema: $ref cycle: #/components/schemas/LoopA"
        " -> #/components/schemas/LoopB -> #/components/schemas/LoopA",
        "#/paths/~1broken/get: unknown security scheme 'missingScheme'",
    )


def test_vendor_extensions_in_paths_are_ignored(composition: NormalizedSpec) -> None:
    assert not any(o.path.startswith("x-") for o in composition.operations)


@pytest.mark.parametrize(
    ("doc", "problem"),
    [
        ({"paths": {"no-slash": {"get": {}}}}, "path does not start with '/'"),
        ({"paths": {"/a": {"get": {"parameters": {}}}}}, "parameters is not a list"),
        ({"paths": {"/a": {"get": {"security": {}}}}}, "security is not a list"),
        ({"components": {"securitySchemes": {"s": {"in": "header"}}}}, "without a type"),
    ],
)
def test_malformed_structures(doc: dict[str, object], problem: str) -> None:
    spec = normalize({"openapi": "3.1.0", **doc})
    assert any(problem in p for p in spec.problems)


def test_empty_document() -> None:
    spec = normalize({})
    assert (spec.operations, spec.security_schemes, spec.problems) == ((), (), ())
    assert (spec.title, spec.api_version, spec.openapi_version) == (None, None, "")


def test_parameter_with_content_instead_of_schema() -> None:
    doc = {
        "paths": {
            "/a": {
                "get": {
                    "parameters": [
                        {
                            "name": "filter",
                            "in": "query",
                            "content": {"application/json": {"schema": {"type": "object"}}},
                        }
                    ]
                }
            }
        }
    }
    param = normalize(doc).operations[0].parameters[0]
    assert param.type == "object"
    assert param.source == "#/paths/~1a/get/parameters/0"


def test_examples_list_and_ref_sibling_description() -> None:
    x = {"$ref": "#/components/schemas/S", "description": "own"}
    doc = {
        "components": {"schemas": {"S": {"type": "string", "description": "shared"}}},
        "paths": {
            "/a": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "properties": {
                                        "x": x,
                                        "y": {"type": "string", "examples": ["first", "second"]},
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
    }
    fields = {f.name: f for f in normalize(doc).operations[0].body_fields}
    assert fields["x"].description == "own"
    assert fields["y"].example == "first"
