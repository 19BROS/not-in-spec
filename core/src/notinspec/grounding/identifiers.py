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
  A backticked expression that is not one name (`Retry(total=3)`) is split into its names
  and numbers, each checked on its own; a backticked phrase with spaces
  (`pip install urllib3`) adds no names. Plain words, lowercase inventory names that are also
  words (`read`, `total`, unless backticked), acronyms (HTTPS) and their plurals (`URLs`,
  `CAs`) are not checked.
  Matching is case-sensitive on name boundaries: `ssl_context` does not match inside
  `proxy_ssl_context`, but does match `ProxyConfig.ssl_context`. A trailing `()` and a leading
  dot (`.request()`) are ignored. A dotted name that starts with the project name also passes
  without it (`urllib3.Timeout` on `Timeout`). Only a capitalized inventory name that starts
  a sentence of the claim (and is not backticked) matches regardless of case: "Timeout errors
  are retried." passes on "Read timeout errors". Everywhere else case matters, because short
  class names are also words (`Request` would pass in 81 instead of 7 of 481 urllib3 sections).
- **number**: compared as written; the only extra equality is trailing zeros against an
  integer, so "1 second" matches `Timeout(connect=1.0)` but `3.10` is not `3.1`. Thousands
  separators are dropped (`1,000` = `1000`, groups of exactly 3 digits). A unit glued to the
  number is allowed on both sides ("2.5s"). A number never matches inside a name or a longer
  version (`3` is not in `urllib3`, `3.13` is not in `3.13.14`).
- **version**: two dots or more (`2.8.0`), compared as written; a leading `v` is ignored. An
  acronym glued to a version is the acronym and the version: `TLSv1.2` = "TLS 1.2".
"""

import re
from collections.abc import Sequence

from notinspec.chunking import Chunk, prose_sentences
from notinspec.grounding.citation import QUOTES
from notinspec.inventory import Inventory

_NAME = r"[A-Za-z_][A-Za-z0-9_]*"
_WORD = re.compile(rf"(?<![\w.]){_NAME}(?:\.{_NAME})*(?:\(\))?")
_NUMBER = re.compile(r"(?<![\w.])v?(\d+(?:\.\d+)*)(?:[A-Za-z]+)?(?![\w]|\.\d)")
_SINGLE_NAME = re.compile(rf"{_NAME}(?:\.{_NAME})*(?:\(\))?")
_BACKTICKED = re.compile(r"`([^`]+)`")
_THOUSANDS = re.compile(r"(?<![\w.,])(\d{1,3})((?:,\d{3})+)(?![\w]|,\d|\.\d)")
_TRAILING_ZEROS = re.compile(r"(\d+)\.0+")
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
    for name, any_case in _identifiers(claim, known_names).items():
        if _name_in(name, ref, any_case):
            continue
        if name.startswith(prefix) and _name_in(name.removeprefix(prefix), ref, any_case):
            continue
        out.append(name)
    ref_numbers = {_value(n) for n in _numbers(ref)}
    out += [n for n in _numbers(_norm(claim)) if _value(n) not in ref_numbers]
    return tuple(dict.fromkeys(out))


def identifiers_in(claim: str, known_names: frozenset[str]) -> tuple[str, ...]:
    """The identifiers the claim names, each once: backticked names first, then plain words,
    each group in text order. Same rules as `missing_identifiers`; numbers are not included."""
    return tuple(_identifiers(claim, known_names))


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


def _identifiers(claim: str, known_names: frozenset[str]) -> dict[str, bool]:
    """Identifiers of the claim, each with whether it may match regardless of case."""
    text = _ACRONYM_VERSION.sub(r"\1 \2", claim.translate(QUOTES))
    found: dict[str, bool] = {}
    for span in _BACKTICKED.findall(text):
        if any(c.isspace() for c in span.strip()):
            continue  # a phrase or command (`pip install urllib3`): its words are not names
        name = span.strip().removesuffix("()").lstrip(".")
        names = [name] if _SINGLE_NAME.fullmatch(name) else _WORD.findall(span)
        for n in names:
            found[n.removesuffix("()")] = False
    # backticked spans are blanked out, so offsets stay valid for finding sentence starts
    plain = _BACKTICKED.sub(lambda m: " " * len(m.group(0)), text)
    for match in _WORD.finditer(plain):
        word = match.group(0)
        if not _is_identifier(word, known_names):
            continue
        name = word.removesuffix("()")
        initial = (
            name[:1].isupper() and name in known_names and _starts_sentence(plain, match.start())
        )
        found[name] = found.get(name, True) and initial
    # a number is left to the number check
    return {n: c for n, c in found.items() if n and not _NUMBER.fullmatch(n)}


def _starts_sentence(text: str, at: int) -> bool:
    before = text[:at].rstrip().rstrip("\"'([")
    return not before or before[-1] in ".!?"


def _numbers(text: str) -> list[str]:
    text = _THOUSANDS.sub(lambda m: m.group(1) + m.group(2).replace(",", ""), text)
    return list(dict.fromkeys(_NUMBER.findall(text)))


def _value(number: str) -> str:
    """The number as written, but `1.0` and `1.00` are `1`."""
    match = _TRAILING_ZEROS.fullmatch(number)
    return match.group(1) if match else number


def _name_in(name: str, ref: str, any_case: bool = False) -> bool:
    pattern = rf"(?<!\w){re.escape(name)}(?!\w)"
    return re.search(pattern, ref, re.IGNORECASE if any_case else 0) is not None
