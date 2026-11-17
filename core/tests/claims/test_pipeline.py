"""ground_claims with a fake NLI classifier: statuses, the choice among repeated citations."""

from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path

from notinspec.chunking import Chunk, Document, chunk_blocks, chunk_document
from notinspec.claims import (
    ExtractedClaim,
    ExtractionResult,
    ExtractorSpec,
    GroundingVersions,
    ground_claims,
)
from notinspec.grounding import GROUNDING_VERSION, PREMISE_RULE
from notinspec.inventory import Inventory
from notinspec.nli import NliScores
from notinspec.sphinx import read_sphinx_xml

SPHINX = Path(__file__).parents[1] / "fixtures" / "sphinx" / "xml-napoleon"

SPEC = ExtractorSpec("x", "acme/model", prompt_version=1)
ENTAIL = NliScores(0.9, 0.05, 0.05)
NEUTRAL = NliScores(0.1, 0.8, 0.1)
CONTRA = NliScores(0.05, 0.05, 0.9)


class _FakeNli:
    """Entailment when every word of the claim is in the premise; `contradict` words flip it."""

    model_id = "fake/nli"
    revision = "0" * 40

    def __init__(self, contradict: frozenset[str] = frozenset()) -> None:
        self.contradict = contradict
        self.calls: list[Sequence[tuple[str, str]]] = []

    def score(self, pairs: Sequence[tuple[str, str]]) -> list[NliScores]:
        self.calls.append(pairs)
        out = []
        for premise, hypothesis in pairs:
            words = set(hypothesis.lower().rstrip(".").split())
            if words & self.contradict:
                out.append(CONTRA)
            elif words <= set(premise.lower().replace(".", " ").replace(":", " ").split()):
                out.append(ENTAIL)
            else:
                out.append(NEUTRAL)
        return out


def _chunk(text: str) -> Chunk:
    return chunk_document(Document("docs/a.md", text), project="acme")[0]


def _claim(chunk: Chunk, text: str, citation: str, local_id: str = "c1") -> ExtractedClaim:
    return ExtractedClaim(chunk.id, SPEC.name, local_id, text, citation, "fact", "r", "h", "m")


def _result(*claims: ExtractedClaim) -> ExtractionResult:
    return ExtractionResult(SPEC, claims, (), (), asked=1, reused=0, without_prose=0)


def test_every_status() -> None:
    chunk = _chunk(
        "# Retries\n\n"
        "Retries are counted per request. The default is 3 retries.\n\n"
        "```\nretries = 5\n```\n"
    )
    claims = (
        _claim(chunk, "Retries are counted per request.", "counted per request", "c1"),
        _claim(chunk, "Retries are counted per pool.", "counted per request", "c2"),
        _claim(chunk, "Retries are never counted.", "counted per request", "c3"),
        _claim(chunk, "The default is 3 retries.", "The default is 3 retries.", "c4"),
        _claim(chunk, "The default is 5 retries.", "The default is 3 retries.", "c5"),
        _claim(chunk, "Retries can be 5.", "retries = 5", "c6"),
        _claim(chunk, "Retries are free.", "free of charge", "c7"),
    )
    nli = _FakeNli(contradict=frozenset({"never"}))
    out = ground_claims([_result(*claims)], [chunk], Inventory(()), nli, project="acme")
    assert [c.status for c in out] == [
        "kept",
        "nli_neutral",
        "nli_contradiction",
        "kept",
        "nli_neutral",
        "not_checkable",
        "citation_not_found",
    ]
    kept = out[0]
    assert kept.premise == (
        "acme > Retries: Retries are counted per request. The default is 3 retries."
    )
    assert kept.nli == ENTAIL and kept.missing == () and kept.prompt_version == 1
    assert kept.citation_span is not None
    assert chunk.text[slice(*kept.citation_span)] == "counted per request"
    # the identifier check also runs when NLI already dropped the claim
    assert out[4].missing == ("5",)
    unchecked = out[5]
    assert (unchecked.premise, unchecked.nli, unchecked.premise_candidates) == (None, None, 0)
    # one NLI batch, every pair once
    assert len(nli.calls) == 1 and len(nli.calls[0]) == 5


def test_nli_keeps_it_but_an_identifier_is_missing() -> None:
    chunk = _chunk("# Pool\n\nThe pool keeps idle connections.\n")
    claim = _claim(chunk, "The pool keeps idle connections in `ConnectionCache`.", "keeps idle")

    class Always:
        model_id, revision = "fake/nli", "0" * 40

        def score(self, pairs: Sequence[tuple[str, str]]) -> list[NliScores]:
            return [ENTAIL] * len(pairs)

    (out,) = ground_claims([_result(claim)], [chunk], Inventory(()), Always(), project="acme")
    assert out.status == "id_missing" and out.missing == ("ConnectionCache",)


def _connect_chunk() -> Chunk:
    """connect() of the Sphinx fixture project, with `timeout` described like `host`."""
    xml = read_sphinx_xml(SPHINX)
    chunk = next(
        c
        for d in xml.documents
        for c in chunk_blocks(d, project="fixturelib")
        if c.breadcrumb.endswith("> connect()")
    )
    # same lines, so the blocks still fit: a docstring that repeats a sentence
    return replace(
        chunk, text=chunk.text.replace("Seconds to wait; `None` waits forever.", "Server name.")
    )


def test_a_repeated_citation_prefers_the_parameter_the_claim_names() -> None:
    chunk = _connect_chunk()
    claim = _claim(chunk, "The timeout parameter of connect() is a server name.", "Server name.")
    nli = _FakeNli()
    (out,) = ground_claims([_result(claim)], [chunk], Inventory(()), nli, project="fixturelib")
    assert out.citation_matches == 2 and out.premise_candidates == 1
    assert out.premise is not None
    assert out.premise.startswith("fixturelib > API Reference > connect() > timeout: ")
    assert len(nli.calls[0]) == 1


def test_a_repeated_citation_without_a_named_parameter_goes_to_nli() -> None:
    chunk = _connect_chunk()
    claim = _claim(chunk, "connect() takes a server name.", "Server name.")
    nli = _FakeNli()
    (out,) = ground_claims([_result(claim)], [chunk], Inventory(()), nli, project="fixturelib")
    assert out.citation_matches == 2 and out.premise_candidates == 2
    # equal scores: the earlier match wins
    assert out.premise is not None
    assert out.premise.startswith("fixturelib > API Reference > connect() > host: ")

    class PreferTimeout(_FakeNli):
        def score(self, pairs: Sequence[tuple[str, str]]) -> list[NliScores]:
            return [ENTAIL if "> timeout:" in p else NEUTRAL for p, _ in pairs]

    (out,) = ground_claims(
        [_result(claim)], [chunk], Inventory(()), PreferTimeout(), project="fixturelib"
    )
    assert out.premise is not None and "> timeout:" in out.premise
    assert out.status == "kept"


def test_versions_name_everything_a_decision_depends_on() -> None:
    versions = GroundingVersions.of(_FakeNli())
    assert versions.grounding == GROUNDING_VERSION
    assert versions.premise_rule == PREMISE_RULE
    assert (versions.nli_model, versions.decision_rule) == ("fake/nli", "argmax")


def test_no_claims_no_nli_call() -> None:
    nli = _FakeNli()
    assert ground_claims([_result()], [], Inventory(()), nli, project="acme") == ()
    assert nli.calls == []
