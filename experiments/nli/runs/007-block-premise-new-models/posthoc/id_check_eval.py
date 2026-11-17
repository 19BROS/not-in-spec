"""Measure the identifier / number / version check (id_check.py) next to large + local-block.

Gold = the human labels (labels-human.csv, labels-human-cross.csv). For comparison the same
counts are also printed with the Claude draft (labels.csv, all 350 same-section claims; every
cross pair counts as should-drop) and ChatGPT (labels-chatgpt.csv, the same 180 claims) as gold.

A claim is kept if NLI keeps it (argmax entailment) AND the check finds no missing token.
Reference text: `premise` = the local-block premise NLI saw (breadcrumb + cited sentence(s) +-1
in the cited block); `section` = breadcrumb + all prose sentences of the section (no code).
Indented variants split the main one into its two token classes.

usage (from experiments/nli): python runs/007-block-premise-new-models/posthoc/id_check_eval.py
Read-only; prints the tables used in FINDINGS.md (-> id_check_eval.txt).
"""

import csv
import json
import os
import sys

csv.field_size_limit(10**9)
NLI = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, NLI)
from id_check import Options, identifiers, missing, numbers  # noqa: E402

RESULTS = os.path.join(
    NLI,
    "runs",
    "007-block-premise-new-models",
    "results",
    "MoritzLaurer__DeBERTa-v3-large-mnli-fever-anli-ling-wanli__ctx-breadcrumb__prem-local-block.csv",
)
# name -> (reference text, tokens checked, read number words, strip a leading `<project>.`)
VARIANTS = {
    "premise": ("premise", "all", False, False),
    "section": ("section", "all", False, False),
    "section + project prefix": ("section", "all", False, True),
    "section + project prefix + number words": ("section", "all", True, True),
    "  identifiers only": ("section", "identifiers", False, True),
    "  numbers / versions only": ("section", "numbers", False, True),
}
MAIN = "section + project prefix"


def read(name):
    with open(os.path.join(NLI, name), encoding="utf-8") as f:
        return {(r["section"], r["extractor"], r["claim_id"]): r for r in csv.DictReader(f)}


def section_prose(slug, header):
    with open(os.path.join(NLI, "sections", slug, "windows-400.json"), encoding="utf-8") as f:
        sents = json.load(f)["sentences"]
    return header + "\n\n" + " ".join(s["text"] for s in sents)


with open(RESULTS, encoding="utf-8") as f:
    rows = {
        (r["section"], r["extractor"], r["claim_id"]): r
        for r in csv.DictReader(f)
        if r["window_size"] == "128"  # local premises don't depend on the window size
    }
nli_kept = {
    k for k, r in rows.items() if r["status"].startswith("ok") and r["label"] == "entailment"
}
headers = {k[0]: r["premise"].split("\n\n", 1)[0] for k, r in rows.items() if r["premise"]}
prose = {slug: section_prose(slug, h) for slug, h in headers.items()}


def miss(key, variant):
    scope, part, words, strip = VARIANTS[variant]
    r = rows[key]
    if not r["premise"]:  # the citation check already dropped it
        return ["(no premise)"]
    ref = r["premise"] if scope == "premise" else prose[key[0]]
    project = r["premise"].split(" > ", 1)[0] if strip else None
    opts = Options(number_words=words, project=project)
    out = missing(r["hypothesis"], ref, opts)
    if part == "identifiers":
        out = [t for t in out if t in identifiers(r["hypothesis"])]
    if part == "numbers":
        out = [t for t in out if t in numbers(r["hypothesis"], opts)]
    return out


def gold_sets(same, cross=None):
    """(should keep, should drop, cross should drop) for one label set."""
    pos = {k for k, v in same.items() if v["gold"] == "entailment"}
    xs = {k for k in rows if k[1].startswith("x-")}
    xbad = xs if cross is None else {k for k, v in cross.items() if v["gold"] != "entailment"}
    return pos, set(same) - pos, xbad


def table(title, pos, neg, xbad):
    fk, wx = nli_kept & neg, nli_kept & xbad
    print(
        f"\n{title}: {len(pos)} should-keep, {len(neg)} should-drop, {len(xbad)} cross should-drop"
    )
    print(
        f"  NLI alone: recall {len(nli_kept & pos)}/{len(pos)},"
        f" false keeps {len(fk)}, wrong cross keeps {len(wx)}"
    )
    print(
        f"  {'variant':40} false keeps caught  wrong cross caught"
        f"  good flagged/{len(pos)}  recall after"
    )
    for v in VARIANTS:
        flagged = {k for k in rows if miss(k, v)}
        good = pos & flagged
        print(
            f"  {v:40} {len(fk & flagged):4}/{len(fk):<13} {len(wx & flagged):4}/{len(wx):<13}"
            f" {len(good):4}            {len((nli_kept & pos) - flagged)}/{len(pos)}"
        )
    # rows the citation check already dropped have no premise and are left out here
    flagged = {k for k in rows if rows[k]["premise"] and miss(k, MAIN)}
    print(
        f"  check alone ({MAIN}): flags {len(neg & flagged)}/{len(neg)} should-drop"
        f" ({len(neg & flagged - nli_kept)} already dropped by NLI) and"
        f" {len(xbad & flagged)}/{len(xbad)} cross"
        f" ({len(xbad & flagged - nli_kept)} already dropped)"
    )


def show(title, keys, variant=MAIN):
    print(f"\n{title} ({variant}):")
    for k in sorted(keys):
        m = miss(k, variant)
        print(f"  {'/'.join(k)}  missing {m}" if m else f"  {'/'.join(k)}  passes")
        print(f"      claim:   {rows[k]['hypothesis']}")
        print(f"      premise: {' '.join(rows[k]['premise'].split(chr(10) * 2)[1:])}")


human, cross = read("labels-human.csv"), read("labels-human-cross.csv")
pos, neg, xbad = gold_sets(human, cross)
table("Gold = human (labels-human.csv + labels-human-cross.csv)", pos, neg, xbad)
table("Compare: gold = claude-draft (labels.csv, all claims)", *gold_sets(read("labels.csv")))
table(
    "Compare: gold = chatgpt (labels-chatgpt.csv, human sample; cross = human)",
    *gold_sets(read("labels-chatgpt.csv"), cross)[:2],
    xbad,
)

for v in VARIANTS:
    good = sorted(pos & {k for k in rows if miss(k, v)})
    print(f"\nGood claims (human) flagged by '{v}': {len(good)}")
    for k in good:
        nli = "NLI keeps" if k in nli_kept else "NLI drops"
        print(f"  {'/'.join(k)}  {nli}  missing {miss(k, v)}: {rows[k]['hypothesis']}")

show("False keeps of large + local-block (human gold)", nli_kept & neg)
show("Wrong cross keeps of large + local-block (human gold)", nli_kept & xbad)
