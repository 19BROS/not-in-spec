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
- `fixtures/run009-k2-claims.json`: every grounded claim of 6 API descriptions, for K2:
  - `e1726e8f38d96ea4` Utilities > is_connection_dropped() (prose `HTTPConnection`, parameter
    entry `BaseHTTPConnection`: an error in the docs, issue #42);
  - `aa0b73129092fb4b` Utilities > Timeout > connect_timeout and `0f1fe6bd0dcdec3d`
    ... > read_timeout (annotation `float | None`, `Return type` with `int`);
  - `acea3ace92f50446` Utilities > Timeout > get_connect_duration();
  - `7a897b7b860d7108` Utilities > create_urllib3_context() (defaults `None` in the signature,
    the effective defaults in the prose);
  - `eefc47cfde210dc9` Utilities > ssl_wrap_socket() (two overloads).
- `fixtures/nli-k2-run009.json`: the real NLI scores (same model, revision and machine,
  2026-11-22) of every fact-claim pair K2 compares in those chunks, both directions, cut out
  of a recording of all 432 pairs of run 009. Re-record after changing the facts, their
  sentences, the prefilter or the claims.
"""

import json
from pathlib import Path
from typing import Any

import pytest

from notinspec.chunking import Chunk
from notinspec.claims import ExtractedClaim, GroundedClaim
from notinspec.config import load_config
from notinspec.ingestion import ingest
from notinspec.inventory import Inventory, build_inventory
from notinspec.nli import NliScores, RecordedNli

CORE = Path(__file__).parents[2]
FIXTURES = Path(__file__).parent / "fixtures"
RUN009_CLAIMS = FIXTURES / "run009-claims.json"
RUN009_NLI = FIXTURES / "nli-k5a-run009.json"
RUN009_K2_CLAIMS = FIXTURES / "run009-k2-claims.json"
RUN009_K2_NLI = FIXTURES / "nli-k2-run009.json"


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


@pytest.fixture(scope="session")
def run009_k2_claims() -> list[GroundedClaim]:
    rows = json.loads(RUN009_K2_CLAIMS.read_text(encoding="utf-8"))
    return [grounded_claim(r) for r in rows]


@pytest.fixture(scope="session")
def urllib3_inventory(urllib3_chunks: list[Chunk]) -> Inventory:
    return build_inventory(urllib3_chunks).inventory


@pytest.fixture
def run009_k2_nli() -> RecordedNli:
    return RecordedNli.load(RUN009_K2_NLI)
