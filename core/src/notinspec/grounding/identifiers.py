"""Identifier / number / version check: does the section name what the claim names (SPEC §18)?

NLI misses swapped names, numbers and versions (`experiments/nli/FINDINGS.md`, run 006), so
this runs next to it: a claim passes only if every identifier, number and version it names
also appears in the reference. The reference is the whole section's prose plus its breadcrumb
(`section_reference`); the NLI premise alone drops correct claims that name something from a
neighbouring sentence. For an API description, the symbol's inventory names are added too,
because its signature is not prose. In guides, code still doesn't count.

What the claim is checked for (both sides normalized like the citation check):

- **identifier**: a backticked span, or a word with `_`, a dot between names (`Retry.total`),
  a trailing `()`, an inner capital (`ProxyManager`, `SSLError`) or letters + digits
  (`urllib3`). A single capitalized word (`Retry`) counts when it is a name in the inventory.
  Plain words, lowercase inventory names that are also words (`read`, `total`, unless
  backticked), acronyms (HTTPS) and their plurals (`URLs`, `CAs`) are not checked.
  Matching is case-sensitive on name boundaries: `ssl_context` does not match inside
  `proxy_ssl_context`, but does match `ProxyConfig.ssl_context`. A trailing `()` and a leading
  dot (`.request()`) are ignored. A dotted name that starts with the project name also passes
  without it (`urllib3.Timeout` on `Timeout`).
- **number**: compared by value, so "1 second" matches `Timeout(connect=1.0)`. A unit glued to
  the number is allowed on both sides ("2.5s"). A number never matches inside a name or a
  longer version (`3` is not in `urllib3`, `3.13` is not in `3.13.14`).
- **version**: two dots or more (`2.8.0`), compared as written; a leading `v` is ignored. An
  acronym glued to a version is the acronym and the version: `TLSv1.2` = "TLS 1.2".
"""

import re
from collections.abc import Sequence
from decimal import Decimal

from notinspec.chunking import Chunk, prose_sentences
from notinspec.grounding.citation import QUOTES
from notinspec.inventory import Inventory

_NAME = r"[A-Za-z_][A-Za-z0-9_]*"
_WORD = re.compile(rf"(?<![\w.]){_NAME}(?:\.{_NAME})*(?:\(\))?")
_NUMBER = re.compile(r"(?<![\w.])v?(\d+(?:\.\d+)*)(?:[A-Za-z]+)?(?![\w]|\.\d)")
_BACKTICKED = re.compile(r"`([^`]+)`")
# an acronym glued to a version: TLSv1.2, IPv6, HTTP2 (read as "TLS 1.2")
_ACRONYM_VERSION = re.compile(r"(?<![\w.])([A-Z]{2,})v?(\d+(?:\.\d+)*)(?![\w]|\.\d)")


def missing_identifiers(
    claim: str, reference: str, *, project: str, known_names: frozenset[str]
) -> tuple[str, ...]:
    """Identifiers, numbers and versions of the claim that the reference lacks; () = passes.

    `known_names` are the inventory's names (`inventory_names`); only the capitalized ones
    make a single word an identifier.
    """
    ref = _norm(reference)
    prefix = f"{project}."
    out: list[str] = []
    for name in _identifiers(claim, known_names):
        if _name_in(name, ref):
            continue
        if name.startswith(prefix) and _name_in(name.removeprefix(prefix), ref):
            continue
        out.append(name)
    ref_numbers = {_value(n) for n in _numbers(ref)}
    out += [n for n in _numbers(_norm(claim)) if _value(n) not in ref_numbers]
    return tuple(dict.fromkeys(out))


def section_reference(section: Sequence[Chunk], inventory: Inventory) -> str:
    """Reference text for one section (all its parts): breadcrumb + prose (+ API names).

    For an API description (a chunk with a signature), the symbol's path, its short name and
    its parameter names are added from the inventory, or from the signature block when the
    symbol is not in it.
    """
    if not section:
        return ""
    lines = [section[0].breadcrumb]
    for chunk in section:
        lines.extend(s.text for s in prose_sentences(chunk))
    symbols = {s.path: s for s in inventory.symbols}
    for chunk in section:
        for block in chunk.blocks:
            if block.kind != "signature" or not block.objtype or not block.name:
                continue
            names = [block.name, block.name.rsplit(".", 1)[-1]]
            symbol = symbols.get(block.name)
            if symbol is not None:
                names += [p.name for sig in symbol.signatures for p in sig.parameters]
            else:
                names += [p.name.lstrip("*") for p in block.parameters or ()]
            lines.append(" ".join(dict.fromkeys(n for n in names if n and n != "/")))
    return "\n".join(lines)


def inventory_names(inventory: Inventory) -> frozenset[str]:
    """Short names of every symbol and parameter: `Retry`, `sleep`, `total`."""
    names: set[str] = set()
    for symbol in inventory.symbols:
        names.add(symbol.path.rsplit(".", 1)[-1])
        names.update(p.name for sig in symbol.signatures for p in sig.parameters)
    return frozenset(n for n in names if re.fullmatch(_NAME, n))


def _norm(text: str) -> str:
    text = text.translate(QUOTES)
    text = _ACRONYM_VERSION.sub(r"\1 \2", text)
    return " ".join(text.replace("`", "").split())


def _is_identifier(word: str, known_names: frozenset[str]) -> bool:
    w = word.removesuffix("()")
    if all(len(part) == 1 for part in w.split(".")):  # e.g., i.e.
        return False
    return (
        word.endswith("()")
        or "_" in w
        or "." in w
        or re.search(r"[a-z][A-Z]|[A-Z]{2,}[a-z]{2}", w) is not None
        or (re.search(r"[A-Za-z]", w) is not None and re.search(r"\d", w) is not None)
        or (w[:1].isupper() and w in known_names)
    )


def _identifiers(claim: str, known_names: frozenset[str]) -> list[str]:
    text = _ACRONYM_VERSION.sub(r"\1 \2", claim.translate(QUOTES))
    found = [_norm(s).removesuffix("()").lstrip(".") for s in _BACKTICKED.findall(text)]
    found += [
        w.removesuffix("()") for w in _WORD.findall(_norm(text)) if _is_identifier(w, known_names)
    ]
    # a backticked number or phrase is left to the number check
    return list(dict.fromkeys(f for f in found if f and not _NUMBER.fullmatch(f) and " " not in f))


def _numbers(text: str) -> list[str]:
    return list(dict.fromkeys(_NUMBER.findall(text)))


def _value(number: str) -> str | Decimal:
    """A plain number by value (`1` = `1.0`), a version (two dots or more) as written."""
    return number if number.count(".") >= 2 else Decimal(number)


def _name_in(name: str, ref: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(name)}(?!\w)", ref) is not None
