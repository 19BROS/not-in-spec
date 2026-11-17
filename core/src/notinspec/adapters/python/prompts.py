"""Interactive-session code (`>>>` prompts, Sphinx `doctest_block`, `pycon`) → plain Python.

The standard library's `doctest.DocTestParser` decides what is source and what is output, so
`...` continuation lines and expected output are handled the same way as by `doctest` itself.
"""

import doctest
from dataclasses import dataclass

_PARSER = doctest.DocTestParser()


@dataclass(frozen=True)
class Source:
    text: str  # Python source to parse
    # 1-based line in the original code for every line of `text`
    line_map: tuple[int, ...]


def has_prompts(code: str, *, anywhere: bool = False) -> bool:
    """True when the first non-blank line (or, with `anywhere`, any line) is a `>>>` prompt."""
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    return any(_is_prompt(line) for line in (lines if anywhere else lines[:1]))


def _is_prompt(line: str) -> bool:
    return line == ">>>" or line.startswith(">>> ")


def strip_prompts(code: str) -> Source:
    """Only the statements after `>>>` / `...`; output lines are dropped.

    Raises ValueError (from `doctest`) on inconsistent indentation after a prompt.
    """
    lines: list[str] = []
    line_map: list[int] = []
    for example in _PARSER.get_examples(code):
        own = example.source.rstrip("\n").split("\n")
        lines += own
        line_map += range(example.lineno + 1, example.lineno + 1 + len(own))
    return Source("\n".join(lines) + "\n" if lines else "", tuple(line_map))


def plain(code: str) -> Source:
    count = len(code.split("\n"))
    return Source(code, tuple(range(1, count + 1)))
