"""Per-section breakdown of run 006 + list of kept cross pairs for the best configs."""

import csv
import sys
from collections import defaultdict
from pathlib import Path

RUN = Path(sys.argv[1])
CFG = [
    ("cross-encoder__nli-deberta-v3-base", "window"),
    ("cross-encoder__nli-deberta-v3-base", "local"),
    ("MoritzLaurer__DeBERTa-v3-base-mnli-fever-anli", "window"),
    ("MoritzLaurer__DeBERTa-v3-base-mnli-fever-anli", "local"),
    ("MoritzLaurer__DeBERTa-v3-large-mnli-fever-anli-ling-wanli", "window"),
    ("MoritzLaurer__DeBERTa-v3-large-mnli-fever-anli-ling-wanli", "local"),
    ("lytang__MiniCheck-DeBERTa-v3-Large", "local"),
    ("vectara__hallucination_evaluation_model", "local"),
]


def rows(model, prem):
    f = RUN / "results" / f"{model}__ctx-breadcrumb__prem-{prem}.csv"
    return list(csv.DictReader(f.open(encoding="utf-8")))


print("## recall / false keeps per section, window 400 (non-cross, labelled, ok rows)")
for m, p in CFG:
    by = defaultdict(lambda: [0, 0, 0, 0])
    for r in rows(m, p):
        if r["window_size"] != "400" or not r["gold"] or r["extractor"].startswith("x-"):
            continue
        b = by[r["section"]]
        kept = r["label"] == "entailment" and r["status"].startswith("ok")
        if r["gold"] == "entailment":
            b[0] += 1
            b[1] += kept
        else:
            b[2] += 1
            b[3] += kept
    cells = "  ".join(f"{s[:14]}:{v[1]}/{v[0]} fk{v[3]}/{v[2]}" for s, v in sorted(by.items()))
    print(f"{m.split('__')[1][:28]:28} {p:6} {cells}")

for m, p in CFG[4:6] + CFG[6:7]:
    print(f"\n## cross kept, {m.split('__')[1]} {p}, window 400")
    for r in rows(m, p):
        cross = r["extractor"].startswith("x-")
        if r["window_size"] == "400" and cross and r["label"] == "entailment":
            src = r["extractor"][2:]
            pe = float(r["p_entailment"])
            print(f"  [{r['section'][:12]} <- {src[:40]}] {r['claim_id']} p={pe:.2f}", end="")
            print(f" | {r['hypothesis'][:110]}")
            print(f"        prem-sentence: {r['citation'][:150]}")
