"""One Markdown code fence around a whole model answer (models without structured output wrap
JSON in one). Shared by the parsers of every LLM role, so they strip fences the same way.
"""

import re

# "```" + an optional language tag, then LF or CRLF; the closing fence may follow the last line
_FENCE = re.compile(r"\A\s*```[A-Za-z]*[ \t]*\r?\n(.*?)(?:\r?\n)?```\s*\Z", re.DOTALL)


def strip_code_fence(text: str) -> str:
    """The text inside one fence around the whole of `text`, else `text` unchanged."""
    fenced = _FENCE.match(text)
    return fenced.group(1) if fenced else text
