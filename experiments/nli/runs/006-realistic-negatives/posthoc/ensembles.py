"""Post-hoc ensembles on run 006 CSVs: keep only if every member says entailment (window 400)."""

import csv
import sys
from itertools import combinations
from pathlib import Path

RES = Path(sys.argv[1]) / "results"
LARGE = "MoritzLaurer__DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
BASE = "MoritzLaurer__DeBERTa-v3-base-mnli-fever-anli"
M = {
    "large-local": f"{LARGE}__ctx-breadcrumb__prem-local",
    "large-window": f"{LARGE}__ctx-breadcrumb__prem-window",
    "basemnli-local": f"{BASE}__ctx-breadcrumb__prem-local",
    "basemnli-window": f"{BASE}__ctx-breadcrumb__prem-window",
    "minicheck-local": "lytang__MiniCheck-DeBERTa-v3-Large__ctx-breadcrumb__prem-local",
    "ce-base-local": "cross-encoder__nli-deberta-v3-base__ctx-breadcrumb__prem-local",
}
data = {}
for k, f in M.items():
    for r in csv.DictReader((RES / f"{f}.csv").open(encoding="utf-8")):
        if r["window_size"] != "400" or not r["gold"]:
            continue
        key = (r["section"], r["extractor"], r["claim_id"])
        d = data.setdefault(
            key,
            {
                "gold": r["gold"],
                "cross": r["extractor"].startswith("x-"),
                "ok": r["status"].startswith("ok"),
            },
        )
        d[k] = r["label"] == "entailment"


def score(members):
    pos = tp = neg = fk = cr = ck = 0
    for d in data.values():
        if not d["ok"]:
            continue
        kept = all(d[m] for m in members)
        if d["cross"]:
            cr += 1
            ck += kept
        elif d["gold"] == "entailment":
            pos += 1
            tp += kept
        else:
            neg += 1
            fk += kept
    return f"recall {tp}/{pos} = {tp / pos:.0%}, false keeps {fk}/{neg}, cross kept {ck}/{cr}"


for n in (1, 2):
    for c in combinations(M, n):
        print(f"{' + '.join(c):40} {score(c)}")
