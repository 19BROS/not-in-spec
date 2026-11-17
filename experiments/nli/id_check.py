"""Identifier / number / version check for grounding (prototype, SPEC §18).

A claim passes only if every identifier, number and version it names also appears in the
reference text. Best reference so far: breadcrumb + all prose of the claim's section (the NLI
premise alone drops correct claims that name things from a neighbouring sentence; FINDINGS).
NLI misses swapped names, numbers and versions (FINDINGS, run 006), so this runs next to it.

What counts as a token in the claim (both sides normalized like the citation check:
backticks removed, typographic quotes made plain):
- identifier: a backticked span, or a word with `_`, a dot between names (`Retry.total`),
  a trailing `()`, an inner capital (`ProxyManager`, `SSLError`) or letters + digits (`urllib3`).
  Plain words, single capitalized words (`Retry`, `Timeout`) and all-caps acronyms (HTTPS, TLS)
  are not checked unless backticked. Matching is case-sensitive,
  on name boundaries: `ssl_context` does not match inside `proxy_ssl_context`, but does match
  `ProxyConfig.ssl_context`. A trailing `()` is ignored when matching.
- number / version: `3`, `0.5`, `2.8.0`, `v3.0` (the `v` is ignored). A number must appear as a
  whole number: `3.13` does not match inside `3.13.14`, `3` not inside `urllib3`.

Options (measured in runs/007-block-premise-new-models/posthoc/id_check_eval.py):
- `number_words`: also read "zero" .. "twelve" as digits on both sides ("two seconds" = `2`).
- `project`: a dotted name that starts with the project name also passes without it
  (`urllib3.Timeout` passes on `Timeout`). The breadcrumb names the project, so this is free.
"""

import re
from dataclasses import dataclass

QUOTES = str.maketrans("“”‘’", "\"\"''")
NUMBER_WORDS = {
    w: str(i)
    for i, w in enumerate(
        "zero one two three four five six seven eight nine ten eleven twelve".split()
    )
}
NAME = r"[A-Za-z_][A-Za-z0-9_]*"
WORD = re.compile(rf"(?<![\w.]){NAME}(?:\.{NAME})*(?:\(\))?")
NUMBER = re.compile(r"(?<![\w.])v?(\d+(?:\.\d+)*)(?![\w]|\.\d)")
BACKTICKED = re.compile(r"`([^`]+)`")
NUMBER_WORD = re.compile(r"\b(" + "|".join(NUMBER_WORDS) + r")\b", re.IGNORECASE)


@dataclass(frozen=True)
class Options:
    number_words: bool = False
    project: str | None = None


def norm(text: str) -> str:
    return " ".join(text.translate(QUOTES).replace("`", "").split())


def is_identifier(word: str) -> bool:
    w = word.removesuffix("()")
    if all(len(part) == 1 for part in w.split(".")):  # e.g., i.e.
        return False
    return (
        word.endswith("()")
        or "_" in w
        or "." in w
        or re.search(r"[a-z][A-Z]|[A-Z]{2,}[a-z]", w) is not None
        or (re.search(r"[A-Za-z]", w) is not None and re.search(r"\d", w) is not None)
    )


def identifiers(claim: str) -> list[str]:
    text = claim.translate(QUOTES)
    found = [norm(s).removesuffix("()") for s in BACKTICKED.findall(text)]
    found += [w.removesuffix("()") for w in WORD.findall(norm(text)) if is_identifier(w)]
    # a backticked span that is a plain number or a phrase is left to the number check
    found = [f for f in found if f and not NUMBER.fullmatch(f) and " " not in f]
    return list(dict.fromkeys(found))


def numbers(text: str, opts: Options) -> list[str]:
    text = norm(text)
    if opts.number_words:
        text = NUMBER_WORD.sub(lambda m: NUMBER_WORDS[m.group(1).lower()], text)
    return list(dict.fromkeys(NUMBER.findall(text)))


def name_in(name: str, ref: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(name)}(?!\w)", ref) is not None


def missing(claim: str, reference: str, opts: Options | None = None) -> list[str]:
    """Tokens of the claim that the reference lacks. Empty list = the claim passes."""
    opts = opts or Options()
    ref = norm(reference)
    prefix = f"{opts.project}." if opts.project else None
    out = []
    for name in identifiers(claim):
        if not name_in(name, ref) and not (
            prefix and name.startswith(prefix) and name_in(name.removeprefix(prefix), ref)
        ):
            out.append(name)
    ref_numbers = set(numbers(ref, opts))
    out += [n for n in numbers(claim, opts) if n not in ref_numbers]
    return out
