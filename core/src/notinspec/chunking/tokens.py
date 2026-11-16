"""Token counting for chunk sizes."""

import re

_TOKEN = re.compile(r"\w+|[^\w\s]")


def approx_tokens(text: str) -> int:
    """Words plus punctuation marks: a stable, dependency-free estimate of model tokens.

    Close enough to size chunks. Swap in the NLI model's own tokenizer (pass `count_tokens`)
    once that model is chosen (SPEC §18).
    """
    return len(_TOKEN.findall(text))
