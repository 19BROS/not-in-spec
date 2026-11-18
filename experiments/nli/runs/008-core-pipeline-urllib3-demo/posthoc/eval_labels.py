"""Run 008: core pipeline decisions vs. blind human labels.

usage: uv run python -I -X utf8 eval_labels.py <claims.json> <key-008.csv> <labels-human-008.csv>

A claim is good when the human label is `entailment` (the prose supports it). The sample is
stratified, not random: every dropped claim is in it, kept claims only partly. So precision of
kept claims is computed on the kept claims of the sample (a random sample of them per kind),
and recall is reported as counts of good claims per status, never as one overall number.
"""

import csv
import json
import sys
from collections import Counter, defaultdict

claims_path, key_path, labels_path = sys.argv[1:4]
data = json.loads(open(claims_path, encoding="utf-8").read())
claims = {
    (c["claim"]["chunk_id"], c["claim"]["extractor"], c["claim"]["local_id"]): c
    for c in data["claims"]
}
key = {r["id"]: r for r in csv.DictReader(open(key_path, encoding="utf-8"))}
labels = {r["id"]: r for r in csv.DictReader(open(labels_path, encoding="utf-8")) if r["verdict"]}
missing = sorted(set(key) - set(labels))
print(f"labelled {len(labels)} of {len(key)}" + (f"; missing {missing[:10]}" if missing else ""))

rows = []
for i, k in key.items():
    if i not in labels:
        continue
    c = claims[(k["chunk_id"], k["extractor"], k["local_id"])]
    rows.append(
        {
            "id": i,
            "status": k["status"],
            "kind": k["kind"],
            "extractor": k["extractor"],
            "gold": labels[i]["verdict"],
            "borderline": labels[i]["borderline"] == "yes",
            "matches": c["citation_matches"],
            "missing": c["missing"],
            "nli": c["nli"]["entailment"] if c["nli"] else None,
        }
    )


def table(title, group):
    print(f"\n## {title}")
    cells = defaultdict(Counter)
    for r in rows:
        cells[group(r)][r["gold"]] += 1
    print(f"{'':32} {'entail':>7} {'neutral':>8} {'contra':>7} {'good %':>7}")
    for g in sorted(cells):
        c = cells[g]
        n = sum(c.values())
        print(
            f"{g:32} {c['entailment']:>7} {c['neutral']:>8} {c['contradiction']:>7} "
            f"{100 * c['entailment'] / n:>6.0f}%"
        )


table("status × gold (all sampled)", lambda r: r["status"])
table("kept: precision by kind", lambda r: f"kept / {r['kind']}" if r["status"] == "kept" else "~")
table(
    "kept: precision by extractor",
    lambda r: f"kept / {r['extractor']}" if r["status"] == "kept" else "~",
)
table("status × kind", lambda r: f"{r['status']} / {r['kind']}")

print("\n## identifier check")
id_drops = [r for r in rows if r["status"] == "id_missing"]
print(
    f"id_missing sampled: {len(id_drops)}, of them good (false drops): "
    f"{sum(r['gold'] == 'entailment' for r in id_drops)}"
)
nli_drops_with_ids = [r for r in rows if r["status"].startswith("nli_") and r["missing"]]
print(
    f"NLI-dropped claims the id check would also drop: {len(nli_drops_with_ids)}, good: "
    f"{sum(r['gold'] == 'entailment' for r in nli_drops_with_ids)}"
)
for r in id_drops:
    print(f"  {r['id']} gold={r['gold']:<13} missing={r['missing']}")

print("\n## repeated citations")
all_found = [c for c in data["claims"] if c["citation_matches"] > 1]
print(
    f"claims whose citation is in the prose more than once: {len(all_found)} of "
    f"{len(data['claims'])}"
)
multi = [r for r in rows if r["matches"] > 1]
print(
    f"sampled: {len(multi)}, gold: {Counter(r['gold'] for r in multi)}, "
    f"status: {Counter(r['status'] for r in multi)}"
)

print("\n## borderline labels:", sum(r["borderline"] for r in rows))
