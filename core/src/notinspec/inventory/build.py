"""Inventory from API reference blocks: component B (SPEC §6.2, §6.3). Deterministic.

Input is the chunks of any reader; only `signature` blocks of an API description (Sphinx `desc`,
`Block.objtype` set) give symbols, so Markdown chunks add nothing. MVP: Python domain (`py:*`).

Per section (all parts of a chunk, `section_id`), with one `Source("signature")`:

- **Symbol** per signature path (`Block.name`), kind = object type without the domain
  ("function", "method", "class", "attribute", "property", ...). Attributes and properties have
  no parameter list, so no `Signature`.
- **Signature** per signature block with a parameter list (overloads give several).
  `Parameter` kinds follow Python: before `/` positional-only, after `*` or `*args`
  keyword-only; `*args` / `**kwargs` are never required; a parameter without a default is
  required. Type: the annotation, else the type of its parameter entry (`field` block).
  `Literal[...]` annotations give an `enum` `Constraint`.
- **ReturnType**: the signature's `-> X`, else the section's `Return type` field, else the type
  of its `Returns` entry.
- **Change** from version directives (`Block.directives`): `deprecated` → deprecated,
  `versionadded` → added, `versionremoved` → removed, for every symbol of the section; inside
  a parameter entry it is about that parameter. `versionchanged` gives no `Change` (its text
  goes to claims). A version that is not PEP 440 is skipped with a warning.

Everything below the section is merged by `merge.merge` (same symbol documented twice,
same change from several directives).
"""

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from notinspec.chunking import Block, Chunk, SignatureParameter
from notinspec.inventory.merge import Conflict, merge, parse_version
from notinspec.inventory.objects import (
    Change,
    ChangeKind,
    Constraint,
    Inventory,
    Parameter,
    ParameterKind,
    ReturnType,
    Signature,
    Source,
    Symbol,
)

# bump when the inventory can change for the same chunks
INVENTORY_BUILDER_VERSION = 1

_DOMAINS = ("py",)
_CHANGE_KINDS: dict[str, ChangeKind] = {
    "deprecated": "deprecated",
    "versionadded": "added",
    "versionremoved": "removed",
}
_LITERAL = re.compile(r"(?:typing(?:_extensions)?\.)?Literal\[(.*)\]")


@dataclass(frozen=True)
class InventoryBuild:
    inventory: Inventory
    conflicts: tuple[Conflict, ...]  # disagreements between sources (later `Finding`s)
    warnings: tuple[str, ...]  # sorted, de-duplicated


def build_inventory(chunks: Iterable[Chunk]) -> InventoryBuild:
    """The inventory of all API descriptions in `chunks`. Pure: same chunks ⇒ equal result."""
    sections: dict[str, list[Block]] = {}
    for chunk in chunks:
        sections.setdefault(chunk.section_id, []).extend(chunk.blocks)
    warnings: list[str] = []
    parts = [_section(section_id, blocks, warnings) for section_id, blocks in sections.items()]
    inventory, conflicts = merge(parts)
    return InventoryBuild(inventory, conflicts, tuple(sorted(set(warnings))))


def _section(section_id: str, blocks: Sequence[Block], warnings: list[str]) -> Inventory:
    descs = [b for b in blocks if b.name and _domain(b) in _DOMAINS]
    if not descs:
        return Inventory(())
    source = (Source("signature", section_id=section_id),)
    fields = [b for b in blocks if b.kind == "field" and b.field == "param" and b.name]
    field_types: dict[str, str] = {}
    for field in fields:
        if field.type:
            field_types.setdefault(_bare(field.name or ""), field.type)
    returns = _section_returns(blocks)

    paths: dict[str, list[Signature]] = {}
    kinds: dict[str, str] = {}
    for block in descs:
        path = block.name or ""
        kinds.setdefault(path, (block.objtype or "").partition(":")[2])
        signatures = paths.setdefault(path, [])
        if block.parameters is not None:
            signatures.append(_signature(block, block.parameters, field_types, returns, source))
    symbols = tuple(
        Symbol(path, kinds[path], source, tuple(signatures)) for path, signatures in paths.items()
    )

    return Inventory(symbols, _changes(blocks, tuple(paths), source, warnings))


def _signature(
    block: Block,
    params: tuple[SignatureParameter, ...],
    field_types: dict[str, str],
    returns: str | None,
    source: tuple[Source, ...],
) -> Signature:
    names = [p.name for p in params]
    slash = names.index("/") if "/" in names else -1
    keyword_only = False
    parameters: list[Parameter] = []
    for i, param in enumerate(params):
        if param.name in ("/", "*"):
            keyword_only = keyword_only or param.name == "*"
            continue
        kind: ParameterKind
        if param.name.startswith("**"):
            kind = "var_keyword"
        elif param.name.startswith("*"):
            kind, keyword_only = "var_positional", True
        elif i < slash:
            kind = "positional_only"
        else:
            kind = "keyword_only" if keyword_only else "positional_or_keyword"
        name = _bare(param.name)
        variadic = kind in ("var_positional", "var_keyword")
        parameters.append(
            Parameter(
                name,
                kind,
                required=not variadic and param.default is None,
                sources=source,
                type=param.annotation or field_types.get(name),
                default=None if variadic else param.default,
                constraints=_constraints(param.annotation, source),
            )
        )
    return_type = block.type or returns
    return Signature(
        tuple(parameters),
        source,
        text=_text(block),
        returns=ReturnType(return_type, source) if return_type else None,
    )


def _changes(
    blocks: Sequence[Block], paths: tuple[str, ...], source: tuple[Source, ...], warnings: list[str]
) -> tuple[Change, ...]:
    changes: list[Change] = []
    for block in blocks:
        if not block.directives or (block.kind == "field" and block.field != "param"):
            continue
        parameter = _bare(block.name) if block.kind == "field" and block.name else None
        for directive, version in block.directives:
            kind = _CHANGE_KINDS.get(directive)
            if kind is None:
                continue
            if parse_version(version) is None:
                warnings.append(
                    f"{', '.join(paths)}: {directive} {version!r} is not a PEP 440 version"
                )
                continue
            changes += [Change(p, kind, version, source, parameter=parameter) for p in paths]
    return tuple(changes)


def _section_returns(blocks: Sequence[Block]) -> str | None:
    """`Return type` field, else the type of the `Returns` entry."""
    for field in ("return-type", "returns"):
        found = next((b.type for b in blocks if b.field == field and b.type), None)
        if found:
            return found
    return None


def _constraints(annotation: str | None, source: tuple[Source, ...]) -> tuple[Constraint, ...]:
    match = _LITERAL.fullmatch(annotation or "")
    if match is None:
        return ()
    values = tuple(v for v in _split_top_level(match[1]) if v)
    return (Constraint("enum", source, values=values),) if values else ()


def _split_top_level(value: str) -> list[str]:
    """Split at commas outside brackets and quotes: `'a, b', 1` → [`'a, b'`, `1`]."""
    parts: list[str] = []
    depth, quote, start = 0, "", 0
    for i, char in enumerate(value):
        if quote:
            quote = "" if char == quote and value[i - 1] != "\\" else quote
        elif char in "'\"":
            quote = char
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(value[start:i].strip())
            start = i + 1
    parts.append(value[start:].strip())
    return parts


def _domain(block: Block) -> str:
    return (block.objtype or "").partition(":")[0] if block.objtype else ""


def _bare(name: str) -> str:
    return name.lstrip("*")


def _text(block: Block) -> str | None:
    """The signature as documented, without the code span: built from the block's data."""
    if block.parameters is None:
        return None
    params = ", ".join(_parameter_text(p) for p in block.parameters)
    tail = f" -> {block.type}" if block.type else ""
    return f"{block.name}({params}){tail}"


def _parameter_text(param: SignatureParameter) -> str:
    out = param.name
    if param.annotation:
        out += f": {param.annotation}"
    if param.default is not None:
        out += f" = {param.default}" if param.annotation else f"={param.default}"
    return out
