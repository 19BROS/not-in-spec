"""SCRUM-46: recorded human benchmark and frozen controls on real Sphinx documents.

Run from the repository root with `uv run --extra nli python experiments/nli/validation/run.py`.
The 36 control labels were authored from the documentation before running NLI. They are
AI-authored controls, not independent human labels or an estimate of production precision.
This developer experiment can load the local model; project tests and CI do not invoke it.
"""

import argparse
import csv
import hashlib
import json
import platform
import time
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from notinspec.chunking import CHUNKER_VERSION, WINDOWS_VERSION
from notinspec.config import load_config
from notinspec.grounding import (
    GROUNDING_VERSION,
    check_citation,
    inventory_names,
    missing_identifiers,
    nli_premise,
    section_reference,
)
from notinspec.ingestion import ingest
from notinspec.nli import RecordingNli, TransformersNli

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LABELS = ("entailment", "neutral", "contradiction")


def metrics(rows):
    matrix = {gold: {pred: 0 for pred in LABELS} for gold in LABELS}
    for row in rows:
        matrix[row["gold"]][row["label"]] += 1
    tp = sum(r["gold"] == r["label"] == "entailment" for r in rows)
    fp = sum(r["gold"] != "entailment" and r["label"] == "entailment" for r in rows)
    fn = sum(r["gold"] == "entailment" and r["label"] != "entailment" for r in rows)
    tn = len(rows) - tp - fp - fn
    return {
        "count": len(rows),
        "confusion_gold_rows": matrix,
        "correct_three_way": sum(r["gold"] == r["label"] for r in rows),
        "keep_drop": {"true_keep": tp, "false_keep": fp, "false_drop": fn, "true_drop": tn},
        "keep_precision": tp / (tp + fp) if tp + fp else None,
        "keep_recall": tp / (tp + fn) if tp + fn else None,
    }


def historical():
    base = ROOT / "experiments/nli"
    with (base / "labels-human.csv").open(encoding="utf-8", newline="") as file:
        gold = list(csv.DictReader(file))
    source = (
        base
        / "runs/007-block-premise-new-models/results"
        / (
            "MoritzLaurer__DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
            "__ctx-breadcrumb__prem-local-block.csv"
        )
    )
    with source.open(encoding="utf-8", newline="") as file:
        predictions = {
            (r["section"], r["extractor"], r["claim_id"]): r
            for r in csv.DictReader(file)
            if r["window_size"] == "128"
        }
    rows = []
    for item in gold:
        prediction = predictions[item["section"], item["extractor"], item["claim_id"]]
        # No NLI premise is a pre-NLI rejection, never an invented three-way prediction.
        label = prediction["label"] if prediction["status"].startswith("ok") else None
        rows.append({**item, "label": label, "status": prediction["status"]})
    scored = [r for r in rows if r["label"] in LABELS]
    return {
        "sample_count": len(rows),
        "nli_scored": metrics(scored),
        "pre_nli_rejections": [r for r in rows if r["label"] is None],
        "pipeline_keep_drop": {
            "true_keep": sum(r["gold"] == r["label"] == "entailment" for r in rows),
            "false_keep": sum(
                r["gold"] != "entailment" and r["label"] == "entailment" for r in rows
            ),
            "false_drop": sum(
                r["gold"] == "entailment" and r["label"] != "entailment" for r in rows
            ),
            "true_drop": sum(
                r["gold"] != "entailment" and r["label"] != "entailment" for r in rows
            ),
        },
        "by_section": {
            s: metrics([r for r in scored if r["section"] == s])
            for s in sorted({r["section"] for r in rows})
        },
    }


def controls(model):
    cases_bytes = (HERE / "cases.json").read_bytes()
    cases = json.loads(cases_bytes)
    libraries = {}
    rows = []
    for index, case in enumerate(cases):
        library = case["library"]
        if library not in libraries:
            config = load_config(ROOT / "core/examples/sphinx" / library / "notinspec.yaml")
            libraries[library] = ingest(config, output=ROOT / "tmp/nli-validation")
        data = libraries[library]
        chunk = next(c for c in data.chunks if c.id == case["chunk_id"])
        match = check_citation(chunk, case["citation"])
        if match.status != "found":
            raise ValueError(f"case {index}: citation {match.status}")
        premises = [nli_premise(chunk, span) for span in match.spans]
        section = [c for c in data.chunks if c.section_id == chunk.section_id]
        reference = section_reference(section, data.inventory)
        for gold, hypothesis in case["claims"]:
            scores = model.score([(p.text, hypothesis) for p in premises])
            best = max(
                range(len(scores)),
                key=lambda i: (scores[i].label == "entailment", scores[i].entailment),
            )
            missing = missing_identifiers(
                hypothesis,
                reference,
                project=data.project,
                known_names=inventory_names(data.inventory),
            )
            rows.append(
                {
                    "id": f"control-{len(rows) + 1:03}",
                    "library": library,
                    "scope": case["scope"],
                    "chunk_id": chunk.id,
                    "source": chunk.source,
                    "breadcrumb": chunk.breadcrumb,
                    "input_hash": data.input_hash,
                    "content_hash": chunk.content_hash,
                    "citation": case["citation"],
                    "gold": gold,
                    "hypothesis": hypothesis,
                    "premise": premises[best].text,
                    "scores": asdict(scores[best]),
                    "label": scores[best].label,
                    "missing_identifiers": missing,
                    "pipeline_keep": scores[best].label == "entailment" and not missing,
                }
            )
    assert len(rows) == 36 and Counter(r["gold"] for r in rows) == dict.fromkeys(LABELS, 12)
    return rows, hashlib.sha256(cases_bytes).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recorded", type=Path, help="replay previously recorded control scores")
    parser.add_argument("--out", type=Path, default=HERE / "results.json")
    args = parser.parse_args()
    from notinspec.nli import RecordedNli

    model = (
        RecordedNli.load(args.recorded)
        if args.recorded
        else RecordingNli(TransformersNli(threads=4))
    )
    started = time.perf_counter()
    rows, case_hash = controls(model)
    results = {
        "schema_version": 1,
        "case_sha256": case_hash,
        "python": platform.python_version(),
        "model": model.model_id,
        "revision": model.revision,
        "grounding_version": GROUNDING_VERSION,
        "chunker_version": CHUNKER_VERSION,
        "windows_version": WINDOWS_VERSION,
        "decision": "argmax",
        "annotation": "AI-authored frozen controls; independent human review pending",
        "historical_human_benchmark": historical(),
        "controls": {
            "all": metrics(rows),
            "by_library": {
                s: metrics([r for r in rows if r["library"] == s])
                for s in sorted({r["library"] for r in rows})
            },
            "by_scope": {
                s: metrics([r for r in rows if r["scope"] == s]) for s in ("guide", "api")
            },
            "pipeline_false_drops": [
                r["id"] for r in rows if r["gold"] == "entailment" and not r["pipeline_keep"]
            ],
            "pipeline_false_keeps": [
                r["id"] for r in rows if r["gold"] != "entailment" and r["pipeline_keep"]
            ],
        },
        "rows": rows,
    }
    args.out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if isinstance(model, RecordingNli):
        model.save(args.out.with_name("scores.json"))
    print(
        json.dumps(
            {
                "elapsed_seconds": round(time.perf_counter() - started, 2),
                "historical": results["historical_human_benchmark"]["pipeline_keep_drop"],
                "controls": results["controls"]["all"],
                "false_drops": results["controls"]["pipeline_false_drops"],
                "false_keeps": results["controls"]["pipeline_false_keeps"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
