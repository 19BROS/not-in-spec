"""Build the blind labelling page for run 008 and its hidden key (read-only on the repo).

usage: uv run python -I -X utf8 build_008.py <claims.json> <config> <out-dir>

<claims.json> comes from `notinspec claims run` (core pipeline) on the urllib3 demo pages. The
page uses template.html, with each claim's chunk as its section (code, tables and signatures
grey). The hidden key goes to <out-dir>/../hidden/. Same seed + same claims.json give the same
ids and order.

Sample (stratified by status and by guide vs. API reference): every claim NLI or the identifier
check dropped, every claim whose citation was not found, a few `not_checkable` ones, and kept
claims at random, half from guides and half from the API reference.
"""

import csv
import json
import random
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

from notinspec.config import load_config
from notinspec.ingestion import ingest

CLAIMS, CONFIG, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
HERE = Path(__file__).resolve().parent
SEED = 20261117
TOTAL = 180
NOT_CHECKABLE = 10
CODE_KINDS = {"code", "table", "signature", "html"}
LIST_ITEM = re.compile(r"^[ \t]*(?:[-*+]|\d{1,9}[.)])[ \t]+")


def kind(source: str) -> str:
    return "api" if source.startswith("reference/") else "guide"


def blocks(chunk) -> list[dict[str, str]]:
    lines = chunk.text.split("\n")
    out = []
    for block in chunk.blocks:
        if block.nested or block.kind == "heading":
            continue
        text = "\n".join(
            lines[block.start_line - chunk.start_line : block.end_line - chunk.start_line + 1]
        )
        if block.kind in CODE_KINDS:
            out.append({"type": "code", "text": block.code or text})
        elif block.kind in ("list", "field"):
            items: list[list[str]] = []
            for line in text.split("\n"):
                if LIST_ITEM.match(line) or not items:
                    items.append([LIST_ITEM.sub("", line)])
                else:
                    items[-1].append(line.strip())
            out += [
                {"type": "list_item", "text": " ".join(i).strip()}
                for i in items
                if "".join(i).strip()
            ]
        elif block.kind == "admonition":
            out.append({"type": "admonition", "text": " ".join(text.split())})
        else:
            out.append({"type": "paragraph", "text": " ".join(text.split())})
    return out


data = json.loads(CLAIMS.read_text(encoding="utf-8"))
ingestion = ingest(load_config(CONFIG), output=Path(tempfile.mkdtemp()))
chunks = {c.id: c for c in ingestion.chunks}
claims = data["claims"]
for n, c in enumerate(claims):
    c["_n"] = n
    c["_kind"] = kind(chunks[c["claim"]["chunk_id"]].source)

rng = random.Random(SEED)
picked: list[tuple[dict, str]] = []
for c in claims:
    if c["status"] in ("nli_neutral", "nli_contradiction", "id_missing", "citation_not_found"):
        picked.append((c, c["status"]))
unchecked = [c for c in claims if c["status"] == "not_checkable"]
rng.shuffle(unchecked)
picked += [(c, "not_checkable") for c in unchecked[:NOT_CHECKABLE]]
rest = TOTAL - len(picked)
for k, share in (("guide", rest // 2), ("api", rest - rest // 2)):
    kept = [c for c in claims if c["status"] == "kept" and c["_kind"] == k]
    rng.shuffle(kept)
    picked += [(c, f"kept-{k}") for c in kept[:share]]
if len(picked) < TOTAL:  # one kind has fewer kept claims than its share: fill from the other
    used = {c["_n"] for c, _ in picked}
    more = [c for c in claims if c["status"] == "kept" and c["_n"] not in used]
    rng.shuffle(more)
    picked += [(c, f"kept-{c['_kind']}") for c in more[: TOTAL - len(picked)]]

ids = [f"q{n:03d}" for n in rng.sample(range(100, 1000), len(picked))]
rows = [{"id": i, "claim": c, "why": why} for i, (c, why) in zip(ids, picked, strict=True)]
order = list(
    dict.fromkeys(
        c.id for c in ingestion.chunks if any(r["claim"]["claim"]["chunk_id"] == c.id for r in rows)
    )
)
by_chunk = {k: [r for r in rows if r["claim"]["claim"]["chunk_id"] == k] for k in order}
for k in order:
    rng.shuffle(by_chunk[k])
ordered = [r for k in order for r in by_chunk[k]]

sections = {
    k: {
        "project": ingestion.project,
        "breadcrumb": list(chunks[k].heading_path) or [chunks[k].source],
        "blocks": blocks(chunks[k]),
    }
    for k in order
}
items = [
    {
        "id": r["id"],
        "section": r["claim"]["claim"]["chunk_id"],
        "claim": r["claim"]["claim"]["text"],
        "citation": r["claim"]["claim"]["citation"],
    }
    for r in ordered
]
page = {
    "sections": sections,
    "order": order,
    "items": items,
    "storeKey": "nis-blind-labels-008",
    "file": "labels-human-008.csv",
    "title": "Blind labeling · run 008",
}
OUT.mkdir(parents=True, exist_ok=True)
html = (HERE / "template.html").read_text(encoding="utf-8")
data_js = json.dumps(page, ensure_ascii=False).replace("</", "<\\/")
(OUT / "labeling-008.html").write_text(html.replace("/*__DATA__*/null", data_js), encoding="utf-8")

hidden = OUT.resolve().parent / "hidden"
hidden.mkdir(exist_ok=True)
with open(hidden / "key-008-DO-NOT-OPEN.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "chunk_id", "extractor", "local_id", "status", "kind", "why"])
    for r in ordered:
        c = r["claim"]
        w.writerow(
            [
                r["id"],
                c["claim"]["chunk_id"],
                c["claim"]["extractor"],
                c["claim"]["local_id"],
                c["status"],
                c["_kind"],
                r["why"],
            ]
        )
print("items", len(items), "chunks", len(order), Counter(r["why"] for r in rows))
