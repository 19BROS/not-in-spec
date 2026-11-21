import json
import time
from collections.abc import Callable
from email.utils import formatdate
from typing import Any

import httpx2
import pytest

from notinspec.runner import (
    FIIT,
    GROQ,
    OPENROUTER,
    ChatRequest,
    ModelUnavailable,
    OpenAICompatProvider,
    ProviderConfig,
    ProviderError,
    QuotaExhausted,
    RateLimited,
    RequestTimeout,
    TransientError,
)
from notinspec.runner.openai_compat import SCHEMA_FAILED
from notinspec.verify import ANSWER_SCHEMA, parse_answer

type Handler = Callable[[httpx2.Request], httpx2.Response]


def provider(handler: Handler, config: ProviderConfig = GROQ) -> OpenAICompatProvider:
    return OpenAICompatProvider(config, "sk-test", transport=httpx2.MockTransport(handler))


def reply(status: int, body: Any, headers: dict[str, str] | None = None) -> Handler:
    return lambda _: httpx2.Response(status, json=body, headers=headers)


@pytest.mark.parametrize(
    ("config", "url"),
    [
        (GROQ, "https://api.groq.com/openai/v1/chat/completions"),
        (OPENROUTER, "https://openrouter.ai/api/v1/chat/completions"),
    ],
    ids=["groq", "openrouter"],
)
def test_sends_request_and_parses_answer(
    request_: ChatRequest, body: dict[str, Any], config: ProviderConfig, url: str
) -> None:
    sent: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.append(request)
        return httpx2.Response(200, json=body)

    schema_request = ChatRequest(request_.model, request_.messages, response_schema=ANSWER_SCHEMA)
    completion = provider(handler, config).complete(schema_request)

    assert str(sent[0].url) == url
    assert sent[0].headers["Authorization"] == "Bearer sk-test"
    assert ("X-Title" in sent[0].headers) == (config is OPENROUTER)
    payload = json.loads(sent[0].content)
    assert payload["model"] == "acme/model-a:free"
    assert payload["temperature"] == 0.0
    assert payload["messages"][1] == {"role": "user", "content": "Create a charge."}
    assert payload["response_format"]["json_schema"]["schema"] == ANSWER_SCHEMA
    assert "strict" not in payload["response_format"]["json_schema"]  # best effort
    assert "max_tokens" not in payload
    assert "reasoning_effort" not in payload
    assert "chat_template_kwargs" not in payload

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

    provider(handler).complete(
        ChatRequest(request_.model, request_.messages, max_tokens=50, reasoning_effort="low")
    )
    assert "response_format" not in sent[0]
    assert sent[0]["max_tokens"] == 50
    assert sent[0]["reasoning_effort"] == "low"


def test_thinking_off_is_sent_as_chat_template_kwargs(
    request_: ChatRequest, body: dict[str, Any]
) -> None:
    sent: list[dict[str, Any]] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.append(json.loads(request.content))
        return httpx2.Response(200, json=body)

    provider(handler).complete(ChatRequest(request_.model, request_.messages, thinking=False))
    assert sent[0]["chat_template_kwargs"] == {"enable_thinking": False}


def test_fiit_sends_only_the_free_models(request_: ChatRequest, body: dict[str, Any]) -> None:
    sent: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.append(request)
        return httpx2.Response(200, json=body)

    fiit = provider(handler, FIIT)
    for model in ("claude-haiku-5.5-fiit", "gpt-6-luna-fiit", "openrouter-free"):
        with pytest.raises(ModelUnavailable, match="not allowed"):
            fiit.complete(ChatRequest(model, request_.messages))
    assert sent == []  # refused before anything was sent
    fiit.complete(ChatRequest("qwen3.8-flash-next", request_.messages))
    assert str(sent[0].url) == "https://litellm.blockfinlab.xyz/v1/chat/completions"


def test_litellm_unknown_model_is_unavailable(request_: ChatRequest) -> None:
    # the FIIT proxy's answer for an alias it doesn't serve (checked live 2026-11-21)
    message = (
        "/chat/completions: Invalid model name passed in model=qwen3.7-does-not-exist. "
        "Call `/v1/models` to view available models for your key."
    )
    error = {"message": message, "type": "invalid_request_error", "param": None, "code": "400"}
    with pytest.raises(ModelUnavailable, match="Invalid model name"):
        provider(reply(400, {"error": error})).complete(request_)


def test_litellm_budget_exceeded_pauses_the_run(request_: ChatRequest) -> None:
    message = "Budget has been exceeded! Current cost: 100.2, Max budget: 100.0"
    error = {"message": message, "type": "budget_exceeded", "param": None, "code": "400"}
    with pytest.raises(QuotaExhausted, match="Budget has been exceeded"):
        provider(reply(400, {"error": error})).complete(request_)


def test_a_read_timeout_is_a_request_timeout(request_: ChatRequest) -> None:
    def slow(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ReadTimeout("read timed out", request=request)

    with pytest.raises(RequestTimeout, match="no answer within 120s"):
        provider(slow).complete(request_)


def test_the_timeout_comes_from_the_provider() -> None:
    assert OpenAICompatProvider(FIIT, "k")._http.timeout.read == 900.0
    assert OpenAICompatProvider(GROQ, "k")._http.timeout.read == 120.0
    assert OpenAICompatProvider(GROQ, "k", timeout=5)._http.timeout.read == 5


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
        provider(reply(429, error), OPENROUTER).complete(request_)
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
        (404, "Unknown request URL: POST /openai/v1/chat", ProviderError),
        (400, "messages is required", ProviderError),
        (413, "Request Entity Too Large", ProviderError),
        (498, "Flex Tier Capacity Exceeded", TransientError),
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
        provider(reply(429, error), OPENROUTER).complete(request_)
    assert str(exc.value) == (
        "HTTP 429: Provider returned error "
        "(Google AI Studio: google/gemma:free is temporarily rate-limited upstream)"
    )


def test_error_in_200_body(request_: ChatRequest) -> None:
    with pytest.raises(TransientError, match="HTTP 502: provider returned error"):
        error = reply(200, {"error": {"message": "provider returned error"}})
        provider(error, OPENROUTER).complete(request_)


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


def test_list_models_openrouter() -> None:
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
    listed = provider(reply(200, models), OPENROUTER).list_models()
    assert [(m.id, m.context_length, m.structured_output) for m in listed] == [
        ("a/model:free", 131072, True),
        ("b/model:free", 32768, False),
        ("c/model", None, False),
    ]


def test_list_models_groq() -> None:
    """Groq's /models says nothing about structured output; the config's list does."""

    def model(id_: str, active: bool = True) -> dict[str, Any]:
        return {
            "id": id_,
            "object": "model",
            "created": 1754000000,
            "owned_by": "x",
            "active": active,
            "context_window": 131072,
            "public_apps": None,
        }

    models = {
        "object": "list",
        "data": [
            model("llama-3.3-70b-versatile"),
            model("openai/gpt-oss-20b"),
            model("old/decommissioned", active=False),
        ],
    }
    listed = provider(reply(200, models)).list_models()
    assert [(m.id, m.context_length, m.structured_output) for m in listed] == [
        ("llama-3.3-70b-versatile", 131072, False),
        ("openai/gpt-oss-20b", 131072, True),
    ]


@pytest.mark.parametrize("code", ["model_not_found", "model_decommissioned"])
def test_groq_model_gone(request_: ChatRequest, code: str) -> None:
    error = {
        "error": {
            "message": f"The model `{request_.model}` has been decommissioned",
            "type": "invalid_request_error",
            "code": code,
        }
    }
    with pytest.raises(ModelUnavailable, match="HTTP 400"):
        provider(reply(400, error)).complete(request_)


def test_groq_429_with_retry_after(request_: ChatRequest) -> None:
    error = {
        "error": {
            "message": "Rate limit reached for model `openai/gpt-oss-20b` on requests per day",
            "type": "requests",
            "code": "rate_limit_exceeded",
        }
    }
    headers = {"retry-after": "2", "x-ratelimit-reset-requests": "2m59.56s"}
    with pytest.raises(RateLimited) as exc:
        provider(reply(429, error, headers)).complete(request_)
    assert exc.value.retry_after == 2.0


@pytest.mark.parametrize(
    ("generation", "cause"), [('{"method": "GET"}', "malformed-output"), (None, "malformed-output")]
)
def test_schema_failure_is_an_answer(
    request_: ChatRequest, generation: str | None, cause: str
) -> None:
    """Groq's 400 for an answer that fails a best-effort schema carries the model's output."""
    error: dict[str, Any] = {
        "message": "Generated JSON does not match the expected schema. Please adjust your prompt.",
        "type": "invalid_request_error",
        "code": SCHEMA_FAILED,
    }
    if generation is not None:
        error["failed_generation"] = generation
    body = {"error": error}

    completion = provider(reply(400, body)).complete(request_)

    assert completion.content == generation
    assert completion.finish_reason == SCHEMA_FAILED
    assert completion.model == request_.model
    assert completion.raw == body
    assert parse_answer(completion.content, refusal=completion.refusal).cause == cause


@pytest.mark.parametrize(
    ("config", "env"),
    [(GROQ, "GROQ_API_KEY"), (OPENROUTER, "OPENROUTER_API_KEY"), (FIIT, "FIIT_API_KEY")],
)
def test_from_env(monkeypatch: pytest.MonkeyPatch, config: ProviderConfig, env: str) -> None:
    monkeypatch.setenv(env, "sk-env")
    assert OpenAICompatProvider.from_env(config).config is config
    monkeypatch.setenv(env, " ")
    with pytest.raises(ProviderError, match=f"{env} is not set"):
        OpenAICompatProvider.from_env(config)


def test_from_env_defaults_to_groq(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "gsk-env")
    assert OpenAICompatProvider.from_env().config is GROQ


def test_config_limiters() -> None:
    groq, openrouter = GROQ.limiters(), OPENROUTER.limiters()
    assert groq.for_model("a") is not groq.for_model("b")  # Groq counts per model
    assert openrouter.for_model("a") is openrouter.for_model("b")  # OpenRouter per account
    limiter = groq.for_model("a")
    assert (limiter.per_minute, limiter.per_day) == (GROQ.per_minute, GROQ.per_day)


def test_non_json_429_keeps_retry_after(request_: ChatRequest) -> None:
    def handler(_: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(
            429, text="<html>Too Many Requests</html>", headers={"Retry-After": "30"}
        )

    with pytest.raises(RateLimited) as exc:
        provider(handler).complete(request_)
    assert exc.value.retry_after == 30.0


def test_retry_after_as_http_date(request_: ChatRequest) -> None:
    when = formatdate(time.time() + 120, usegmt=True)
    with pytest.raises(RateLimited) as exc:
        provider(reply(429, {"error": {"message": "slow down"}}, {"Retry-After": when})).complete(
            request_
        )
    assert exc.value.retry_after is not None and 100 < exc.value.retry_after <= 120


def test_bad_retry_after_falls_back_to_reset(request_: ChatRequest) -> None:
    reset_ms = str(int((time.time() + 60) * 1000))
    headers = {"Retry-After": "soon", "X-RateLimit-Reset": reset_ms}
    with pytest.raises(RateLimited) as exc:
        provider(reply(429, {"error": {"message": "slow down"}}, headers)).complete(request_)
    assert exc.value.retry_after is not None and 50 < exc.value.retry_after <= 60


@pytest.mark.parametrize("code", [{"type": "x"}, ["model_not_found"]], ids=["dict", "list"])
def test_odd_error_code_is_a_provider_error(request_: ChatRequest, code: object) -> None:
    with pytest.raises(ProviderError, match="HTTP 400: bad"):
        provider(reply(400, {"error": {"message": "bad", "code": code}})).complete(request_)
