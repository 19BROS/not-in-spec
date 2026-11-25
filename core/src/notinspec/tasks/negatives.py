"""Conservative near-miss names for the supplied documentation snapshot, not runtime claims."""

import html
import json
import keyword
import re
import string
import unicodedata
from collections.abc import Iterator, Sequence

from notinspec.adapters.canonical import canonical_json
from notinspec.chunking import Chunk
from notinspec.inventory import Conflict, Inventory


def normalized(text: str) -> str:
    # Work on actual strings, not JSON syntax: JSON escapes are decoded by the index.
    text = html.unescape(text)
    text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m[1], 16)), text)
    text = re.sub(r"\\([" + re.escape(string.punctuation) + r"])", r"\1", text)
    # Soft hyphens and zero-width formatting characters can split a rendered identifier.
    text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return unicodedata.normalize("NFKC", text).casefold()


def _strings(value: object) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _strings(child)


class AbsenceIndex:
    """Search ALL supplied evidence, even weak signatures, changes, links and conflicts.

    Case-insensitive substring matching is deliberately stricter than Python name matching:
    a mention inside another identifier also vetoes a candidate. No rejected claim is evidence
    of absence. Callers must supply the complete snapshot, not retrieval/gold-context chunks.
    """

    def __init__(
        self, inventory: Inventory, chunks: Sequence[Chunk], conflicts: Sequence[Conflict]
    ) -> None:
        values = json.loads(canonical_json((inventory, chunks, conflicts)))
        self.corpus = "\n".join(normalized(text) for text in sorted(set(_strings(values))))
        self._cache: dict[str, bool] = {}
        sections: dict[str, set[int]] = {}
        for chunk in chunks:
            sections.setdefault(chunk.section_id, set()).add(chunk.part)
        self.complete = bool(chunks) and all(
            sections[c.section_id] == set(range(1, c.parts + 1)) for c in chunks
        )

    def absent(self, name: str) -> bool:
        # Also veto a short-name mention or alias in a different module.
        short = normalized(name.rsplit(".", 1)[-1])
        if short not in self._cache:
            self._cache[short] = self.complete and short not in self.corpus
        return self._cache[short]


def near_misses(name: str) -> tuple[str, ...]:
    """Bounded edits: unambiguous plural proposals, compound order, verb alternatives.

    These are proposals, never facts. Keep the original snake/camel/Pascal naming style;
    never create random strings, casing-only changes, private/dunder names or keywords.
    """
    if len(name) < 3:
        return ()
    if "_" in name:
        if not re.fullmatch(r"[a-z]+(?:_[a-z]+)+", name):
            return ()  # mixed snake styles are not lowercased into a different style
    elif not re.fullmatch(r"(?:[a-z]+|[A-Z][a-z]+)(?:[A-Z][a-z]+)*", name):
        return ()  # private names, acronyms, digits and unsupported spellings
    words = re.sub(r"([a-z])([A-Z])", r"\1_\2", name).lower().split("_")
    last = words[-1]
    edits: list[list[str]] = []
    # No singularization: a shortened prefix is vetoed by its own documented anchor.
    # Nor guess whether an s-ending word is plural (has, alias, analysis, series, ...).
    if len(last) >= 3 and not last.endswith(("s", "z")):
        if last.endswith("y") and last[-2] not in "aeiou":
            inflected = last[:-1] + "ies"
        elif last.endswith(("sh", "ch", "x")):
            inflected = last + "es"
        else:
            inflected = last + "s"
        edits.append(words[:-1] + [inflected])
    if len(words) > 1:
        edits.append([*words[:-2], words[-1], words[-2]])
    alternatives = {
        "get": "fetch",
        "fetch": "get",
        "set": "update",
        "update": "set",
        "create": "make",
        "make": "create",
        "remove": "delete",
        "delete": "remove",
    }
    if words[0] in alternatives:
        edits.append([alternatives[words[0]], *words[1:]])

    def render(parts: list[str]) -> str:
        if "_" in name:
            return "_".join(parts)
        if name[0].isupper():
            return "".join(p.title() for p in parts)
        return parts[0] + "".join(p.title() for p in parts[1:])

    return tuple(sorted({render(e) for e in edits} - {name} - set(keyword.kwlist)))
