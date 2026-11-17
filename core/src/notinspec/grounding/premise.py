"""NLI premise of a claim: the text around its citation that NLI reads (SPEC §6.1).

`<breadcrumb>: ` + the cited sentence(s) ±1 sentence, without leaving the cited prose unit. A
unit is a prose block, or one item of a list (a list item and its continuation paragraphs).
For a list item, the sentence that introduces the list (the last sentence before the list,
ending with ":") is put in front. A parameter entry (`field` block) adds the parameter name to
the breadcrumb: `urllib3 > API Reference > Retry > total`.

Measured as "local-block" in `experiments/nli` (run 007, FINDINGS): against a 400-token
window it keeps nearly half as many wrong claims. Computed from the chunk and the citation
span alone, so it needs no storage.
"""

import re
from dataclasses import dataclass

from notinspec.chunking import Block, Chunk, Sentence, prose_sentences
from notinspec.chunking.chunker import BREADCRUMB_SEPARATOR

PREMISE_RULE = "cited±1-in-block+lead-in"
RADIUS = 1  # sentences on each side of the cited ones

_PROSE_KINDS = frozenset({"text", "list", "quote", "admonition", "field"})
_LIST_ITEM = re.compile(r"[ \t]*(?:>[ \t]?)*[ \t]*(?:[-*+]|\d{1,9}[.)])(?:[ \t]+|$)")


@dataclass(frozen=True)
class Premise:
    text: str  # "<breadcrumb>: <sentences>"
    span: tuple[int, int]  # from the first to the last sentence used, offsets into chunk.text
    rule: str  # PREMISE_RULE


@dataclass(frozen=True)
class _Unit:
    block: int  # index into chunk.blocks
    item: int | None  # line number where the list item starts; None outside lists
    list_start: int | None  # line number of the list's first item


def nli_premise(chunk: Chunk, span: tuple[int, int]) -> Premise:
    """Premise for a citation at `span` (offsets into chunk.text, from `check_citation`)."""
    sentences = prose_sentences(chunk)
    cited = [i for i, s in enumerate(sentences) if s.start < span[1] and span[0] < s.end]
    if not cited:
        raise ValueError(f"span {span} is not in the prose of chunk {chunk.id}")
    units = [_unit(chunk, s) for s in sentences]
    cited_units = {units[i] for i in cited}
    low, high = max(cited[0] - RADIUS, 0), min(cited[-1] + RADIUS, len(sentences) - 1)
    picked = [i for i in range(low, high + 1) if units[i] in cited_units]

    first = units[picked[0]]
    block = chunk.blocks[first.block]
    if block.kind != "field" and first.list_start is not None:
        lead = _lead_in(chunk, sentences, units, first)
        if lead is not None and lead not in picked:
            picked.insert(0, lead)

    crumb = chunk.breadcrumb
    if len(cited_units) == 1 and block.kind == "field" and block.field == "param" and block.name:
        crumb = f"{crumb}{BREADCRUMB_SEPARATOR}{block.name}"
    used = [sentences[i] for i in picked]
    text = f"{crumb}: " + " ".join(s.text for s in used)
    return Premise(text, (used[0].start, max(s.end for s in used)), PREMISE_RULE)


def _lead_in(
    chunk: Chunk, sentences: tuple[Sentence, ...], units: list[_Unit], first: _Unit
) -> int | None:
    """Index of the sentence that introduces the list of `first`, if there is one.

    It is the last prose sentence before the list's first item, either earlier in the same
    block (a list inside an admonition) or in the block right before the list.
    """
    start = first.list_start or 0
    before = [
        i
        for i, u in enumerate(units)
        if u.block <= first.block and _line(chunk, sentences[i].start) < start
    ]
    if not before or not sentences[before[-1]].text.endswith(":"):
        return None
    block = units[before[-1]].block
    if block == first.block or block == _previous_block(chunk.blocks, first.block):
        return before[-1]
    return None


def _previous_block(blocks: tuple[Block, ...], index: int) -> int | None:
    """The block right before `index`, skipping code nested in a list or quote."""
    for i in range(index - 1, -1, -1):
        if not blocks[i].nested:
            return i
    return None


def _unit(chunk: Chunk, sentence: Sentence) -> _Unit:
    line = _line(chunk, sentence.start)
    for index, block in enumerate(chunk.blocks):
        if block.nested or block.kind not in _PROSE_KINDS:
            continue
        if block.start_line <= line <= block.end_line:
            lines = chunk.text.split("\n")
            items = [
                n
                for n in range(block.start_line, block.end_line + 1)
                if _LIST_ITEM.match(lines[n - chunk.start_line])
            ]
            if not items or items[0] > line:
                return _Unit(index, None, None)
            return _Unit(index, max(n for n in items if n <= line), items[0])
    raise AssertionError(f"sentence at {sentence.start} is in no prose block")


def _line(chunk: Chunk, offset: int) -> int:
    return chunk.start_line + chunk.text.count("\n", 0, offset)
