"""End to end: the CLI on the real Sphinx 9 XML of three libraries (core/examples/sphinx/)."""

import json
from pathlib import Path

import pytest

from notinspec.cli import main

EXAMPLES = Path(__file__).parents[1] / "examples" / "sphinx"


@pytest.mark.parametrize("library", ["urllib3", "trio", "hydra-zen"])
def test_sphinx_example_end_to_end(library: str, tmp_path: Path) -> None:
    config = str(EXAMPLES / library / "notinspec.yaml")
    first, second = tmp_path / "first", tmp_path / "second"
    assert main(["ci", "--config", config, "--out", str(first)]) == 0
    assert main(["ci", "--config", config, "--out", str(second)]) == 0
    raw = (first / "ingestion.json").read_bytes()
    assert raw == (second / "ingestion.json").read_bytes()

    data = json.loads(raw)
    assert data["project"] == library
    assert data["sphinx"]["version"].startswith("9.")
    assert {f["kind"] for f in data["files"]} == {"sphinx"}
    assert "xml/build-env.txt" in {f["source"] for f in data["files"]}
    assert not any("unknown node" in w for w in data["warnings"])
    xml = EXAMPLES / library / "xml"
    assert str(xml.resolve()) not in raw.decode("utf-8")

    # every document with text gives chunks
    sources = {c["source"] for c in data["chunks"]}
    docnames = {p.relative_to(xml).with_suffix("").as_posix() for p in xml.rglob("*.xml")}
    assert sources <= docnames
    assert len(sources) >= len(docnames) - 2  # only toctree-only pages may be empty
    report = (first / "report.html").read_text("utf-8")
    assert all(f"id='c-{c['id']}'" in report for c in data["chunks"])
    assert "<script" not in report
