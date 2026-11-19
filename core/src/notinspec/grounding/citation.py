"""Citation check: is the claim's quoted span in the chunk, and is it prose (SPEC §6.4 step 1)?

Both sides are normalized the same way before matching:

- whitespace runs collapse to one space (a quote of a wrapped paragraph);
- Markdown markup is removed: backticks, `**`, link syntax (`[text](target)` keeps `text`),
  autolink brackets, and heading, quote and list markers at the start of a line;
- typographic quotes become plain quotes; en and em dashes, hyphen variants (U+2010–U+2012,
  U+2015) and the minus sign become "-" (Sphinx renders a parameter entry as
  ``- `name` (type) – text``, an extractor may quote it with "-");
- a control character becomes "'": an extractor sometimes writes `\x02` or `\x00` where the
  text has "’" (`you\x02re`, run 008).

The exact citation is tried first. Only if it is not found in prose, two looser forms are tried:

- a list marker right after a colon is dropped (`Raises: - Error – if …`): the extractor
  quoted a field list on one line, the chunk has the marker at the start of the next line;
- a citation with "..." or "…" is split into parts, and all parts must appear in order inside
  one prose block (`By default, urllib3 will ... follow up to 3 redirects`; a leading or
  trailing ellipsis leaves one part). Every part needs
  at least two words, so a part like "the" can't match anywhere. The span runs from the first
  part to the last one, the skipped text included.

A match is mapped back to offsets in the raw `chunk.text`, which is what NLI premises and
`Source` point into. A citation found only outside prose (code, table, signature, heading) is
`not_checkable`: facts in code and signatures belong to components B and C.
"""

import re
import unicodedata
from bisect import bisect_left
from dataclasses import dataclass
from typing import Literal

from notinspec.chunking import Chunk, prose_sentences

type CitationStatus = Literal["found", "not_found", "not_checkable"]

QUOTES = str.maketrans("“”‘’„‚", "\"\"''\"'")
# quotes, dashes, hyphen variants and the minus sign; citation check only
_PLAIN = str.maketrans("“”‘’„‚–—‐‑‒―−", "\"\"''\"'-------")

# markup removed before matching; each pattern's groups name the characters to drop.
# A wrapped Markdown line that starts with "3." is read as a list marker too, although only
# "1." can interrupt a paragraph in CommonMark. The Sphinx reader writes each paragraph on one
# line, so this affects only Markdown docs.
_LINE_MARKERS = re.compile(
    r"^[ \t]*(?:(?:>[ \t]?)+[ \t]*)?"
    r"(#{1,6}[ \t]+|(?:[-*+]|\d{1,9}[.)])(?:[ \t]+\[[ xX]\])?[ \t]+)?",
    re.MULTILINE,
)
_QUOTE_MARKERS = re.compile(r"^[ \t]*((?:>[ \t]?)+)", re.MULTILINE)
_LINK = re.compile(r"(!?\[)[^\]\n]*(\](?:\([^)\n]*\)|\[[^\]\n]*\]))")
_AUTOLINK = re.compile(r"(<)(?:https?|mailto):[^>\s]+(>)")
_MARKUP = re.compile(r"`|\*\*")
# on the normalized citation: a list marker after a colon, and an ellipsis between parts
_MIDLINE_MARKER = re.compile(r"(?<=:) [-*+•] ")
_ELLIPSIS = re.compile(r" ?(?:\.\.\.|…) ?")
_MIN_PART_WORDS = 2


@dataclass(frozen=True)
class CitationCheck:
    status: CitationStatus
    span: tuple[int, int] | None  # offsets into chunk.text: the first match; None when not found
    # found: every match in prose, in document order (span is the first). A docstring repeats
    # sentences across parameter entries, so which one the claim means is decided later.
    # not_checkable: the first match outside prose only.
    spans: tuple[tuple[int, int], ...] = ()


def normalize(text: str) -> str:
    """The text as the citation check compares it."""
    return _normalized(text)[0]


def check_citation(chunk: Chunk, citation: str) -> CitationCheck:
    """Where the citation is in the chunk: all matches in prose, or `not_checkable`."""
    return ChunkCitations(chunk).check(citation)


class ChunkCitations:
    """Checks many citations against one chunk: normalizes it and splits its sentences once."""

    def __init__(self, chunk: Chunk) -> None:
        self.chunk = chunk
        self.sentences = prose_sentences(chunk)
        self._haystack, self._offsets = _normalized(chunk.text)

    def check(self, citation: str) -> CitationCheck:
        exact = normalize(citation)
        if not exact:
            return CitationCheck("not_found", None)
        loose = _MIDLINE_MARKER.sub(" ", exact)
        results = [self._match(exact)]
        if loose != exact:
            results.append(self._match(loose))
        for result in results:
            if result.status == "found":
                return result
        elided = self._match_parts(loose)
        if elided is not None:
            return elided
        for result in results:
            if result.status == "not_checkable":
                return result
        return CitationCheck("not_found", None)

    def _match(self, needle: str) -> CitationCheck:
        text, haystack, offsets = self.chunk.text, self._haystack, self._offsets
        prose: list[tuple[int, int]] = []
        first: tuple[int, int] | None = None
        at = haystack.find(needle)
        while at >= 0:
            span = _widen(text, offsets[at], offsets[at + len(needle) - 1] + 1)
            if any(s.start < span[1] and span[0] < s.end for s in self.sentences):
                prose.append(span)
            elif first is None:
                first = span
            at = haystack.find(needle, at + 1)
        if prose:
            return CitationCheck("found", prose[0], tuple(prose))
        if first is not None:
            return CitationCheck("not_checkable", first, (first,))
        return CitationCheck("not_found", None)

    def _match_parts(self, needle: str) -> CitationCheck | None:
        """A citation with an ellipsis: its parts in order inside one prose block, or None."""
        if not _ELLIPSIS.search(needle):
            return None
        parts = [p for p in _ELLIPSIS.split(needle) if p.strip()]  # "... x" leaves one part
        if not parts or any(len(p.split()) < _MIN_PART_WORDS for p in parts):
            return None
        haystack, offsets = self._haystack, self._offsets
        spans: list[tuple[int, int]] = []
        for raw_start, raw_end in self._prose_blocks():
            at, end = bisect_left(offsets, raw_start), bisect_left(offsets, raw_end)
            first = -1
            for part in parts:
                at = haystack.find(part.strip(), at, end)
                if at < 0:
                    break
                first = at if first < 0 else first
                at += len(part.strip())
            if at >= 0:
                spans.append(_widen(self.chunk.text, offsets[first], offsets[at - 1] + 1))
        return CitationCheck("found", spans[0], tuple(spans)) if spans else None

    def _prose_blocks(self) -> list[tuple[int, int]]:
        """Raw offsets of each block's prose: from its first sentence to its last one."""
        text, first_line = self.chunk.text, self.chunk.start_line
        ranges: dict[int, tuple[int, int]] = {}
        for sentence in self.sentences:
            line = first_line + text.count("\n", 0, sentence.start)
            block = next(
                i for i, b in enumerate(self.chunk.blocks) if b.start_line <= line <= b.end_line
            )
            start, _ = ranges.get(block, (sentence.start, sentence.end))
            ranges[block] = (start, sentence.end)
        return list(ranges.values())


def _widen(text: str, start: int, end: int) -> tuple[int, int]:
    """Take in the backticks and `**` right around a match, so the span shows `code` whole."""
    while start > 0 and text[start - 1] in "`*":
        start -= 1
    while end < len(text) and text[end] in "`*":
        end += 1
    return start, end


def _normalized(text: str) -> tuple[str, list[int]]:
    """Normalized text and, for each of its characters, the offset in `text` it came from."""
    dropped = bytearray(len(text))

    def drop(match: re.Match[str]) -> None:
        for group in range(1, (match.re.groups or 0) + 1):
            start, end = match.span(group)
            if start >= 0:
                dropped[start:end] = b"\x01" * (end - start)

    for pattern in (_QUOTE_MARKERS, _LINE_MARKERS, _LINK, _AUTOLINK):
        for match in pattern.finditer(text):
            drop(match)
    for match in _MARKUP.finditer(text):
        dropped[match.start() : match.end()] = b"\x01" * (match.end() - match.start())

    chars: list[str] = []
    offsets: list[int] = []
    for i, char in enumerate(text):
        if dropped[i]:
            continue
        if char.isspace():
            if chars and chars[-1] != " ":
                chars.append(" ")
                offsets.append(i)
            continue
        if unicodedata.category(char) == "Cc":
            char = "'"
        chars.append(char.translate(_PLAIN))
        offsets.append(i)
    if chars and chars[-1] == " ":
        chars.pop()
        offsets.pop()
    return "".join(chars), offsets
