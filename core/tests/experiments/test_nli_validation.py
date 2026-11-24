"""Regression checks for the experiment's production adapter and reported metrics."""

import json
import runpy
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from notinspec.chunking import chunk_blocks
from notinspec.inventory import Inventory
from notinspec.nli import NliScores, RecordingNli
from notinspec.sphinx import read_sphinx_xml

ROOT = Path(__file__).parents[3]
SCRIPT = ROOT / "experiments/nli/validation/run.py"
experiment = runpy.run_path(str(SCRIPT))


class FakeNli:
    model_id = "fake/nli"
    revision = "0" * 40

    def __init__(self):
        self.pairs = []

    def score(self, pairs):
        self.pairs.extend(pairs)
        return [
            NliScores(0.01, 0.01, 0.98) if "> timeout:" in p else NliScores(0.98, 0.01, 0.01)
            for p, _ in pairs
        ]


def test_named_parameter_and_pair_dedup_are_decided_by_core():
    xml = read_sphinx_xml(ROOT / "core/tests/fixtures/sphinx/xml-napoleon")
    chunk = next(
        c
        for d in xml.documents
        for c in chunk_blocks(d, project="fixturelib")
        if c.breadcrumb.endswith("> connect()")
    )
    chunk = replace(
        chunk, text=chunk.text.replace("Seconds to wait; `None` waits forever.", "Server name.")
    )
    data = SimpleNamespace(
        chunks=(chunk,), inventory=Inventory(()), project="fixturelib", input_hash="fixture"
    )
    hypothesis = "The timeout parameter of connect() is a server name."
    case = dict(
        library="fixturelib",
        chunk_id=chunk.id,
        scope="api",
        citation="Server name.",
        claims=[["contradiction", hypothesis], ["contradiction", hypothesis]],
    )
    model = FakeNli()
    rows = experiment["ground_case"](case, data, model, 1)
    assert len(model.pairs) == 1
    assert "> timeout:" in model.pairs[0][0]
    assert all(r["citation_matches"] == 2 and r["premise_candidates"] == 1 for r in rows)
    assert all(r["status"] == "nli_contradiction" and not r["pipeline_keep"] for r in rows)
    case["chunk_id"] = "missing-id"
    with pytest.raises(ValueError, match="case 7: chunk missing-id not found in fixturelib"):
        experiment["ground_case"](case, data, model, 7)


def test_pipeline_false_drop_is_not_hidden_by_nli_entailment():
    result = experiment["metrics"](
        [{"gold": "entailment", "label": "entailment", "pipeline_keep": False}]
    )
    assert result["correct_three_way"] == 1
    assert result["keep_drop"]["false_drop"] == 1
    assert result["keep_drop"]["true_keep"] == 0
    assert result["keep_recall"] == 0


def test_missing_control_is_an_explicit_error():
    cases = json.loads((SCRIPT.parent / "cases.json").read_bytes())
    cases[0]["claims"].pop()
    with pytest.raises(ValueError, match="35 claims"):
        experiment["validate_cases"](cases)


def test_live_recording_replaces_obsolete_pairs(tmp_path):
    target = tmp_path / "scores.json"
    old = RecordingNli(FakeNli())
    old.score([("old premise", "old claim")])
    old.save(target)
    current = RecordingNli(FakeNli())
    current.score([("current premise", "current claim")])
    experiment["save_scores"](current, target)
    entries = json.loads(target.read_bytes())
    assert [(r["premise"], r["hypothesis"]) for r in entries] == [
        ("current premise", "current claim")
    ]
    assert list(tmp_path.iterdir()) == [target]


def test_readme_replay_creates_a_fresh_output_parent_and_records_provenance(tmp_path):
    out = tmp_path / "new" / "nested" / "results.json"
    result = subprocess.run(
        [
            sys.executable,
            "-O",
            str(SCRIPT),
            "--recorded",
            str(SCRIPT.parent / "scores.json"),
            "--out",
            str(out),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    doc = json.loads(out.read_bytes())
    assert doc["controls"]["all"]["keep_drop"] == {
        "true_keep": 12,
        "false_keep": 1,
        "false_drop": 0,
        "true_drop": 23,
    }
    old = doc["historical_human_benchmark"]["provenance"]
    assert old["premise_rule"] == "local-block" and old["window_size"] == 128
    assert old["grounding_version"] is None and Path(ROOT / old["predictions_file"]).is_file()
    assert doc["control_grounding"]["grounding"] >= 2
