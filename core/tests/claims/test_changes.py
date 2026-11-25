"""*Change* claims → `Change` candidates. Sentences are from the real urllib3 changelog."""

from pathlib import Path

import pytest

from notinspec.chunking import Chunk, Document, chunk_document
from notinspec.claims import (
    ChangeCandidate,
    ExtractedClaim,
    GroundedClaim,
    changes_from_claims,
)
from notinspec.claims.pipeline import GroundingStatus
from notinspec.config import load_config
from notinspec.grounding import check_citation
from notinspec.ingestion import ingest
from notinspec.inventory import Change, Inventory, Parameter, Signature, Source, Symbol

SIGNATURE = Source("signature", "api")


def _symbol(path: str, *parameters: str) -> Symbol:
    params = tuple(
        Parameter(p, "keyword_only", False, (SIGNATURE,), default="None") for p in parameters
    )
    return Symbol(path, "class", (SIGNATURE,), (Signature(params, (SIGNATURE,)),))


INVENTORY = Inventory(
    (
        _symbol("acme.util.Retry", "total", "allowed_methods"),
        _symbol("acme.Pool", "maxsize"),
        _symbol("acme.Conn", "strict"),
        _symbol("acme.response.HTTPResponse"),
        _symbol("acme.request"),
        _symbol("acme.fields.format_header_param"),
        _symbol("acme.fields.format_multipart_header_param"),
        _symbol("acme.a.Twin"),
        _symbol("acme.b.Twin"),
    ),
    (Change("acme.fields.format_header_param", "deprecated", "2.0.0", (SIGNATURE,)),),
)


def _chunk(*items: str, heading: str = "2.0.0 (2023-04-26)") -> Chunk:
    body = "\n".join(f"- {i}" for i in items)
    text = f"# Changelog\n\n## {heading}\n\n### Removed\n\n{body}\n"
    chunks = chunk_document(Document("CHANGELOG.md", text), project="acme")
    return next(c for c in chunks if c.breadcrumb.endswith("Removed"))


def _claim(
    chunk: Chunk,
    text: str,
    citation: str,
    *,
    extractor: str = "one",
    local_id: str = "c1",
    type_: str = "change",
    status: GroundingStatus = "kept",
) -> GroundedClaim:
    span = check_citation(chunk, citation).span
    assert span is not None, citation
    extracted = ExtractedClaim(
        chunk.id,
        extractor,
        local_id,
        text,
        citation,
        type_,
        "run",
        "hash",
        "model",  # type: ignore[arg-type]
    )
    return GroundedClaim(extracted, 1, status, span, 1, 1, None, None, None, ())


def _one(chunk: Chunk, text: str, citation: str | None = None) -> ChangeCandidate:
    claim = _claim(chunk, text, citation or chunk.text.split("- ", 1)[1].strip())
    result = changes_from_claims([claim], [chunk], INVENTORY, "acme")
    assert not result.skipped
    assert len(result.candidates) == 1
    return result.candidates[0]


def _skip(chunk: Chunk, text: str) -> str:
    claim = _claim(chunk, text, chunk.text.split("- ", 1)[1].strip())
    result = changes_from_claims([claim], [chunk], INVENTORY, "acme")
    assert not result.candidates
    return result.skipped[0].reason


def test_a_removed_module_gets_the_version_of_its_heading() -> None:
    chunk = _chunk("Removed the deprecated `acme.contrib.ntlmpool` module (#2339).")
    candidate = _one(chunk, "acme 2.0.0 removed the acme.contrib.ntlmpool module.")
    assert candidate.change == Change(
        "acme.contrib.ntlmpool", "removed", "2.0.0", (Source("changelog", chunk.section_id),)
    )
    assert candidate.review == ("no-directive",)


def test_a_claim_about_one_listed_name_gives_only_that_name() -> None:
    chunk = _chunk("Removed deprecated `Retry` options `method_whitelist`, `DEFAULT_BLACKLIST`.")
    parameter = _one(chunk, "The Retry option method_whitelist was removed.").change
    assert (parameter.symbol, parameter.parameter) == ("acme.util.Retry", "method_whitelist")
    constant = _one(chunk, "The Retry option DEFAULT_BLACKLIST was removed.").change
    assert (constant.symbol, constant.parameter) == ("acme.util.Retry.DEFAULT_BLACKLIST", None)


def test_one_owner_that_still_has_the_name_does_not_lose_the_others() -> None:
    chunk = _chunk("Removed the `strict` parameter/attribute from `Pool`, `Conn` and `Missing`.")
    claim = _claim(chunk, "The strict parameter was removed.", chunk.text.split("- ", 1)[1].strip())
    result = changes_from_claims([claim], [chunk], INVENTORY, "acme")
    assert [(c.change.symbol, c.change.parameter) for c in result.candidates] == [
        ("acme.Pool", "strict")
    ]
    assert sorted(s.reason for s in result.skipped) == ["still-in-inventory", "unresolved-name"]


@pytest.mark.parametrize(
    ("sentence", "claim"),
    [
        (
            "Removed fallback on certificate `commonName` in `match_hostname()` function.",
            "Fallback on commonName was removed.",
        ),
        (
            "Removed support for Python with an `ssl` module compiled with LibreSSL.",
            "Support for the ssl module with LibreSSL was removed.",
        ),
        (
            "Removed default value of `None` for the `maxsize` parameter of `Pool`.",
            "The default value None of maxsize was removed.",
        ),
        ("Restore previously removed `Retry.total` method.", "Retry.total was restored."),
        ("`Retry.total` will be removed in acme v3.0.", "total will be removed."),
        ("Removed `Pool` and `Conn`.", "Something else was removed."),
    ],
)
def test_sentences_that_do_not_remove_a_name_give_nothing(sentence: str, claim: str) -> None:
    assert _skip(_chunk(sentence), claim) == "no-api-name"


def test_a_removed_name_that_still_exists_is_skipped() -> None:
    chunk = _chunk("Removed the `acme.request` module.")
    assert _skip(chunk, "The acme.request module was removed.") == "still-in-inventory"


@pytest.mark.parametrize(
    ("sentence", "claim", "reason"),
    [
        ("Removed `Unknown`.", "Unknown was removed.", "unresolved-name"),
        ("Removed `Twin`.", "Twin was removed.", "ambiguous-name"),
        (
            "Deprecated `ssl_version` option.",
            "ssl_version is deprecated.",
            "parameter-without-owner",
        ),
        ("Removed the `<4` in metadata.", "<4 was removed.", "unresolved-name"),
        ("Removed `Unknown.attr`.", "Unknown.attr was removed.", "unresolved-name"),
        ("Removed `Twin.attr`.", "Twin.attr was removed.", "ambiguous-name"),
    ],
)
def test_names_that_cannot_be_placed_are_skipped(sentence: str, claim: str, reason: str) -> None:
    assert _skip(_chunk(sentence), claim) == reason


def test_a_chunk_without_a_version_heading_is_skipped() -> None:
    chunk = _chunk("Removed `Retry`.", heading="Migration guide")
    assert _skip(chunk, "Retry was removed.") == "no-version-heading"


def test_a_re_export_resolves_to_the_inventory_path() -> None:
    chunk = _chunk("Removed `acme.HTTPResponse.from_httplib` (#2648).")
    change = _one(chunk, "acme.HTTPResponse.from_httplib was removed.").change
    assert change.symbol == "acme.response.HTTPResponse.from_httplib"


def test_a_dotted_parameter_names_its_owner() -> None:
    chunk = _chunk(
        "Deprecated `Retry.header_formatter` parameter which will be removed in acme v3.0."
    )
    change = _one(chunk, "The header_formatter parameter is deprecated.").change
    assert (change.symbol, change.parameter) == ("acme.util.Retry", "header_formatter")
    assert change.removal_planned == "3.0"


def test_a_call_names_its_owner_and_parameter() -> None:
    chunk = _chunk(
        "Deprecated `Retry(method_whitelist=...)` in favor of `Retry(allowed_methods=...)`."
    )
    candidate = _one(chunk, "method_whitelist is deprecated in favor of allowed_methods.")
    change = candidate.change
    assert (change.symbol, change.parameter) == ("acme.util.Retry", "method_whitelist")
    assert change.replacement == "allowed_methods"
    assert "replacement" not in candidate.review


def test_a_sentence_wrapped_over_two_lines_is_one_sentence() -> None:
    chunk = _chunk("Removed the deprecated\n  `acme.contrib.ntlmpool` module.")
    claim = _claim(chunk, "ntlmpool was removed.", "`acme.contrib.ntlmpool` module")
    result = changes_from_claims([claim], [chunk], INVENTORY, "acme")
    assert [c.change.symbol for c in result.candidates] == ["acme.contrib.ntlmpool"]


@pytest.mark.parametrize(
    ("old", "kind"),
    [("format_header_param", "deprecated"), ("old_header_param", "removed")],
)
def test_a_rename_is_deprecated_if_the_old_name_exists(old: str, kind: str) -> None:
    written = f"acme.fields.{old}"
    chunk = _chunk(f"Rename `{written}` to `format_multipart_header_param`.")
    change = _one(chunk, f"{old} was renamed.").change
    assert (change.symbol, change.kind) == (written, kind)
    assert change.replacement == "acme.fields.format_multipart_header_param"


def test_a_key_confirmed_by_a_directive_with_a_known_replacement_needs_no_review() -> None:
    chunk = _chunk("Deprecated `format_header_param` in favor of `format_multipart_header_param`.")
    assert _one(chunk, "format_header_param is deprecated.").review == ()


def test_a_replacement_outside_the_inventory_goes_to_review() -> None:
    chunk = _chunk("Deprecated `format_header_param` in favor of `format_new`.")
    assert _one(chunk, "format_header_param is deprecated.").review == ("replacement",)


def test_a_replacement_only_in_the_sentence_but_not_the_citation_goes_to_review() -> None:
    chunk = _chunk("Deprecated `format_header_param` in favor of `format_multipart_header_param`.")
    candidate = _one(
        chunk, "format_header_param is deprecated.", "Deprecated `format_header_param`"
    )
    assert candidate.review == ("replacement",)


def test_a_planned_removal_goes_to_review() -> None:
    chunk = _chunk("Deprecated `format_header_param` which will be removed in acme v2.1.0.")
    candidate = _one(chunk, "format_header_param is deprecated.")
    assert candidate.change.removal_planned == "2.1.0"
    assert candidate.review == ("removal-planned",)


def test_two_extractors_on_one_change_give_one_candidate() -> None:
    chunk = _chunk("Removed `acme.contrib.ntlmpool`.")
    citation = "Removed `acme.contrib.ntlmpool`"
    claims = [
        _claim(chunk, "ntlmpool was removed.", citation, extractor="two"),
        _claim(chunk, "ntlmpool is gone: acme.contrib.ntlmpool.", citation, extractor="one"),
    ]
    result = changes_from_claims(claims, [chunk], INVENTORY, "acme")
    assert len(result.candidates) == 1
    assert [r.extractor for r in result.candidates[0].claims] == ["one", "two"]
    assert changes_from_claims(reversed(claims), [chunk], INVENTORY, "acme") == result


def test_different_replacements_for_one_key_are_a_conflict() -> None:
    chunk = _chunk(
        "Deprecated `format_header_param` in favor of `format_multipart_header_param`.",
        "Deprecated `format_header_param` in favor of `format_new`.",
    )
    claims = [
        _claim(
            chunk,
            "format_header_param is deprecated.",
            "in favor of `format_multipart_header_param`",
        ),
        _claim(
            chunk, "format_header_param is deprecated.", "in favor of `format_new`", local_id="c2"
        ),
    ]
    result = changes_from_claims(claims, [chunk], INVENTORY, "acme")
    assert len(result.candidates) == 1
    assert [c.attribute for c in result.conflicts] == ["replacement"]


@pytest.mark.parametrize(
    ("type_", "status"),
    [("fact", "kept"), ("change", "nli_neutral"), ("change", "id_missing")],
)
def test_only_kept_change_claims_count(type_: str, status: GroundingStatus) -> None:
    chunk = _chunk("Removed `acme.contrib.ntlmpool`.")
    claim = _claim(
        chunk,
        "ntlmpool was removed.",
        "Removed `acme.contrib.ntlmpool`",
        type_=type_,
        status=status,
    )
    result = changes_from_claims([claim], [chunk], INVENTORY, "acme")
    assert not result.candidates
    assert not result.skipped


def test_real_urllib3_changelog(tmp_path: Path) -> None:
    config = Path(__file__).parents[2] / "examples/sphinx/urllib3/notinspec.yaml"
    ingestion = ingest(load_config(config), output=tmp_path)

    def run(version: str, sentence: str, text: str) -> tuple[list[Change], list[str]]:
        chunk = next(
            c
            for c in ingestion.chunks
            if c.source == "changelog" and version in c.breadcrumb and sentence in c.text
        )
        claim = _claim(chunk, text, sentence)
        result = changes_from_claims([claim], ingestion.chunks, ingestion.inventory, "urllib3")
        return [c.change for c in result.candidates], [s.reason for s in result.skipped]

    changes, _ = run(
        "2.0.0",
        "Removed deprecated `Retry` options `method_whitelist`",
        "The Retry option method_whitelist was removed.",
    )
    assert [(c.symbol, c.parameter, c.kind, c.version) for c in changes] == [
        ("urllib3.util.Retry", "method_whitelist", "removed", "2.0.0")
    ]
    changes, skipped = run(
        "2.0.0", "Removed the `urllib3.request` module", "The urllib3.request module was removed."
    )
    assert (changes, skipped) == ([], ["still-in-inventory"])
