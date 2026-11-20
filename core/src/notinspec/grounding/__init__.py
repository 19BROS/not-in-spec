"""Deterministic grounding checks for claims (SPEC §6.4): no model, same input → same result.

- `check_citation`: is the claim's quoted span in the chunk (every match), and is it prose?
- `nli_premise`: the text around the citation that NLI reads (SPEC §6.1).
- `missing_identifiers` on `section_reference`: does the section name every identifier,
  number and version the claim names (SPEC §18)?

The NLI decision itself and the claim extractor live elsewhere (`notinspec.nli`,
`notinspec.claims`); this package only takes chunks, strings and the inventory.
"""

from notinspec.grounding.citation import (
    ChunkCitations,
    CitationCheck,
    CitationStatus,
    check_citation,
    normalize,
)
from notinspec.grounding.identifiers import (
    inventory_names,
    missing_identifiers,
    section_reference,
)
from notinspec.grounding.premise import PREMISE_RULE, ChunkPremises, Premise, nli_premise

# bump when any result can change for the same input (normalization, premise, identifier rules).
# Results also depend on chunking's sentence splitter (`prose_sentences`), so a claim stores
# WINDOWS_VERSION and CHUNKER_VERSION next to this one (`notinspec.claims.GroundingVersions`).
GROUNDING_VERSION = 2  # 2: hyphen variants, control characters, list marker after a colon, ...

__all__ = [
    "GROUNDING_VERSION",
    "PREMISE_RULE",
    "ChunkCitations",
    "ChunkPremises",
    "CitationCheck",
    "CitationStatus",
    "Premise",
    "check_citation",
    "inventory_names",
    "missing_identifiers",
    "nli_premise",
    "normalize",
    "section_reference",
]
