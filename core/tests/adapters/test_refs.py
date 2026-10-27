import pytest

from notinspec.adapters.openapi.refs import RefError, Resolver, escape, join, unescape

DOC = {
    "paths": {"/v1/charges": {"get": {"x": 1}}},
    "components": {
        "schemas": {
            "A": {"$ref": "#/components/schemas/B"},
            "B": {"type": "string"},
            "Loop1": {"$ref": "#/components/schemas/Loop2"},
            "Loop2": {"$ref": "#/components/schemas/Loop1"},
            "a~b": {"type": "integer"},
        }
    },
    "list": [{"type": "boolean"}],
}


@pytest.mark.parametrize("token", ["/v1/charges", "a~b", "~1", "plain", "{id}"])
def test_escape_round_trip(token: str) -> None:
    assert unescape(escape(token)) == token


def test_join_escapes_tokens() -> None:
    assert join("#/paths", "/v1/charges", "post") == "#/paths/~1v1~1charges/post"
    assert join("#/x", 0) == "#/x/0"


def test_resolve_follows_a_chain_and_keeps_the_pointer() -> None:
    r = Resolver(DOC).resolve({"$ref": "#/components/schemas/A"}, "#/somewhere")
    assert r.node == {"type": "string"}
    assert r.pointer == "#/components/schemas/B"
    assert r.refs == ("#/components/schemas/A", "#/components/schemas/B")


def test_resolve_without_ref_returns_the_node_as_is() -> None:
    r = Resolver(DOC).resolve({"type": "x"}, "#/here")
    assert (r.node, r.pointer, r.refs) == ({"type": "x"}, "#/here", ())


@pytest.mark.parametrize(
    ("ref", "expected"),
    [
        ("#/paths/~1v1~1charges/get", {"x": 1}),
        ("#/components/schemas/a~0b", {"type": "integer"}),
        ("#/components/schemas/a%7E0b", {"type": "integer"}),  # percent-encoded fragment
        ("#/list/0", {"type": "boolean"}),
        ("#", DOC),
    ],
)
def test_lookup(ref: str, expected: object) -> None:
    assert Resolver(DOC).lookup(ref) == expected


@pytest.mark.parametrize(
    ("ref", "message"),
    [
        ("#/components/schemas/Missing", "not found"),
        ("#/list/5", "not found"),
        ("#/list/x", "not found"),
        ("other.yaml#/components/schemas/A", "external"),
        ("#components", "not a JSON pointer"),
    ],
)
def test_lookup_errors(ref: str, message: str) -> None:
    with pytest.raises(RefError, match=message):
        Resolver(DOC).lookup(ref)


def test_ref_cycle_is_an_error() -> None:
    with pytest.raises(RefError, match="cycle"):
        Resolver(DOC).resolve({"$ref": "#/components/schemas/Loop1"}, "#/x")
