"""Reference converter (scratch): ingestion.json + results.json + claims.json -> demo run.json v0, trimmed."""
import json, sys, collections, random
ing = json.load(open(sys.argv[1], encoding="utf8"))
res = json.load(open(sys.argv[2], encoding="utf8"))
cl = json.load(open(sys.argv[3], encoding="utf8"))
out = sys.argv[4]
inv = ing["inventory"]
chunks = {c["id"]: c for c in ing["chunks"]}
section_source = {c["section_id"]: c["source"] for c in ing["chunks"]}
docs = collections.OrderedDict()
for c in ing["chunks"]:
    d = docs.setdefault(c["source"], {"source": c["source"], "chunks": 0, "tokens": 0, "symbols": 0, "claims": 0, "claims_kept": 0})
    d["chunks"] += 1; d["tokens"] += c["tokens"]
for s in inv["symbols"]:
    src = section_source.get(s["sources"][0]["section_id"]) if s["sources"] else None
    if src in docs: docs[src]["symbols"] += 1
items = []
for i, x in enumerate(cl["claims"]):
    c = x["claim"]; ch = chunks.get(c["chunk_id"], {})
    src = ch.get("source")
    if src in docs:
        docs[src]["claims"] += 1; docs[src]["claims_kept"] += x["status"] == "kept"
    items.append({
        "id": f'{c["chunk_id"]}:{c["extractor"]}:{c["local_id"]}',
        "extractor": c["extractor"], "source": src, "breadcrumb": ch.get("breadcrumb"),
        "chunk_id": c["chunk_id"], "type": c["type"], "text": c["text"], "citation": c["citation"],
        "status": x["status"], "premise": x.get("premise"), "nli": x.get("nli"), "missing": x.get("missing", []),
    })
kept = sum(1 for x in items if x["status"] == "kept")
run = {
    "schema": "notinspec-demo-run", "schema_version": 0,
    "id": "20261118T1000Z-urllib3-sample", "project": ing["project"], "created_at": res["created_at"],
    "commit": res["commit"], "tool_version": res["tool"]["version"],
    "docs": {"sphinx_version": (ing.get("sphinx") or {}).get("version"), "input_hash": ing["input_hash"], "config_hash": ing["config_hash"]},
    "counts": {"files": len(ing["files"]), "chunks": len(ing["chunks"]), "symbols": len(inv["symbols"]),
               "parameters": sum(len(sig["parameters"]) for s in inv["symbols"] for sig in s["signatures"]),
               "changes": len(inv["changes"]), "warnings": len(ing["warnings"]), "claims": len(items), "claims_kept": kept},
    "steps": [
        {"id": "read", "label": "Read & chunk", "status": "done", "detail": f'{len(ing["files"])} files · {len(ing["chunks"])} chunks'},
        {"id": "inventory", "label": "Build inventory", "status": "done", "detail": f'{len(inv["symbols"])} symbols · {len(inv["changes"])} changes'},
        {"id": "claims", "label": "Extract claims", "status": "done", "detail": f'{len(items)} claims · {len(cl["extractors"])} extractors · {len(cl["sources"])} pages'},
        {"id": "grounding", "label": "Ground claims (citation, NLI, identifiers)", "status": "done", "detail": f"{kept} kept · {len(items)-kept} dropped"},
        {"id": "tests", "label": "Generate tests (L0-L4)", "status": "not_implemented", "detail": "next iteration"},
        {"id": "models", "label": "Run models", "status": "not_implemented", "detail": "next iteration"},
        {"id": "evaluate", "label": "Evaluate & report", "status": "not_implemented", "detail": "next iteration"},
    ],
    "documents": list(docs.values()),
    "symbols": [{"path": s["path"], "kind": s["kind"], "source": section_source.get(s["sources"][0]["section_id"]) if s["sources"] else None,
                 "parameters": [p["name"] for sig in s["signatures"] for p in sig["parameters"]]} for s in inv["symbols"]],
    "changes": [{"symbol": c["symbol"], "kind": c["kind"], "version": c["version"], "parameter": c["parameter"], "replacement": c["replacement"]} for c in inv["changes"]],
    "warnings": ing["warnings"],
    "claims": {"sources": cl["sources"], "extractors": [e["model"] for e in cl["extractors"]], "counts": cl["counts"],
               "versions": cl["versions"], "items": items},
}
json.dump(run, open(out + ".full.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
# trimmed fixture: every dropped claim + 40 kept ones, symbols capped at 60
random.seed(1)
keptl = [x for x in items if x["status"] == "kept"]
run["claims"]["items"] = [x for x in items if x["status"] != "kept"] + random.sample(keptl, 40)
run["symbols"] = run["symbols"][:60]
json.dump(run, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(json.dumps(run["counts"]), len(run["claims"]["items"]))
