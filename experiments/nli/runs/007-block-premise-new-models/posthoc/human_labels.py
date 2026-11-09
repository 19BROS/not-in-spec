"""Score runs 006 and 007 on the human labels (labels-human.csv, labels-human-cross.csv).

usage (from experiments/nli): python runs/007-block-premise-new-models/posthoc/human_labels.py
Read-only; prints the tables used in FINDINGS.md.
"""

import csv
import glob
import math
import os
from collections import Counter

csv.field_size_limit(10**9)
NLI = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
REF = "007 wanli-large local-block"
COMPARE = (
    "007 wanli-large local",
    "006 wanli-large window-400",
    "006 wanli-large window-128",
    "007 deberta-v3-large-zeroshot-v2.0 local-block",
    "007 ModernBERT-large-zeroshot-v2.0 local-block",
    "007 ModernBERT-large-nli local-block",
    "007 DeBERTa-v3-base-mnli-fever-anli local-block",
)


def read(name):
    with open(os.path.join(NLI, name), encoding="utf-8") as f:
        return {(r["section"], r["extractor"], r["claim_id"]): r for r in csv.DictReader(f)}


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[x] * cb[x] for x in set(ca) | set(cb)) / n / n
    return po, (po - pe) / (1 - pe)


def mcnemar(right_a, right_b):
    """(only a right, only b right, exact two-sided p)."""
    x, y = len(right_a - right_b), len(right_b - right_a)
    n = x + y
    tail = sum(math.comb(n, i) for i in range(min(x, y) + 1))
    return x, y, float(f"{min(1.0, 2 * tail / 2**n):.2g}") if n else 1.0


def load_setups():
    """name -> kept keys, p_entailment and the number of cross pairs."""
    setups = {}
    for f in sorted(glob.glob(os.path.join(NLI, "runs", "00[67]*", "results", "*.csv"))):
        run = os.path.basename(os.path.dirname(os.path.dirname(f)))[:3]
        model, _, prem = os.path.basename(f)[:-4].partition("__ctx-breadcrumb__prem-")
        model = model.split("__", 1)[-1]
        model = model.replace("DeBERTa-v3-large-mnli-fever-anli-ling-wanli", "wanli-large")
        with open(f, encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        # local premises don't depend on the window size, so one size is enough
        for ws in ("400", "128") if prem == "window" else ("128",):
            sized = [r for r in rows if r["window_size"] == ws]
            key = [(r["section"], r["extractor"], r["claim_id"]) for r in sized]
            name = f"{run} {model} {prem}" + (f"-{ws}" if prem == "window" else "")
            setups[name] = {
                "kept": {
                    k
                    for k, r in zip(key, sized, strict=True)
                    if r["status"].startswith("ok") and r["label"] == "entailment"
                },
                "p": {k: float(r["p_entailment"] or 0) for k, r in zip(key, sized, strict=True)},
                "n_cross": sum(k[1].startswith("x-") for k in key),
            }
    return setups


human, cross, draft = read("labels-human.csv"), read("labels-human-cross.csv"), read("labels.csv")
pos = {k for k, v in human.items() if v["gold"] == "entailment"}
neg = set(human) - pos
cross_ok = {k for k, v in cross.items() if v["gold"] == "entailment"}

n_bl = sum(v["borderline"] == "yes" for v in human.values())
print(
    f"Human sample: {len(human)} claims, {n_bl} borderline;",
    dict(Counter(v["gold"] for v in human.values())),
)
p3 = [(v["gold"], draft[k]["gold"]) for k, v in human.items()]
po3, k3 = kappa(p3)
po2, k2 = kappa([(a == "entailment", b == "entailment") for a, b in p3])
print(
    f"Human vs claude-draft: 3-way {po3:.1%} (kappa {k3:.2f}), keep/drop {po2:.1%} (kappa {k2:.2f})"
)
for k, v in sorted(human.items()):
    if (v["gold"] == "entailment") != (draft[k]["gold"] == "entailment"):
        print(f"  keep/drop disagreement: {k} human={v['gold']} draft={draft[k]['gold']}")
print(
    f"Cross sample: {len(cross)} pairs kept by at least one compared setup;",
    dict(Counter(v["gold"] for v in cross.values())),
)

setups = load_setups()
print(f"\n{'setup':52} recall/{len(pos)}  false keeps/{len(neg)}  cross kept (wrong / supported)")


def order(item):
    kept = item[1]["kept"]
    return len(kept & pos) - 2 * len(kept & neg)


for name, s in sorted(setups.items(), key=order):
    kept = s["kept"]
    ck = {x for x in kept if x[1].startswith("x-")}
    unlabeled = len(ck - set(cross))
    detail = (
        f"{unlabeled} not human-labelled"
        if unlabeled
        else f"{len(ck - cross_ok)} / {len(ck & cross_ok)}"
    )
    counts = f"{len(kept & pos):3}        {len(kept & neg):3}"
    print(f"  {name:52} {counts}            {len(ck)}/{s['n_cross']} ({detail})")

ref = setups[REF]["kept"]
# Cross pairs outside the human sample were kept by none of the compared setups: correctly dropped.
all_cross = {k for k in setups[REF]["p"] if k[1].startswith("x-")}


def right(kept):
    return {k for k in human if (k in kept) == (k in pos)}


def right_cross(kept):
    return {k for k in all_cross if (k in kept) == (k in cross_ok)}


print(f"\nMcNemar vs {REF} (only ref right / only other right / p)")
for name in COMPARE:
    print(f"  same-section {name:48} {mcnemar(right(ref), right(setups[name]['kept']))}")
for name in COMPARE[:2] + COMPARE[3:4]:
    print(
        f"  cross pairs  {name:48} {mcnemar(right_cross(ref), right_cross(setups[name]['kept']))}"
    )

p = setups[REF]["p"]
print(f"\nThreshold sweep, {REF} (keep if p_entailment >= t; dropped by the citation check = 0)")
for t in (0.9, 0.5, 0.1, 0.05, 0.01, 0.001):
    gd = sum(p.get(k, 0) < t for k in pos)
    bk = sum(p.get(k, 0) >= t for k in neg)
    print(f"  t={t:<6} good dropped {gd:2}/{len(pos)}  bad kept {bk:2}/{len(neg)}")
for lo in (0.01, 0.05):
    rev = [k for k in human if lo <= p.get(k, 0) < 0.9]
    good_rev, bad_rev = sum(k in pos for k in rev), sum(k in neg for k in rev)
    auto_drop = sum(p.get(k, 0) < lo for k in pos)
    auto_keep = sum(p.get(k, 0) >= 0.9 for k in neg)
    print(
        f"  zones keep>=0.9 / review [{lo},0.9) / drop<{lo}: review {len(rev)}/{len(human)}"
        f" (good {good_rev}, bad {bad_rev});"
        f" good auto-dropped {auto_drop}, bad auto-kept {auto_keep}"
    )
