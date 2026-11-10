"""Round 2: blind page for cross-section pairs that any compared NLI setup kept.

A cross pair is a claim from section A judged against the prose of section B.

usage: python -X utf8 build_cross.py <repo-root> <out-dir>
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
R = os.path.join(N, "runs")
HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261109
SECTION_ORDER = [
    "using-timeouts",
    "retrying-requests",
    "configuring-exponential-backoff",
    "httpx-timeouts-fine-tuning",
    "changelog-2-8-0-security",
    "changelog-2-8-0-bugfixes",
]
W = "MoritzLaurer__DeBERTa-v3-large-mnli-fever-anli-ling-wanli__ctx-breadcrumb__prem-"
SOURCES = [  # (run, file, window_size): the setups we compare
    ("007-block-premise-new-models", W + "local-block", "128"),
    ("007-block-premise-new-models", W + "local", "128"),
    ("006-realistic-negatives", W + "window", "400"),
    ("006-realistic-negatives", W + "window", "128"),
    (
        "007-block-premise-new-models",
        "MoritzLaurer__deberta-v3-large-zeroshot-v2.0__ctx-breadcrumb__prem-local-block",
        "128",
    ),
    (
        "007-block-premise-new-models",
        "MoritzLaurer__ModernBERT-large-zeroshot-v2.0__ctx-breadcrumb__prem-local-block",
        "128",
    ),
]

picked = {}
for run, name, ws in SOURCES:
    for r in csv.DictReader(open(os.path.join(R, run, "results", name + ".csv"), encoding="utf-8")):
        if r["window_size"] != ws or not r["extractor"].startswith("x-"):
            continue
        k = (r["section"], r["extractor"], r["claim_id"])
        if r["status"].startswith("ok") and r["label"] == "entailment":
            picked.setdefault(k, r)

rng = random.Random(SEED)
keys = sorted(picked)
ids = [f"x{n:03d}" for n in rng.sample(range(100, 1000), len(keys))]
rows = list(zip(ids, keys, strict=True))
by_sec = {s: [x for x in rows if x[1][0] == s] for s in SECTION_ORDER}
for s in SECTION_ORDER:
    rng.shuffle(by_sec[s])
ordered = [x for s in SECTION_ORDER for x in by_sec[s]]

sections = {}
for s in SECTION_ORDER:
    d = json.load(open(os.path.join(N, "sections", s, "section.json"), encoding="utf-8"))
    sections[s] = {
        "project": d["source"]["project"],
        "breadcrumb": d["breadcrumb"],
        "blocks": [{"type": b["type"], "text": b["text"]} for b in d["blocks"]],
    }
order = [s for s in SECTION_ORDER if by_sec[s]]
items = [
    {"id": i, "section": k[0], "claim": picked[k]["hypothesis"], "citation": picked[k]["citation"]}
    for i, k in ordered
]

os.makedirs(OUT, exist_ok=True)
data = json.dumps(
    {
        "sections": sections,
        "order": order,
        "items": items,
        "storeKey": "nis-blind-labels-cross-v1",
        "file": "labels-human-cross.csv",
        "title": "Blind labeling – kolo 2",
    },
    ensure_ascii=False,
)
html = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
open(os.path.join(OUT, "labeling-cross.html"), "w", encoding="utf-8").write(
    html.replace("/*__DATA__*/null", data.replace("</", "<\\/"))
)

hidden = os.path.join(os.path.dirname(os.path.abspath(OUT)), "hidden")
os.makedirs(hidden, exist_ok=True)
with open(
    os.path.join(hidden, "key-cross-DO-NOT-OPEN.csv"), "w", encoding="utf-8", newline=""
) as f:
    w = csv.writer(f)
    w.writerow(["id", "section", "extractor", "claim_id"])
    for i, k in ordered:
        w.writerow([i, *k])
print("items", len(items), Counter(i["section"] for i in items))
