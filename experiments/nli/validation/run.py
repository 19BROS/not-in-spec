"""SCRUM-46: recorded human benchmark and frozen controls on real Sphinx documents.

Run from the root with `uv run --all-packages --extra nli python
experiments/nli/validation/run.py`.
The 36 control labels were authored from the documentation before running NLI. They are
AI-authored controls, not independent human labels or an estimate of production precision.
This developer experiment can load the local model; project tests and CI do not invoke it.
"""

import argparse
import csv
import hashlib
import json
import os
import platform
import tempfile
import time
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from notinspec.claims import (
    ExtractedClaim,
    ExtractionResult,
    ExtractorSpec,
    GroundingVersions,
    ground_claims,
)
from notinspec.config import load_config
from notinspec.grounding import check_citation
from notinspec.ingestion import ingest
from notinspec.nli import RecordingNli, TransformersNli

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LABELS = ("entailment", "neutral", "contradiction")


def metrics(rows):
    matrix = {gold: {pred: 0 for pred in LABELS} for gold in LABELS}
    for row in rows:
        if row["label"] in LABELS:
            matrix[row["gold"]][row["label"]] += 1
    tp = sum(r["gold"] == "entailment" and r["pipeline_keep"] for r in rows)
    fp = sum(r["gold"] != "entailment" and r["pipeline_keep"] for r in rows)
    fn = sum(r["gold"] == "entailment" and not r["pipeline_keep"] for r in rows)
    tn = len(rows) - tp - fp - fn
    return {
        "count": len(rows),
        "nli_scored_count": sum(r["label"] in LABELS for r in rows),
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
        rows.append(
            {
                **item,
                "label": label,
                "status": prediction["status"],
                "pipeline_keep": label == "entailment",
            }
        )
    scored = [r for r in rows if r["label"] in LABELS]
    config_file = source.parent.parent / "config.json"
    config = json.loads(config_file.read_bytes())
    model_id = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
    return {
        "provenance": {
            "mode": "replay of stored run 007 predictions, not a new model run",
            "predictions_file": source.relative_to(ROOT).as_posix(),
            "predictions_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "labels_file": "experiments/nli/labels-human.csv",
            "labels_sha256": hashlib.sha256((base / "labels-human.csv").read_bytes()).hexdigest(),
            "config_file": config_file.relative_to(ROOT).as_posix(),
            "config_sha256": hashlib.sha256(config_file.read_bytes()).hexdigest(),
            "model": model_id,
            "revision": config["hub_sha"][model_id],
            "premise_rule": "local-block",
            "context": "breadcrumb",
            "window_size": 128,
            "radius": config["radius"],
            "decision": "argmax",
            "grounding_version": None,
            "chunker_version": None,
            "windows_version": None,
            "unrecorded_versions": "legacy experiment did not record core rule versions",
            "git": config["git"],
            "runtime_versions": config["versions"],
        },
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


def validate_cases(cases):
    labels = Counter(gold for case in cases for gold, _ in case["claims"])
    count = sum(labels.values())
    if len(cases) != 12 or count != 36 or labels != dict.fromkeys(LABELS, 12):
        raise ValueError(
            f"expected 12 cases / 36 claims / 12 per label; got {len(cases)} cases, "
            f"{count} claims, labels {dict(labels)}"
        )


def ground_case(case, data, model, index, offset=0):
    library = case["library"]
    chunk = next((c for c in data.chunks if c.id == case["chunk_id"]), None)
    if chunk is None:
        raise ValueError(f"case {index}: chunk {case['chunk_id']} not found in {library}")
    match = check_citation(chunk, case["citation"])
    if match.status != "found":
        raise ValueError(f"case {index}: citation {match.status} in {library}/{chunk.id}")
    spec = ExtractorSpec("frozen-controls", "authored-controls")
    claims = tuple(
        ExtractedClaim(
            chunk.id,
            spec.name,
            f"control-{offset + i + 1:03}",
            hypothesis,
            case["citation"],
            "fact",
            "frozen-controls",
            "not-an-llm-call",
            spec.model,
        )
        for i, (_, hypothesis) in enumerate(case["claims"])
    )
    result = ExtractionResult(spec, claims, (), (), 0, 0, 0)
    grounded = ground_claims([result], data.chunks, data.inventory, model, project=data.project)
    return [
        {
            "id": item.claim.local_id,
            "library": library,
            "scope": case["scope"],
            "chunk_id": chunk.id,
            "source": chunk.source,
            "breadcrumb": chunk.breadcrumb,
            "input_hash": data.input_hash,
            "content_hash": chunk.content_hash,
            "citation": case["citation"],
            "gold": gold,
            "hypothesis": item.claim.text,
            "status": item.status,
            "citation_matches": item.citation_matches,
            "premise_candidates": item.premise_candidates,
            "premise": item.premise,
            "scores": asdict(item.nli) if item.nli is not None else None,
            "label": item.nli.label if item.nli is not None else None,
            "missing_identifiers": item.missing,
            "pipeline_keep": item.status == "kept",
        }
        for (gold, _), item in zip(case["claims"], grounded, strict=True)
    ]


def controls(model):
    cases_bytes = (HERE / "cases.json").read_bytes()
    cases = json.loads(cases_bytes)
    validate_cases(cases)
    libraries = {}
    rows = []
    for index, case in enumerate(cases, 1):
        library = case["library"]
        if library not in libraries:
            config = load_config(ROOT / "core/examples/sphinx" / library / "notinspec.yaml")
            libraries[library] = ingest(config, output=ROOT / "tmp/nli-validation")
        rows.extend(ground_case(case, libraries[library], model, index, len(rows)))
    return rows, hashlib.sha256(cases_bytes).hexdigest()


def save_scores(model, path):
    """Publish only this run's pairs; RecordingNli.save otherwise merges old entries."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="nli-scores-", dir=path.parent) as temporary:
        fresh = Path(temporary) / "scores.json"
        model.save(fresh)
        os.replace(fresh, path)


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
        "schema_version": 2,
        "case_sha256": case_hash,
        "python": platform.python_version(),
        "model": model.model_id,
        "revision": model.revision,
        "control_grounding": asdict(GroundingVersions.of(model)),
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
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if isinstance(model, RecordingNli):
        save_scores(model, args.out.with_name("scores.json"))
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
