"""Inline docutils nodes → one line of Markdown-like text.

- `literal`, `literal_strong`, `literal_emphasis` and inline `math` → text in backticks.
  Neighbouring code spans merge into one (`list of` + ` or ` + `None` → one span), so a
  reference wrapping a literal stays one backticked span.
- links and cross-references (`reference`, `pending_xref`), `emphasis`, `strong`, `inline`,
  `abbreviation`, `title_reference`, `target` → their text, never the link target, so
  intersphinx cannot change the chunk text (SPEC §6.1).
- `footnote_reference`, `citation_reference` → `[label]`.
- `index`, `image`, `raw`, `comment`, `substitution_definition` → nothing (their tail stays).
- `problematic` (broken markup) → its text, with a warning.
- Whitespace collapses to single spaces.
"""

from collections import Counter
from dataclasses import dataclass
from xml.etree.ElementTree import Element

CODE_TAGS = frozenset({"literal", "literal_strong", "literal_emphasis", "math"})
TEXT_TAGS = frozenset(
    {
        "reference",
        "pending_xref",
        "emphasis",
        "strong",
        "inline",
        "abbreviation",
        "acronym",
        "title_reference",
        "target",
        "subscript",
        "superscript",
        "generated",
        "number_reference",
        "download_reference",
        "desc_inline",
    }
)
SKIP_TAGS = frozenset({"index", "image", "raw", "comment", "substitution_definition"})
_LABEL_TAGS = frozenset({"footnote_reference", "citation_reference"})


@dataclass
class Context:
    """Per-document state: the docname for messages and the shared warning counter."""

    docname: str
    warnings: Counter[str]

    def warn(self, message: str) -> None:
        self.warnings[message] += 1

    def unknown(self, tag: str) -> None:
        self.warn(f"unknown node {tag}")


type Run = tuple[bool, str]  # (is code, text)


def runs(el: Element, ctx: Context) -> list[Run]:
    """Text runs of `el`'s content (its own text, children and their tails)."""
    out: list[Run] = []
    if el.text:
        out.append((False, el.text))
    for child in el:
        out.extend(element_runs(child, ctx))
        if child.tail:
            out.append((False, child.tail))
    return out


def element_runs(el: Element, ctx: Context) -> list[Run]:
    """Runs of one inline element, without its tail."""
    tag = el.tag
    if tag in CODE_TAGS:
        return [(True, "".join(el.itertext()))]
    if tag in SKIP_TAGS:
        return []
    if tag in _LABEL_TAGS:
        return [(False, f"[{text(el)}]")]
    if tag == "problematic":
        ctx.warn(f"unresolved markup in {ctx.docname}")
    elif tag not in TEXT_TAGS and not tag.startswith("desc_"):
        ctx.unknown(tag)
    return runs(el, ctx)


def render(parts: list[Run], *, code: bool = True) -> str:
    """Runs → one line. `code=False` drops the backticks (heading paths, types)."""
    merged: list[Run] = []
    for is_code, chunk in parts:
        if merged and is_code and merged[-1][0]:
            merged[-1] = (True, merged[-1][1] + chunk)
        else:
            merged.append((is_code, chunk))
    out: list[str] = []
    for is_code, chunk in merged:
        if not is_code:
            out.append(chunk)
            continue
        content = collapse(chunk)
        if not content:
            continue
        if code:
            # a leading/trailing space in a span (" or ") must stay a space between words
            lead = " " if chunk[:1].isspace() else ""
            trail = " " if chunk[-1:].isspace() else ""
            out.append(f"{lead}{backticks(content)}{trail}")
        else:
            out.append(f" {content} " if chunk.strip() != chunk else content)
    return collapse("".join(out))


def inline(el: Element, ctx: Context, *, code: bool = True) -> str:
    return render(runs(el, ctx), code=code)


def text(el: Element) -> str:
    """Plain text of all descendants, whitespace collapsed (labels, names)."""
    return collapse("".join(el.itertext()))


def collapse(value: str) -> str:
    return " ".join(value.split())


def backticks(content: str) -> str:
    """`content` as one code span; a longer fence when the content has backticks itself."""
    fence = "`"
    while fence in content:
        fence += "`"
    pad = " " if content.startswith("`") or content.endswith("`") else ""
    return f"{fence}{pad}{content}{pad}{fence}"
