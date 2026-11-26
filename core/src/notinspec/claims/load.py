"""Grounded claims back from `claims.json`, e.g. as the input of L2 items (`notinspec.tasks.l2`)."""

import json
from pathlib import Path
from typing import Any

from notinspec.claims.model import ExtractedClaim
from notinspec.claims.pipeline import GroundedClaim
from notinspec.nli import NliScores


def load_grounded_claims(path: Path) -> tuple[GroundedClaim, ...]:
    """Every claim of a `claims.json` (all statuses), or of a bare list of its claim rows."""
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data["claims"] if isinstance(data, dict) else data
    return tuple(grounded_claim(row) for row in rows)


def grounded_claim(row: dict[str, Any]) -> GroundedClaim:
    """One claim row of `claims.json` as a `GroundedClaim`."""
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
