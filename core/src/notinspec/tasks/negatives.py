"""Conservative near-miss names for the supplied documentation snapshot, not runtime claims."""

import keyword
import re
import unicodedata
from collections.abc import Sequence

from notinspec.adapters.canonical import canonical_json
from notinspec.chunking import Chunk
from notinspec.inventory import Conflict, Inventory


def normalized(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


class AbsenceIndex:
    """Search ALL supplied evidence, even weak signatures, changes, links and conflicts.

    Case-insensitive substring matching is deliberately stricter than Python name matching:
    a mention inside another identifier also vetoes a candidate. No rejected claim is evidence
    of absence. Callers must supply the complete snapshot, not retrieval/gold-context chunks.
    """

    def __init__(
        self, inventory: Inventory, chunks: Sequence[Chunk], conflicts: Sequence[Conflict]
    ) -> None:
        self.corpus = normalized(canonical_json((inventory, chunks, conflicts)).decode())
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
    """Bounded lexical edits: last-word number, compound order, common verb alternatives.

    These are proposals, never facts. Keep the original snake/camel/Pascal naming style;
    never create random strings, casing-only changes, private/dunder names or keywords.
    """
    if not re.fullmatch(r"[A-Za-z][A-Za-z_]{2,}", name):
        return ()
    if re.search(r"[A-Z]{2,}", name):
        return ()  # do not silently change acronym spelling while rendering an edit
    words = re.sub(r"([a-z])([A-Z])", r"\1_\2", name).lower().split("_")
    if any(not word for word in words):
        return ()
    last = words[-1]
    if last.endswith("ies") and len(last) > 3:
        inflected = last[:-3] + "y"
    elif last.endswith(("sses", "ches", "shes", "xes", "zes")):
        inflected = last[:-2]
    elif len(last) > 1 and last.endswith("s") and not last.endswith(("ss", "us")):
        inflected = last[:-1]
    elif len(last) > 1 and last.endswith("y") and last[-2] not in "aeiou":
        inflected = last[:-1] + "ies"
    elif last.endswith(("s", "sh", "ch", "x", "z")):
        inflected = last + "es"
    else:
        inflected = last + "s"
    edits = [words[:-1] + [inflected]]
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
