"""load_grounded_claims: claims.json (or a bare list of its rows) back as GroundedClaims."""

import json
from pathlib import Path

from notinspec.claims import load_grounded_claims
from notinspec.crosscheck.k5a import claim_ref

FIXTURE = Path(__file__).parents[1] / "crosscheck" / "fixtures" / "run009-claims.json"


def test_load_bare_rows() -> None:
    rows = json.loads(FIXTURE.read_text(encoding="utf-8"))
    claims = load_grounded_claims(FIXTURE)
    assert len(claims) == len(rows)
    first = rows[0]["claim"]
    assert claim_ref(claims[0]) == f"{first['chunk_id']}/{first['extractor']}/{first['local_id']}"
    assert claims[0].status == rows[0]["status"]


def test_load_cli_claims_json(tmp_path: Path) -> None:
    rows = json.loads(FIXTURE.read_text(encoding="utf-8"))
    path = tmp_path / "claims.json"
    path.write_text(json.dumps({"schema_version": 1, "claims": rows}), encoding="utf-8")
    assert load_grounded_claims(path) == load_grounded_claims(FIXTURE)
