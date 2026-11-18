import json
import re
from pathlib import Path
from typing import Any

import pytest

from notinspec.cli import main
from notinspec.demo import build_demo_run, new_run_id

TRIO = Path(__file__).parents[1] / "examples" / "sphinx" / "trio" / "notinspec.yaml"
STEP_IDS = ["read", "inventory", "claims", "grounding", "tests", "models", "evaluate"]

INGESTION: dict[str, Any] = {
    "project": "lib",
    "input_hash": "ih",
    "config_hash": "ch",
    "sphinx": {"version": "9.1.0"},
    "files": [{"source": "xml/a.xml"}, {"source": "xml/b.xml"}],
    "chunks": [
        {"id": "k1", "section_id": "s1", "source": "guide", "tokens": 10, "breadcrumb": "lib > G"},
        {"id": "k2", "section_id": "s2", "source": "api", "tokens": 5, "breadcrumb": "lib > A"},
    ],
    "inventory": {
        "symbols": [
            {
                "path": "lib.f",
                "kind": "function",
                "sources": [{"section_id": "s2"}],
                "signatures": [{"parameters": [{"name": "x"}, {"name": "y"}]}],
            },
            {"path": "lib.C", "kind": "class", "sources": [], "signatures": []},
        ],
        "changes": [
            {"symbol": "lib.f", "kind": "deprecated", "version": "2.0", "parameter": None,
             "replacement": "lib.g"},
        ],
    },
    "warnings": ["w"],
}  # fmt: skip
RESULTS: dict[str, Any] = {
    "created_at": "2026-11-18T10:30:00+00:00",
    "commit": "a" * 40,
    "tool": {"version": "0.0.0"},
}


def _claim(chunk: str, local: str, status: str) -> dict[str, Any]:
    return {
        "claim": {"chunk_id": chunk, "extractor": "m1", "local_id": local, "type": "fact",
                  "text": "t", "citation": "c"},
        "status": status,
        "premise": "p" if status == "kept" else None,
        "nli": None,
        "missing": [],
    }  # fmt: skip


CLAIMS: dict[str, Any] = {
    "sources": ["guide"],
    "extractors": [{"name": "m1", "model": "provider/m1-v2"}],  # claims record name
    "counts": {"m1": {"kept": 1, "citation_not_found": 1}},
    "versions": {"grounding": 1},
    "claims": [_claim("k1", "c1", "kept"), _claim("k1", "c2", "citation_not_found")],
    "failures": [{"chunk_id": "k2", "extractor": "m1", "cause": "truncated"}],
}


def test_without_claims() -> None:
    run = build_demo_run(INGESTION, RESULTS, None, "rid")
    assert run["schema"] == "notinspec-demo-run" and run["schema_version"] == 0
    assert run["id"] == "rid" and run["project"] == "lib" and run["commit"] == "a" * 40
    assert run["docs"] == {"sphinx_version": "9.1.0", "input_hash": "ih", "config_hash": "ch"}
    assert run["counts"] == {
        "files": 2, "chunks": 2, "symbols": 2, "parameters": 2, "changes": 1, "warnings": 1,
        "claims": None, "claims_kept": None,
    }  # fmt: skip
    assert [s["id"] for s in run["steps"]] == STEP_IDS
    assert [s["status"] for s in run["steps"]] == ["done", "done", "skipped", "skipped"] + [
        "not_implemented"
    ] * 3
    assert run["claims"] is None
    assert run["documents"] == [
        {"source": "guide", "chunks": 1, "tokens": 10, "symbols": 0, "claims": 0,
         "claims_kept": 0},
        {"source": "api", "chunks": 1, "tokens": 5, "symbols": 1, "claims": 0, "claims_kept": 0},
    ]  # fmt: skip
    assert run["symbols"] == [
        {"path": "lib.f", "kind": "function", "source": "api", "parameters": ["x", "y"]},
        {"path": "lib.C", "kind": "class", "source": None, "parameters": []},
    ]
    assert run["changes"] == [
        {"symbol": "lib.f", "kind": "deprecated", "version": "2.0", "parameter": None,
         "replacement": "lib.g"},
    ]  # fmt: skip


def test_with_claims() -> None:
    run = build_demo_run(INGESTION, RESULTS, CLAIMS, "rid")
    assert run["counts"]["claims"] == 2 and run["counts"]["claims_kept"] == 1
    claims_step, grounding = run["steps"][2], run["steps"][3]
    assert claims_step["status"] == "done" and "1 chunks failed" in claims_step["detail"]
    assert grounding == {
        "id": "grounding", "label": "Ground claims (citation, NLI, identifiers)",
        "status": "done", "detail": "1 kept · 1 dropped",
    }  # fmt: skip
    assert run["documents"][0]["claims"] == 2 and run["documents"][0]["claims_kept"] == 1
    claims = run["claims"]
    assert claims["extractors"] == ["m1"] and claims["counts"] == CLAIMS["counts"]
    assert claims["items"][1] == {
        "id": "k1:m1:c2", "extractor": "m1", "source": "guide", "breadcrumb": "lib > G",
        "chunk_id": "k1", "type": "fact", "text": "t", "citation": "c",
        "status": "citation_not_found", "premise": None, "nli": None, "missing": [],
    }  # fmt: skip


def test_stopped_claims_step_failed() -> None:
    run = build_demo_run(INGESTION, RESULTS, CLAIMS, "rid", stopped=["m1: daily quota"])
    step = run["steps"][2]
    assert step["status"] == "failed"
    assert step["detail"] == "stopped: m1: daily quota; run again to continue"
    assert run["claims"]["items"]  # the claims so far are still shown


def test_run_id_shape() -> None:
    assert re.fullmatch(r"\d{8}T\d{4}Z-hydra-zen-[0-9a-f]{4}", new_run_id("hydra-zen"))
    api_id = re.compile(r"[A-Za-z0-9_.-]{1,100}")  # what the API accepts
    for project in ("a/b c", "Zürich-lib", "x" * 120):
        assert api_id.fullmatch(new_run_id(project)), project


def test_cli_demo_without_claims(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    runs = tmp_path / "runs"
    assert main(["demo", "--config", str(TRIO), "--runs-dir", str(runs), "--no-claims"]) == 0
    (folder,) = runs.iterdir()
    assert {p.name for p in folder.iterdir()} == {
        "ingestion.json", "results.json", "report.html", "comment.md", "run.json",
    }  # fmt: skip
    run = json.loads((folder / "run.json").read_bytes())
    assert run["id"] == folder.name and run["project"] == "trio"
    assert run["claims"] is None and run["counts"]["symbols"] > 0
    assert f"#/runs/{folder.name}" in capsys.readouterr().out
