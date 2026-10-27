"""Local `$ref` resolution that keeps the JSON pointer of every resolved piece.

The pointer of the place a piece is *defined* becomes the claim's `source`, so reports can link
back into the spec. Only same-document refs (`#/...`) are supported; the MVP targets are
self-contained files.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote


class RefError(Exception):
    """A `$ref` that can't be followed: missing target, external file, or a ref-to-ref cycle."""


def escape(token: str) -> str:
    """Escape one JSON pointer token (RFC 6901)."""
    return token.replace("~", "~0").replace("/", "~1")


def unescape(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def join(pointer: str, *tokens: str | int) -> str:
    """Append tokens to a pointer: `join("#/paths", "/v1/charges")` → `#/paths/~1v1~1charges`."""
    return pointer + "".join("/" + escape(str(t)) for t in tokens)


@dataclass(frozen=True)
class Resolved:
    node: Any  # the piece after following all refs
    pointer: str  # where that piece is defined
    refs: tuple[str, ...]  # ref targets followed to get there, in order (empty if none)


class Resolver:
    def __init__(self, document: Mapping[str, Any]) -> None:
        self._document = document

    def lookup(self, ref: str) -> Any:
        """Return the node a local ref points to."""
        if not ref.startswith("#"):
            raise RefError(f"external $ref not supported: {ref}")
        fragment = unquote(ref[1:])
        if fragment == "":
            return self._document
        if not fragment.startswith("/"):
            raise RefError(f"$ref is not a JSON pointer: {ref}")
        node: Any = self._document
        for raw in fragment[1:].split("/"):
            token = unescape(raw)
            if isinstance(node, Mapping) and token in node:
                node = node[token]
            elif isinstance(node, list) and token.isdigit() and int(token) < len(node):
                node = node[int(token)]
            else:
                raise RefError(f"$ref target not found: {ref}")
        return node

    def resolve(self, node: Any, pointer: str) -> Resolved:
        """Follow `$ref` until a real node is reached. `pointer` is where `node` itself sits.

        Sibling keys next to `$ref` are ignored here; callers that care (e.g. a description
        next to a ref, allowed in 3.1) read them from the original node.
        """
        refs: list[str] = []
        while isinstance(node, Mapping) and isinstance(node.get("$ref"), str):
            ref = node["$ref"]
            target = "#" + unquote(ref[1:]) if ref.startswith("#") else ref
            if target in refs:
                raise RefError("$ref cycle: " + " -> ".join([*refs, target]))
            node = self.lookup(ref)
            refs.append(target)
            pointer = target
        return Resolved(node=node, pointer=pointer, refs=tuple(refs))
