"""Build the blind labelling page, a hidden key and ChatGPT inputs (read-only on the repo).

usage: python -I -X utf8 build.py <repo-root> <out-dir>
The hidden key goes to <out-dir>/../hidden/. Same seed + same labels.csv and run-006 CSVs
give the same ids, so labels-human.csv can be traced back to the page.
"""

import csv
import json
import os
import random
import sys
from collections import Counter

csv.field_size_limit(10**9)
REPO, OUT = sys.argv[1], sys.argv[2]
N = os.path.join(REPO, "experiments", "nli")
HERE = os.path.dirname(os.path.abspath(__file__))
TOTAL = 180
SEED = 20261108
SECTION_ORDER = [
    "using-timeouts",
    "retrying-requests",
    "configuring-exponential-backoff",
    "httpx-timeouts-fine-tuning",
    "changelog-2-8-0-security",
    "changelog-2-8-0-bugfixes",
]
RUN = os.path.join(
    N,
    "runs",
    "006-realistic-negatives",
    "results",
    "MoritzLaurer__DeBERTa-v3-large-mnli-fever-anli-ling-wanli__ctx-breadcrumb__prem-local.csv",
)


def source(extractor):
    return (
        "negative"
        if extractor.startswith("negatives")
        else "outside"
        if "outside" in extractor
        else "real"
    )


labels = list(csv.DictReader(open(os.path.join(N, "labels.csv"), encoding="utf-8")))
model = {
    (r["section"], r["extractor"], r["claim_id"]): r["label"]
    for r in csv.DictReader(open(RUN, encoding="utf-8"))
    if r["window_size"] == "400"
}

claims = {}
for sec in SECTION_ORDER:
    for f in os.listdir(os.path.join(N, "sections", sec, "claims")):
        doc = json.load(open(os.path.join(N, "sections", sec, "claims", f), encoding="utf-8"))
        for c in doc.get("claims", doc if isinstance(doc, list) else []):
            claims[(sec, f[:-5], c["id"])] = c

rng = random.Random(SEED)
picked = []
real_rest = []
for r in labels:
    k = (r["section"], r["extractor"], r["claim_id"])
    src = source(r["extractor"])
    if src != "real":
        picked.append((k, "nonreal"))
    elif r["gold"] != "entailment" or model.get(k) != "entailment":
        picked.append((k, "real-disputed"))
    else:
        real_rest.append(k)
rng.shuffle(real_rest)
picked += [(k, "real-random") for k in real_rest[: TOTAL - len(picked)]]
missing = [k for k, _ in picked if k not in claims]
assert not missing, missing

ids = [f"q{n:03d}" for n in rng.sample(range(100, 1000), len(picked))]
rows = [{"id": i, "key": k, "why": why} for i, (k, why) in zip(ids, picked, strict=True)]
by_sec = {s: [r for r in rows if r["key"][0] == s] for s in SECTION_ORDER}
for s in SECTION_ORDER:
    rng.shuffle(by_sec[s])
ordered = [r for s in SECTION_ORDER for r in by_sec[s]]

sections = {}
for s in SECTION_ORDER:
    d = json.load(open(os.path.join(N, "sections", s, "section.json"), encoding="utf-8"))
    sections[s] = {
        "project": d["source"]["project"],
        "breadcrumb": d["breadcrumb"],
        "blocks": [{"type": b["type"], "text": b["text"]} for b in d["blocks"]],
    }
items = [
    {
        "id": r["id"],
        "section": r["key"][0],
        "claim": claims[r["key"]]["claim"],
        "citation": claims[r["key"]].get("citation", ""),
    }
    for r in ordered
]

os.makedirs(OUT, exist_ok=True)
data = json.dumps(
    {"sections": sections, "order": SECTION_ORDER, "items": items}, ensure_ascii=False
)
html = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
open(os.path.join(OUT, "labeling.html"), "w", encoding="utf-8").write(
    html.replace("/*__DATA__*/null", data.replace("</", "<\\/"))
)

hidden = os.path.join(os.path.dirname(os.path.abspath(OUT)), "hidden")
os.makedirs(hidden, exist_ok=True)
with open(os.path.join(hidden, "key-DO-NOT-OPEN.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "section", "extractor", "claim_id", "why"])
    for r in ordered:
        w.writerow([r["id"], *r["key"], r["why"]])

# ChatGPT: one self-contained prompt per section, same blind fields as the page.
gpt = os.path.join(OUT, "chatgpt")
os.makedirs(gpt, exist_ok=True)
head = open(os.path.join(HERE, "chatgpt-instructions.md"), encoding="utf-8").read()
for n, s in enumerate(SECTION_ORDER, 1):
    sec = sections[s]
    prose = []
    for b in sec["blocks"]:
        if b["type"] == "code":
            prose.append("[CODE BLOCK - does not count as prose]\n```\n" + b["text"] + "\n```")
        elif b["type"] == "list_item":
            prose.append("- " + b["text"])
        elif b["type"] == "admonition":
            prose.append("[NOTE BOX] " + b["text"])
        else:
            prose.append(b["text"])
    its = [
        {"id": i["id"], "claim": i["claim"], "citation": i["citation"]}
        for i in items
        if i["section"] == s
    ]
    body = (
        head.replace("{{PROJECT}}", sec["project"])
        .replace("{{BREADCRUMB}}", " > ".join([sec["project"], *sec["breadcrumb"]]))
        .replace("{{SECTION}}", "\n\n".join(prose))
        .replace("{{CLAIMS}}", json.dumps(its, ensure_ascii=False, indent=1))
        .replace("{{COUNT}}", str(len(its)))
    )
    open(os.path.join(gpt, f"{n}-{s}.md"), "w", encoding="utf-8").write(body)

print("items", len(items), Counter(r["why"] for r in rows), Counter(i["section"] for i in items))
