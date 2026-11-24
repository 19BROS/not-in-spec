"""SCRUM-54: measure embeddings as a candidate prefilter and audit semantic diff skipping.

Developer experiment only. Uses the model card's masked mean pooling and L2 normalization.
Model and tokenizer revisions are pinned. No production prefilter or CI diff rule is changed.
"""

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
ENCODING = {
    "version": 1,
    "max_length": 256,
    "pooling": "attention-masked-mean",
    "normalization": "L2",
    "dtype": "float32",
    "tokenizer": "fast",
    "truncation_side": "right",
    "padding": "longest",
    "threads": 4,
    "batch_size": 32,
}


def cache_key(texts):
    return hashlib.sha256(
        json.dumps(
            {
                "model": MODEL,
                "revision": REVISION,
                "encoding": ENCODING,
                "texts": texts,
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()


def encode(texts):
    import torch
    from transformers import AutoModel, AutoTokenizer

    torch.set_num_threads(ENCODING["threads"])
    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION, use_fast=True)
    tokenizer.truncation_side = ENCODING["truncation_side"]
    model = AutoModel.from_pretrained(MODEL, revision=REVISION).float().eval()
    vectors = []
    truncated = 0
    started = time.perf_counter()
    for start in range(0, len(texts), ENCODING["batch_size"]):
        batch = texts[start : start + ENCODING["batch_size"]]
        lengths = tokenizer(batch, truncation=False)["input_ids"]
        truncated += sum(len(ids) > ENCODING["max_length"] for ids in lengths)
        inputs = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=ENCODING["max_length"],
            return_tensors="pt",
        )
        with torch.inference_mode():
            tokens = model(**inputs).last_hidden_state
            mask = inputs["attention_mask"].unsqueeze(-1).to(tokens.dtype)
            means = (tokens * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
            vectors.extend(torch.nn.functional.normalize(means, p=2, dim=1).tolist())
    return vectors, {
        "encoding_seconds": round(time.perf_counter() - started, 3),
        "truncated_texts": truncated,
        "threads": ENCODING["threads"],
        "batch_size": ENCODING["batch_size"],
    }


def diff_cases():
    from notinspec.config import load_config
    from notinspec.ingestion import ingest

    sources = {}
    for library in ("trio", "urllib3"):
        data = ingest(
            load_config(ROOT / "core/examples/sphinx" / library / "notinspec.yaml"),
            output=ROOT / "tmp/embedding-benchmark",
        )
        sources.update({c.id: c for c in data.chunks})
    definitions = [
        ("whitespace", "e1726e8f38d96ea4", "Returns True", "Returns  True", False),
        ("boolean", "e1726e8f38d96ea4", "Returns True", "Returns False", True),
        (
            "unit",
            "d679418e605bafc2",
            "the given number of seconds",
            "the given number of milliseconds",
            True,
        ),
        ("negation", "cd03d7574e56c44f", "will not work by default", "will work by default", True),
        ("version", "cd03d7574e56c44f", "TLS 1.2", "TLS 1.0", True),
        ("identifier", "c46995b2a905490b", "ProxyManager", "PoolManager", True),
        # Keep the previous blind spot explicitly, separate from visible semantic edits.
        ("truncation_control", "4d0da13f85e52a1f", "isn’t required", "is required", True),
    ]
    rows = []
    for kind, chunk_id, old, new, semantic in definitions:
        chunk = sources.get(chunk_id)
        if chunk is None or old not in chunk.text:
            raise ValueError(f"diff {kind}: chunk {chunk_id} must contain {old!r}")
        rows.append(
            {
                "kind": kind,
                "chunk_id": chunk_id,
                "source": chunk.source,
                "before": chunk.text,
                "after": chunk.text.replace(old, new, 1),
                "semantic_change": semantic,
                "edit": {"old": old, "new": new, "start": chunk.text.index(old)},
            }
        )
    return rows


def audit_edit_window(case, tokenizer):
    """Audit both actual encoded inputs; a truncated edit is not a semantic-model failure."""
    encoded = {}
    visibility = {}
    lengths = {}
    for side, edit_key in (("before", "old"), ("after", "new")):
        text = case[side]
        full = tokenizer(text, truncation=False)
        kept = tokenizer(
            text, truncation=True, max_length=ENCODING["max_length"], return_offsets_mapping=True
        )
        encoded[side] = kept["input_ids"]
        lengths[side] = len(full["input_ids"])
        retained_end = max((end for _, end in kept["offset_mapping"]), default=0)
        visibility[side] = case["edit"]["start"] + len(case["edit"][edit_key]) <= retained_end
    return {
        "edit_inside_window": visibility,
        "encoded_input_changed": encoded["before"] != encoded["after"],
        "token_count": lengths,
        "truncated": {side: length > ENCODING["max_length"] for side, length in lengths.items()},
    }


def skipping_audit(diffs, threshold):
    return [
        r["kind"]
        for r in diffs
        if r["semantic_change"]
        and all(r["edit_inside_window"].values())
        and r["encoded_input_changed"]
        and r["cosine"] >= threshold
    ]


def pair_key(a, b):
    return tuple(sorted((a, b)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=ROOT / "tmp/embedding-vectors.json")
    parser.add_argument("--out", type=Path, default=HERE / "results.json")
    args = parser.parse_args()
    import numpy as np
    from transformers import AutoTokenizer

    fixture = ROOT / "core/tests/crosscheck/fixtures"
    raw = (fixture / "run009-claims.json").read_bytes()
    claims = [r for r in json.loads(raw) if r["status"] == "kept"]
    texts = [r["claim"]["text"] for r in claims]
    known = json.loads((fixture / "nli-k5a-run009.json").read_text(encoding="utf-8"))
    labels = {
        (r["premise"], r["hypothesis"]): max(
            ("entailment", "neutral", "contradiction"), key=lambda label: r[label]
        )
        for r in known
    }
    diffs = diff_cases()
    all_texts = list(dict.fromkeys(texts + [r[k] for r in diffs for k in ("before", "after")]))
    key = cache_key(all_texts)
    cached = json.loads(args.cache.read_text(encoding="utf-8")) if args.cache.exists() else {}
    if cached.get("key") == key:
        vectors, timing = cached["vectors"], cached["timing"]
    else:
        vectors, timing = encode(all_texts)
        args.cache.parent.mkdir(parents=True, exist_ok=True)
        args.cache.write_text(
            json.dumps({"key": key, "encoding": ENCODING, "vectors": vectors, "timing": timing}),
            encoding="utf-8",
        )
    lookup = {text: np.asarray(vector) for text, vector in zip(all_texts, vectors, strict=True)}
    matrix = np.asarray([lookup[t] for t in texts])
    similarity = matrix @ matrix.T
    eligible = set()
    recorded = {}
    for i, left in enumerate(claims):
        for j in range(i + 1, len(claims)):
            right = claims[j]
            if (
                left["claim"]["chunk_id"] != right["claim"]["chunk_id"]
                or left["claim"]["extractor"] == right["claim"]["extractor"]
            ):
                continue
            eligible.add((i, j))
            forward = labels.get((texts[i], texts[j]))
            backward = labels.get((texts[j], texts[i]))
            if forward is not None and backward is not None:
                if forward == backward == "contradiction":
                    relation = "contradiction"
                elif forward == backward == "entailment":
                    relation = "duplicate"
                elif "entailment" in (forward, backward):
                    relation = "more_specific"
                else:
                    relation = "different"
                recorded[i, j] = relation
    variants = []
    for k in (1, 2, 3, 5, 8):
        selected = set()
        for i in range(len(claims)):
            neighbors = [j for j in range(len(claims)) if pair_key(i, j) in eligible]
            neighbors.sort(key=lambda j: (-float(similarity[i, j]), j))
            selected.update(pair_key(i, j) for j in neighbors[:k])
        variants.append(
            {
                "top_k": k,
                "candidate_pairs": len(selected),
                "fraction_of_all_pairs": len(selected) / len(eligible),
                "recorded_relations_retained": {
                    relation: {
                        "retained": sum(
                            pair in selected for pair, rel in recorded.items() if rel == relation
                        ),
                        "available": sum(rel == relation for rel in recorded.values()),
                    }
                    for relation in ("duplicate", "more_specific", "contradiction")
                },
            }
        )
    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION, use_fast=True)
    tokenizer.truncation_side = ENCODING["truncation_side"]
    for case in diffs:
        case.update(audit_edit_window(case, tokenizer))
        # Roundoff in float32 can put a dot product just outside [-1, 1].
        case["cosine"] = max(-1.0, min(1.0, float(lookup[case["before"]] @ lookup[case["after"]])))
        case["content_hash_changed"] = (
            hashlib.sha256(case["before"].encode()).hexdigest()
            != hashlib.sha256(case["after"].encode()).hexdigest()
        )
    results = {
        "schema_version": 2,
        "model": MODEL,
        "revision": REVISION,
        "method": (f"masked mean pooling; L2 normalized; {ENCODING['max_length']} wordpieces; CPU"),
        "encoding": ENCODING,
        "fixture_sha256": hashlib.sha256(raw).hexdigest(),
        "timing": timing,
        "claims": len(claims),
        "chunks": len({r["claim"]["chunk_id"] for r in claims}),
        "all_eligible_pairs": len(eligible),
        "pairs_with_recorded_scores": len(recorded),
        "recorded_relation_counts": dict(Counter(recorded.values())),
        "crosscheck_variants": variants,
        "diff_cases": diffs,
        "diff_skipping_audit": {
            str(threshold): skipping_audit(diffs, threshold) for threshold in (0.9, 0.95, 0.99)
        },
        "encoding_blind_spots": [
            r["kind"] for r in diffs if r["semantic_change"] and not r["encoded_input_changed"]
        ],
        "limits": [
            "Recorded NLI relations are a silver reference, not human judgments.",
            "Scores cover only the existing premise-overlap subset of four urllib3 chunks.",
            "Retention is conditional on that subset; no K5b recall estimate is available.",
            "Diff mutations are controlled examples, not a measured production distribution.",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {key: value for key, value in results.items() if key not in ("diff_cases", "limits")},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
