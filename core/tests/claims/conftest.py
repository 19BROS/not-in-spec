"""Shared inputs for the claim extractor tests.

The recordings in fixtures/ are real Groq answers, recorded with `RecordingProvider`
(`notinspec claims extract --record`) on 2026-11-17:

- `groq-fixturelib-guide.json`: the `guide` page of the Sphinx fixture project
  (`core/tests/fixtures/sphinx/xml-napoleon`, project `fixturelib`), 8 prose chunks, both
  default extractors. gpt-oss-20b is in it three times: without a completion limit (2 of 8
  chunks failed with `json_validate_failed`), with 8192 at Groq's default reasoning effort,
  and as the default extractor (8192, effort "low", recorded later the same day).
- `groq-urllib3-demo.json`: 3 chunks of the urllib3 demo pages (`Retry.sleep()`,
  `Timeout.read_timeout`, User Guide > Using Timeouts), same extractors and limits; gpt-oss-20b
  at the default effort and at "low".

Groq was the extractors' provider until 2026-11-21; those tests use `GROQ_EXTRACTORS`.
`fiit-urllib3-demo.json` has the default extractors on the FIIT proxy (thinking off, 16384
tokens), recorded on 2026-11-21: the same 3 urllib3 chunks plus `Utilities > Retry`, the
chunk Groq's qwen cut off at 2048 tokens (run 008, #42).
"""

import shutil
from pathlib import Path

import pytest

from notinspec.chunking import Chunk
from notinspec.config import load_config
from notinspec.ingestion import ingest

CORE = Path(__file__).parents[2]
FIXTURES = Path(__file__).parent / "fixtures"
GUIDE_RECORDING = FIXTURES / "groq-fixturelib-guide.json"
URLLIB3_RECORDING = FIXTURES / "groq-urllib3-demo.json"
URLLIB3_CHUNKS = ("567cff0c95e2e342", "0f1fe6bd0dcdec3d", "00fb7285ec99b133")
FIIT_RECORDING = FIXTURES / "fiit-urllib3-demo.json"
RETRY_CHUNK = "dab80b5788c33002"  # urllib3 > Utilities > Retry


@pytest.fixture
def fixture_project(tmp_path: Path) -> Path:
    """A config for the napoleon build of the Sphinx fixture project, in a temp folder."""
    shutil.copytree(CORE / "tests" / "fixtures" / "sphinx" / "xml-napoleon", tmp_path / "xml")
    config = tmp_path / "notinspec.yaml"
    config.write_text('project: "fixturelib"\ndocs:\n  sphinx_xml: "xml/"\n', encoding="utf-8")
    return config


@pytest.fixture
def guide_chunks(fixture_project: Path, tmp_path: Path) -> list[Chunk]:
    ingestion = ingest(load_config(fixture_project), output=tmp_path / "out")
    return [c for c in ingestion.chunks if c.source == "guide"]


@pytest.fixture(scope="session")
def urllib3_by_id(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Chunk]:
    config = load_config(CORE / "examples" / "sphinx" / "urllib3" / "notinspec.yaml")
    ingestion = ingest(config, output=tmp_path_factory.mktemp("urllib3"))
    return {c.id: c for c in ingestion.chunks}


@pytest.fixture(scope="session")
def urllib3_chunks(urllib3_by_id: dict[str, Chunk]) -> list[Chunk]:
    return [urllib3_by_id[i] for i in URLLIB3_CHUNKS]


@pytest.fixture(scope="session")
def fiit_chunks(urllib3_by_id: dict[str, Chunk]) -> list[Chunk]:
    """The chunks of the FIIT recording."""
    return [urllib3_by_id[i] for i in (*URLLIB3_CHUNKS, RETRY_CHUNK)]


# real NLI scores (notinspec.nli.TransformersNli, pinned revision) of every premise / claim pair
# the pipeline builds from the two recordings above: `guide` through `claims run --record-nli`,
# the urllib3 chunks through run_claims. Re-record after changing the extractor recordings or
# any grounding rule that changes a premise.
NLI_RECORDING = FIXTURES / "nli-claims.json"
