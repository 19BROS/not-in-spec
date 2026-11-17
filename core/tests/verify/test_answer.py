import json

import pytest

from notinspec.verify import (
    ANSWER_SCHEMA,
    FailureCause,
    ParsedAnswer,
    ProposedRequest,
    parse_answer,
)

CHARGE = {
    "method": "POST",
    "path": "/v1/charges",
    "query": {},
    "headers": {"Authorization": "Bearer <API_KEY>"},
    "body": {"amount": 1000, "currency": "eur", "customer": "cus_123"},
}


def malformed(answer: ParsedAnswer) -> str:
    assert answer.request is None
    assert answer.cause is FailureCause.MALFORMED_OUTPUT
    return answer.detail


def test_parses_full_request() -> None:
    answer = parse_answer(json.dumps(CHARGE))
    assert answer == ParsedAnswer(
        ProposedRequest(
            method="POST",
            path="/v1/charges",
            headers={"Authorization": "Bearer <API_KEY>"},
            body={"amount": 1000, "currency": "eur", "customer": "cus_123"},
        )
    )


def test_optional_fields_default_to_empty() -> None:
    answer = parse_answer('{"method": "GET", "path": "/pets/1"}')
    assert answer.request == ProposedRequest("GET", "/pets/1")
    assert answer.cause is None


def test_null_query_and_headers_mean_empty() -> None:
    answer = parse_answer('{"method": "GET", "path": "/pets", "query": null, "headers": null}')
    assert answer.request == ProposedRequest("GET", "/pets")


def test_method_is_upper_cased() -> None:
    answer = parse_answer('{"method": "post", "path": "/pets"}')
    assert answer.request is not None and answer.request.method == "POST"


def test_query_accepts_scalars_and_lists() -> None:
    query = {"limit": 3, "expand": ["customer", "invoice"], "live": True, "q": "x"}
    answer = parse_answer(json.dumps({"method": "GET", "path": "/v1/charges", "query": query}))
    assert answer.request is not None and answer.request.query == query


@pytest.mark.parametrize("fence", ["```json\n{}\n```", "```\n{}\n```", "```JSON  \n{}```"])
def test_strips_one_surrounding_code_fence(fence: str) -> None:
    answer = parse_answer(fence.replace("{}", json.dumps(CHARGE)))
    assert answer.request is not None and answer.request.path == "/v1/charges"


def test_json_inside_prose_is_malformed() -> None:
    assert malformed(parse_answer(f"Sure! Here it is:\n{json.dumps(CHARGE)}")).startswith(
        "not JSON"
    )


@pytest.mark.parametrize(
    ("content", "detail"),
    [
        (None, "empty response"),
        ("   ", "empty response"),
        ("{not json", "not JSON"),
        ('{"method": "GET", "path": "/x", "query": {"n": NaN}}', "not JSON: NaN"),
        ("[1, 2]", "expected a JSON object, got array"),
        ('"GET /pets"', "expected a JSON object, got string"),
        ('{"method": "GET", "path": "/x", "url": "/x"}', "unknown field(s): url"),
        ('{"path": "/x"}', "method must be one of"),
        ('{"method": "FETCH", "path": "/x"}', "method must be one of"),
        ('{"method": 1, "path": "/x"}', "method must be one of"),
        ('{"method": "GET"}', "path must be a string"),
        ('{"method": "GET", "path": "https://api.example.com/x"}', "path must be a string"),
        ('{"method": "GET", "path": "/x", "query": []}', "query must be an object, got array"),
        ('{"method": "GET", "path": "/x", "query": {"a": {"b": 1}}}', "query.a must be"),
        ('{"method": "GET", "path": "/x", "query": {"a": [null]}}', "query.a must be"),
        ('{"method": "GET", "path": "/x", "headers": "k: v"}', "headers must be an object"),
        ('{"method": "GET", "path": "/x", "headers": {"X-N": 1}}', "headers.X-N must be a string"),
    ],
)
def test_malformed(content: str | None, detail: str) -> None:
    assert malformed(parse_answer(content)).startswith(detail)


@pytest.mark.parametrize(
    "content",
    [
        "I'm sorry, but I can't help with that.",
        "I cannot provide this request.",
        "I don’t know which endpoint the Acme API uses.",
        "As an AI, I am unable to access the Acme documentation.",
    ],
)
def test_refusal_without_json(content: str) -> None:
    answer = parse_answer(content)
    assert answer.request is None
    assert answer.cause is FailureCause.REFUSAL
    assert answer.detail == content


def test_provider_refusal_field_wins() -> None:
    answer = parse_answer(json.dumps(CHARGE), refusal="content policy")
    assert answer == ParsedAnswer(None, FailureCause.REFUSAL, "content policy")


def test_unrecognised_prose_is_malformed_not_refusal() -> None:
    assert malformed(parse_answer("Sorry, no idea.")).startswith("not JSON")


def test_schema_matches_parser_fields() -> None:
    assert set(ANSWER_SCHEMA["properties"]) == {"method", "path", "query", "headers", "body"}
    assert ANSWER_SCHEMA["required"] == ["method", "path"]
    json.dumps(ANSWER_SCHEMA)  # serializable, so it can be sent as response_format
