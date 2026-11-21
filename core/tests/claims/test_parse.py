"""Parsing rules of the extractor's answer. Inputs are answer strings, not recordings."""

import json

from notinspec.claims import RawClaim, parse_claims


def _answer(*claims: dict[str, str]) -> str:
    return json.dumps({"claims": list(claims)})


C1 = {"id": "c1", "claim": "A  timeout is\nin seconds.", "citation": "in seconds", "type": "fact"}


def test_valid_answer() -> None:
    parsed = parse_claims(_answer(C1))
    assert parsed.cause is None
    assert parsed.claims == (RawClaim("c1", "A timeout is in seconds.", "in seconds", "fact"),)


def test_empty_list_is_a_valid_answer() -> None:
    parsed = parse_claims('{"claims": []}')
    assert parsed.cause is None and parsed.claims == ()


def test_one_fence_is_stripped() -> None:
    parsed = parse_claims(f"```json\n{_answer(C1)}\n```")
    assert parsed.cause is None and len(parsed.claims) == 1


def test_a_fence_with_crlf_line_endings_is_stripped() -> None:
    parsed = parse_claims(f"```json\r\n{_answer(C1)}\r\n```")
    assert parsed.cause is None and len(parsed.claims) == 1


def test_not_json_fails_the_chunk() -> None:
    assert parse_claims("Here are the claims: c1").cause == "malformed-output"
    assert parse_claims('{"items": []}').cause == "malformed-output"
    assert parse_claims("   ").cause == "malformed-output"


def test_cut_off_answer_is_truncated() -> None:
    assert parse_claims('{"claims": [{"id": "c1"', finish_reason="length").cause == "truncated"
    assert parse_claims(None, finish_reason="length").cause == "truncated"


def test_cut_off_answer_with_valid_json_is_truncated() -> None:
    # run 008: qwen stopped at 2048 completion tokens on `Retry`, and the JSON still parsed
    parsed = parse_claims(_answer(C1), finish_reason="length")
    assert parsed.cause == "truncated" and parsed.claims == ()
    assert parse_claims(_answer(C1), finish_reason="stop").cause is None


def test_refusal() -> None:
    parsed = parse_claims(None, refusal="I can't help with that.")
    assert parsed.cause == "refusal"
    assert "help" in parsed.detail


def test_groq_schema_failure() -> None:
    limit = "max completion tokens reached before generating a valid document"
    parsed = parse_claims(limit, finish_reason="json_validate_failed")
    assert parsed.cause == "truncated"
    assert parsed.detail.startswith("json_validate_failed: max completion")
    empty = parse_claims("", finish_reason="json_validate_failed")
    assert empty.cause == "malformed-output"
    assert empty.detail == "json_validate_failed: empty"


def test_invalid_claims_are_skipped_with_a_problem() -> None:
    parsed = parse_claims(
        _answer(
            C1,
            {"id": "c2", "claim": "", "citation": "x", "type": "fact"},
            {"id": "c3", "claim": "x", "citation": "x", "type": "opinion"},
            {**C1, "claim": "Another claim."},  # repeated id c1
            {"id": "c5", "claim": "Renamed.", "citation": "Renamed", "type": "CHANGE", "x": 1},
        )
    )
    assert parsed.cause is None
    assert [c.local_id for c in parsed.claims] == ["c1", "c5"]
    assert parsed.claims[1].type == "change"
    assert parsed.problems == (
        "claim 2: missing or empty `claim`",
        "claim 3: unknown type 'opinion'",
        "claim 4: repeated id 'c1'",
    )


def test_a_missing_id_is_the_claims_position() -> None:
    no_id = {k: v for k, v in C1.items() if k != "id"}
    parsed = parse_claims(_answer(C1, no_id, {**no_id, "id": "  "}, {**no_id, "id": 7}))
    assert parsed.problems == ()
    assert [c.local_id for c in parsed.claims] == ["c1", "#2", "#3", "#4"]


def test_a_claim_that_is_not_an_object() -> None:
    parsed = parse_claims('{"claims": ["c1"]}')
    assert parsed.claims == () and parsed.problems == ("claim 1: not an object",)


def test_citation_is_kept_as_returned() -> None:
    parsed = parse_claims(_answer({**C1, "citation": "  `timeout`  in\nseconds "}))
    assert parsed.claims[0].citation == "`timeout`  in\nseconds"
