"""NLI windows: short prose-only excerpts of a chunk (SPEC §6.1).

Provisional: #10 proposes a shorter NLI premise (the cited sentence ±1 within its prose block)
instead of windows. The prose sentences and the citation check below are needed either way.
Picking the premise for a claim is grounding (role 4), so it is not in this module.

The NLI model accepts only a few hundred tokens, so it never sees a whole section. A window is:

- **prose only**: paragraphs, list items and quotes. Code blocks, tables, headings, HTML and
  rules are left out (code inside a list item too).
- **cut at sentence boundaries**: a sentence is never split. One sentence over the limit becomes
  its own window, marked `oversized`.
- **sized** to `max_tokens`, and the next window repeats the last sentences of the previous one
  (up to `overlap_tokens`), so a fact near a boundary is whole in at least one window.

Windows are computed from the chunk alone, so they need no storage: `id` is the chunk ID plus
the window's character offset in `chunk.text`. They still depend on the sentence splitter and
the token counter, so a `Claim` should record `WINDOWS_VERSION` and its window IDs; bump the
version when boundaries can change for the same chunk.

Window text is the prose with light Markdown cleanup (list and quote markers, link targets,
`**` and backticks removed), so the NLI model reads sentences, not markup. Offsets (`start`,
`end`) always point into the raw `chunk.text`, which is what claim citations quote.
"""

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from notinspec.chunking.chunker import Chunk
from notinspec.chunking.tokens import approx_tokens

# bump when window boundaries or text can change for the same chunk
WINDOWS_VERSION = 1

DEFAULT_WINDOW_TOKENS = 400  # SPEC §6.1 candidate; leaves room for the hypothesis under 512
DEFAULT_OVERLAP_TOKENS = 80

_PROSE_KINDS = frozenset({"text", "list", "quote"})


@dataclass(frozen=True)
class Sentence:
    start: int  # character offsets into chunk.text, end exclusive
    end: int
    text: str  # cleaned, one line
    tokens: int


@dataclass(frozen=True)
class NliWindow:
    id: str  # "<chunk id>@<start>"
    chunk_id: str
    index: int  # 0-based position among the chunk's windows
    start: int  # offset of the first sentence in chunk.text
    end: int  # end of the last sentence, exclusive
    tokens: int
    oversized: bool  # a single sentence longer than max_tokens
    text: str  # the sentences joined by spaces
    sentences: tuple[Sentence, ...]


def nli_windows(
    chunk: Chunk,
    *,
    max_tokens: int = DEFAULT_WINDOW_TOKENS,
    overlap_tokens: int = DEFAULT_OVERLAP_TOKENS,
    count_tokens: Callable[[str], int] = approx_tokens,
) -> tuple[NliWindow, ...]:
    """Windows of one chunk, in order. Pure: same chunk and settings → equal windows."""
    if not 0 <= overlap_tokens < max_tokens:
        raise ValueError("overlap_tokens must be at least 0 and smaller than max_tokens")
    sentences = prose_sentences(chunk, count_tokens=count_tokens)
    windows: list[NliWindow] = []
    i = 0
    while i < len(sentences):
        j, total = i + 1, sentences[i].tokens
        while j < len(sentences) and total + sentences[j].tokens <= max_tokens:
            total += sentences[j].tokens
            j += 1
        windows.append(_window(chunk.id, len(windows), sentences[i:j], max_tokens))
        if j == len(sentences):
            break
        i = _overlap_start(sentences, i, j, overlap_tokens, max_tokens)
    return tuple(windows)


def find_citation(chunk_text: str, citation: str) -> tuple[int, int] | None:
    """Offsets of the first place `citation` appears verbatim in the chunk, or None.

    SPEC §6.4: a citation that isn't in the chunk drops the claim. Only whitespace may differ
    (a quote of a wrapped paragraph has spaces where the file has line breaks).
    """
    words = citation.split()
    if not words:
        return None
    match = re.search(r"\s+".join(map(re.escape, words)), chunk_text)
    return (match.start(), match.end()) if match else None


# --- sentences -------------------------------------------------------------------------


def prose_sentences(
    chunk: Chunk, *, count_tokens: Callable[[str], int] = approx_tokens
) -> tuple[Sentence, ...]:
    """Every prose sentence of the chunk, in order, with offsets into `chunk.text`."""
    result: list[Sentence] = []
    for start, end in _prose_segments(chunk):
        segment = chunk.text[start:end]
        for s, e in _split_sentences(segment):
            text = clean_markdown(segment[s:e])
            if text:
                result.append(Sentence(start + s, start + e, text, count_tokens(text)))
    return tuple(result)


_LIST_ITEM = re.compile(r"\s*(?:>\s?)*\s*(?:[-*+]|\d{1,9}[.)])(?:\s+\[[ xX]\])?(?:\s+|$)")
_QUOTE_ONLY = re.compile(r"\s*(?:>\s*)+")


def _prose_segments(chunk: Chunk) -> list[tuple[int, int]]:
    """Character ranges of paragraphs and list items, without code inside lists or quotes.

    A segment never spans a blank line or two list items, so a sentence never does either.
    """
    lines = chunk.text.split("\n")
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line) + 1)
    first = chunk.start_line
    code_lines = {n for b in chunk.blocks if b.nested for n in range(b.start_line, b.end_line + 1)}
    segments: list[tuple[int, int]] = []
    for block in chunk.blocks:
        if block.nested or block.kind not in _PROSE_KINDS:
            continue
        current: list[int] = []  # line indexes in chunk.text
        for number in range(block.start_line, block.end_line + 1):
            index = number - first
            line = lines[index]
            breaks = (
                number in code_lines or not line.strip() or _QUOTE_ONLY.fullmatch(line) is not None
            )
            if breaks or (current and _LIST_ITEM.match(line)):
                _close(current, lines, offsets, segments)
                current = []
            if not breaks:
                current.append(index)
        _close(current, lines, offsets, segments)
    return segments


def _close(
    current: list[int], lines: list[str], offsets: list[int], out: list[tuple[int, int]]
) -> None:
    if current:
        first, last = current[0], current[-1]
        start = offsets[first] + len(lines[first]) - len(lines[first].lstrip())
        out.append((start, offsets[last] + len(lines[last])))


# a sentence ends at . ! ? (plus closing quotes, brackets or emphasis) followed by whitespace
_SENTENCE_END = re.compile(r"[.!?]+[\"')\]*_]*(?=\s)")
_CODE_SPAN = re.compile(r"(`+)(?:.+?)\1", re.DOTALL)
_ABBREVIATIONS = frozenset(
    {"e.g.", "i.e.", "vs.", "cf.", "approx.", "fig.", "no.", "nr.", "ca.", "mr.", "ms.", "dr."}
)


def _split_sentences(text: str) -> list[tuple[int, int]]:
    """Sentence ranges in one segment. Deterministic rules, no model:

    a boundary is `.`, `!` or `?` before whitespace, except inside `inline code`, after a known
    abbreviation ("e.g.") and when the next word starts with a lower-case letter ("2 s. or").
    """
    code = [m.span() for m in _CODE_SPAN.finditer(text)]
    cuts = [0]
    for match in _SENTENCE_END.finditer(text):
        end = match.end()
        if any(s <= match.start() < e for s, e in code):
            continue
        word = text[:end].rsplit(None, 1)[-1].lstrip("([\"'*_").lower()
        if word in _ABBREVIATIONS:
            continue
        rest = text[end:].lstrip()
        if not rest or rest[0].islower():
            continue
        cuts.append(end)
    cuts.append(len(text))
    spans: list[tuple[int, int]] = []
    for s, e in zip(cuts, cuts[1:], strict=False):
        while s < e and text[s].isspace():
            s += 1
        while e > s and text[e - 1].isspace():
            e -= 1
        if s < e:
            spans.append((s, e))
    return spans


_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_LINK = re.compile(r"\[([^\]]+)\](?:\([^)]*\)|\[[^\]]*\])")
_AUTOLINK = re.compile(r"<((?:https?|mailto):[^>\s]+)>")


def clean_markdown(text: str) -> str:
    """Markdown → plain sentence: no list/quote markers, link targets, `**` or backticks."""
    lines = []
    for line in text.split("\n"):
        line = re.sub(r"^\s*(?:>\s?)*", "", line)
        line = _LIST_ITEM.sub("", line, count=1) if _LIST_ITEM.match(line) else line
        lines.append(line)
    text = " ".join(lines)
    # links first: their text may itself be code ("[`Request`](api.md)")
    text = _AUTOLINK.sub(r"\1", _LINK.sub(r"\1", _IMAGE.sub(r"\1", text)))
    out: list[str] = []
    done = 0
    for match in _CODE_SPAN.finditer(text):  # code spans keep their content as is
        out.append(_clean_inline(text[done : match.start()]))
        out.append(match.group(0).strip("`").strip())
        done = match.end()
    out.append(_clean_inline(text[done:]))
    return " ".join("".join(out).split())


def _clean_inline(text: str) -> str:
    return text.replace("**", "")


# --- packing ---------------------------------------------------------------------------


def _overlap_start(
    sentences: Sequence[Sentence], i: int, j: int, overlap_tokens: int, max_tokens: int
) -> int:
    """Index where the next window starts: back from `j` by up to `overlap_tokens`.

    Never back to `i` (the window must move forward), and no overlap at all when it would
    leave no room for the next new sentence.
    """
    k, back = j, 0
    while k - 1 > i and back + sentences[k - 1].tokens <= overlap_tokens:
        k -= 1
        back += sentences[k].tokens
    if back + sentences[j].tokens > max_tokens:
        return j
    return k


def _window(chunk_id: str, index: int, sentences: Sequence[Sentence], max_tokens: int) -> NliWindow:
    tokens = sum(s.tokens for s in sentences)
    start = sentences[0].start
    return NliWindow(
        id=f"{chunk_id}@{start}",
        chunk_id=chunk_id,
        index=index,
        start=start,
        end=sentences[-1].end,
        tokens=tokens,
        oversized=tokens > max_tokens,
        text=" ".join(s.text for s in sentences),
        sentences=tuple(sentences),
    )
