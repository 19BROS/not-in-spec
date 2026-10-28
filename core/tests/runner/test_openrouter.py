import json
import time
from collections.abc import Callable
from typing import Any

import httpx2
import pytest

from notinspec.runner import (
    ChatRequest,
    ModelUnavailable,
    OpenRouterProvider,
    ProviderError,
    RateLimited,
    TransientError,
)
from notinspec.verify import ANSWER_SCHEMA

type Handler = Callable[[httpx2.Request], httpx2.Response]


def provider(handler: Handler) -> OpenRouterProvider:
    return OpenRouterProvider("sk-test", transport=httpx2.MockTransport(handler))


def reply(status: int, body: Any, headers: dict[str, str] | None = None) -> Handler:
    return lambda _: httpx2.Response(status, json=body, headers=headers)


def test_sends_request_and_parses_answer(request_: ChatRequest, body: dict[str, Any]) -> None:
    sent: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.append(request)
        return httpx2.Response(200, json=body)

    schema_request = ChatRequest(request_.model, request_.messages, response_schema=ANSWER_SCHEMA)
    completion = provider(handler).complete(schema_request)

    assert str(sent[0].url) == "https://openrouter.ai/api/v1/chat/completions"
    assert sent[0].headers["Authorization"] == "Bearer sk-test"
    payload = json.loads(sent[0].content)
    assert payload["model"] == "acme/model-a:free"
    assert payload["temperature"] == 0.0
    assert payload["messages"][1] == {"role": "user", "content": "Create a charge."}
    assert payload["response_format"]["json_schema"]["schema"] == ANSWER_SCHEMA
    assert "max_tokens" not in payload

    assert completion.content == '{"method": "GET", "path": "/pets/1"}'
    assert completion.refusal is None
    assert completion.finish_reason == "stop"
    assert completion.model == "acme/model-a-2026-09:free"  # exact ID that answered
    assert completion.raw == body


def test_no_schema_means_no_response_format(request_: ChatRequest, body: dict[str, Any]) -> None:
    sent: list[dict[str, Any]] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.append(json.loads(request.content))
        return httpx2.Response(200, json=body)

    provider(handler).complete(ChatRequest(request_.model, request_.messages, max_tokens=50))
    assert "response_format" not in sent[0]
    assert sent[0]["max_tokens"] == 50


def test_refusal_field(request_: ChatRequest, body: dict[str, Any]) -> None:
    body["choices"][0]["message"] = {"content": None, "refusal": "I can't help with that."}
    completion = provider(reply(200, body)).complete(request_)
    assert completion.content is None
    assert completion.refusal == "I can't help with that."


def test_429_with_retry_after(request_: ChatRequest) -> None:
    error = {"error": {"code": 429, "message": "Rate limit exceeded"}}
    with pytest.raises(RateLimited) as exc:
        provider(reply(429, error, {"Retry-After": "7"})).complete(request_)
    assert exc.value.retry_after == 7.0


def test_429_with_reset_in_error_metadata(request_: ChatRequest) -> None:
    reset_ms = str(int((time.time() + 3600) * 1000))
    error = {
        "error": {
            "code": 429,
            "message": "free-models-per-day",
            "metadata": {"headers": {"X-RateLimit-Reset": reset_ms}},
        }
    }
    with pytest.raises(RateLimited) as exc:
        provider(reply(429, error)).complete(request_)
    assert exc.value.retry_after is not None and 3500 < exc.value.retry_after <= 3600


def test_429_without_hint(request_: ChatRequest) -> None:
    with pytest.raises(RateLimited) as exc:
        provider(reply(429, {"error": {"message": "slow down"}})).complete(request_)
    assert exc.value.retry_after is None


@pytest.mark.parametrize(
    ("status", "message", "expected"),
    [
        (404, "No endpoints found for acme/gone:free", ModelUnavailable),
        (400, "acme/typo:free is not a valid model ID", ModelUnavailable),
        (502, "upstream error", TransientError),
        (503, "overloaded", TransientError),
        (401, "No auth credentials found", ProviderError),
        (402, "Insufficient credits", ProviderError),
        (400, "messages is required", ProviderError),
    ],
)
def test_error_status(
    request_: ChatRequest, status: int, message: str, expected: type[ProviderError]
) -> None:
    with pytest.raises(expected) as exc:
        provider(reply(status, {"error": {"code": status, "message": message}})).complete(request_)
    assert type(exc.value) is expected
    assert message in str(exc.value)


def test_upstream_error_names_provider(request_: ChatRequest) -> None:
    error = {
        "error": {
            "code": 429,
            "message": "Provider returned error",
            "metadata": {
                "provider_name": "Google AI Studio",
                "raw": "google/gemma:free is temporarily rate-limited upstream",
            },
        }
    }
    with pytest.raises(RateLimited) as exc:
        provider(reply(429, error)).complete(request_)
    assert str(exc.value) == (
        "HTTP 429: Provider returned error "
        "(Google AI Studio: google/gemma:free is temporarily rate-limited upstream)"
    )


def test_error_in_200_body(request_: ChatRequest) -> None:
    with pytest.raises(TransientError, match="HTTP 502: provider returned error"):
        provider(reply(200, {"error": {"message": "provider returned error"}})).complete(request_)


def test_error_inside_choice(request_: ChatRequest, body: dict[str, Any]) -> None:
    body["choices"][0]["error"] = {"code": 503, "message": "model overloaded"}
    with pytest.raises(TransientError, match="HTTP 503"):
        provider(reply(200, body)).complete(request_)


def test_no_choices_is_transient(request_: ChatRequest) -> None:
    with pytest.raises(TransientError, match="no choices"):
        provider(reply(200, {"id": "gen-1", "choices": []})).complete(request_)


def test_non_json_body(request_: ChatRequest) -> None:
    def handler(_: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(502, text="<html>Bad Gateway</html>")

    with pytest.raises(TransientError, match="not a JSON object"):
        provider(handler).complete(request_)


@pytest.mark.parametrize(
    "error", [httpx2.ConnectError("refused"), httpx2.ReadTimeout("slow")], ids=str
)
def test_network_errors_are_transient(request_: ChatRequest, error: Exception) -> None:
    def handler(_: httpx2.Request) -> httpx2.Response:
        raise error

    with pytest.raises(TransientError):
        provider(handler).complete(request_)


def test_list_models() -> None:
    models = {
        "data": [
            {"id": "b/model:free", "context_length": 32768, "supported_parameters": ["tools"]},
            {
                "id": "a/model:free",
                "context_length": 131072,
                "supported_parameters": ["response_format", "structured_outputs"],
            },
            {"id": "c/model", "context_length": None},
            {"name": "no id"},
        ]
    }
    listed = provider(reply(200, models)).list_models()
    assert [(m.id, m.context_length, m.structured_output) for m in listed] == [
        ("a/model:free", 131072, True),
        ("b/model:free", 32768, False),
        ("c/model", None, False),
    ]


def test_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-env")
    assert isinstance(OpenRouterProvider.from_env(), OpenRouterProvider)
    monkeypatch.setenv("OPENROUTER_API_KEY", " ")
    with pytest.raises(ProviderError, match="OPENROUTER_API_KEY is not set"):
        OpenRouterProvider.from_env()
