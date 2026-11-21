"""Shared inputs for the cross-check tests.

Real data from `experiments/nli/runs/009-fiit-urllib3-demo` (`notinspec claims run` with the
FIIT extractors `qwen3.8-flash-next` and `gemma4-26b-a4b-hpc` on three urllib3 pages):

- `fixtures/run009-claims.json`: every grounded claim of 4 of its chunks, as `claims.json`
  writes them (all statuses, so K5a must skip the dropped ones):
  - `42766add097cdb07` v2 Migration Guide > Optimized for Python 3.10+ (CPython / PyPy);
  - `639d761e261bdd05` v2 Migration Guide > ... > Certificate verification via SSLContext;
  - `4b106715a267e6e4` User Guide > Making Requests (`PoolManager`, `urllib3.request()`);
  - `8b3528352f8e48e1` Utilities > parse_url() (RFC 3986 / RFC 6874).
- `fixtures/nli-k5a-run009.json`: the real NLI scores (`TransformersNli`, pinned revision, 2
  threads, 2026-11-21) of every claim pair K5a compares in those chunks, both directions. They
  were cut out of a recording of all 13 548 pairs of run 009 (`RecordingNli`). Re-record after
  changing the prefilter or the claims.
"""

import json
from pathlib import Path
from typing import Any

import pytest

from notinspec.chunking import Chunk
from notinspec.claims import ExtractedClaim, GroundedClaim
from notinspec.config import load_config
from notinspec.ingestion import ingest
from notinspec.nli import NliScores, RecordedNli

CORE = Path(__file__).parents[2]
FIXTURES = Path(__file__).parent / "fixtures"
RUN009_CLAIMS = FIXTURES / "run009-claims.json"
RUN009_NLI = FIXTURES / "nli-k5a-run009.json"


def grounded_claim(row: dict[str, Any]) -> GroundedClaim:
    """One claim of `claims.json` back as a `GroundedClaim`."""
    nli = row["nli"]
    return GroundedClaim(
        claim=ExtractedClaim(**row["claim"]),
        prompt_version=row["prompt_version"],
        status=row["status"],
        citation_span=_span(row["citation_span"]),
        citation_matches=row["citation_matches"],
        premise_candidates=row["premise_candidates"],
        premise=row["premise"],
        premise_span=_span(row["premise_span"]),
        nli=NliScores(**nli) if nli else None,
        missing=tuple(row["missing"]),
    )


def _span(value: list[int] | None) -> tuple[int, int] | None:
    return (value[0], value[1]) if value else None


@pytest.fixture(scope="session")
def run009_claims() -> list[GroundedClaim]:
    rows = json.loads(RUN009_CLAIMS.read_text(encoding="utf-8"))
    return [grounded_claim(r) for r in rows]


@pytest.fixture(scope="session")
def urllib3_chunks(tmp_path_factory: pytest.TempPathFactory) -> list[Chunk]:
    config = load_config(CORE / "examples" / "sphinx" / "urllib3" / "notinspec.yaml")
    return list(ingest(config, output=tmp_path_factory.mktemp("urllib3")).chunks)


@pytest.fixture
def run009_nli() -> RecordedNli:
    return RecordedNli.load(RUN009_NLI)
