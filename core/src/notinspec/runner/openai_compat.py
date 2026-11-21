"""OpenAI-compatible chat completions (Groq, OpenRouter), mapped onto the Provider contract."""

import os
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC
from email.utils import parsedate_to_datetime
from typing import Any, NoReturn

import httpx2

from notinspec.runner.provider import (
    ChatRequest,
    Completion,
    ModelUnavailable,
    ProviderError,
    QuotaExhausted,
    RateLimited,
    RequestTimeout,
    TransientError,
)
from notinspec.runner.ratelimit import Limiters, RateLimiter

# 498: Groq flex tier over capacity
_TRANSIENT_STATUS = frozenset({408, 498, 500, 502, 503, 504, 520, 522, 524, 529})
_GONE_CODES = frozenset({"model_not_found", "model_decommissioned"})
# OpenRouter says it only in the message; a bare 404 (wrong base URL) is a config error instead
# LiteLLM (FIIT proxy) says "Invalid model name passed in model=..." with HTTP 400, checked live
_GONE_MESSAGES = ("not a valid model", "no endpoints found", "invalid model name")
# Groq rejects a best-effort json_schema answer that fails the schema with HTTP 400 and this code
SCHEMA_FAILED = "json_validate_failed"


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str
    api_key_env: str
    # client-side budget; per model (Groq, SPEC §8) or one for the whole account (OpenRouter)
    per_minute: int
    per_day: int
    per_model_limits: bool
    # models known to accept response_format json_schema, for providers whose /models doesn't say
    structured_output_models: frozenset[str] = frozenset()
    default_model: str | None = None  # model under test when none is named
    headers: Mapping[str, str] = field(default_factory=dict)
    timeout: float = 120.0  # seconds per request
    # the only models this provider may be asked; None = any. A request for another model fails
    # before it is sent
    allowed_models: frozenset[str] | None = None

    def limiters(self) -> Limiters:
        """Fresh limiters, keyed the way this provider counts. Share one per API account."""
        return Limiters(
            lambda: RateLimiter(self.per_minute, self.per_day), per_model=self.per_model_limits
        )


GROQ = ProviderConfig(
    name="groq",
    base_url="https://api.groq.com/openai/v1",
    api_key_env="GROQ_API_KEY",
    # 1000/day measured from x-ratelimit-* headers (2026-11-17); 30/min from Groq's docs.
    # Groq also allows only 8000 tokens/min per model, which this limiter doesn't count.
    per_minute=30,
    per_day=1000,
    per_model_limits=True,
    # console.groq.com/docs/structured-outputs, read 2026-11-17; qwen confirmed live the same day,
    # `models --probe` checks the rest
    structured_output_models=frozenset(
        {
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
            "openai/gpt-oss-safeguard-20b",
            "qwen/qwen3.8-27b",
            "meta-models/muse-spark-open",
        }
    ),
    default_model="qwen/qwen3.8-27b",  # the only model under test for now (SPEC §8)
)

OPENROUTER = ProviderConfig(
    name="openrouter",
    base_url="https://openrouter.ai/api/v1",
    api_key_env="OPENROUTER_API_KEY",
    per_minute=20,
    per_day=50,
    per_model_limits=False,
    headers={"X-Title": "notinspec"},
)

# The faculty's LiteLLM proxy (fiit-ba.github.io/docs/litellm-quickstart, read 2026-11-21). One key
# for the whole team, with a budget the paid models (Claude, GPT, OpenRouter) draw from;
# `openrouter-free` may log prompts. The local models did not change the key's spend, so only
# they are allowed (SPEC §8). The proxy publishes no rate limits: the limiter is a guess. A
# request waited up to 85 s in the queue of the shared server, and a long reasoning answer ran
# past 10 minutes.
FIIT = ProviderConfig(
    name="fiit",
    base_url="https://litellm.blockfinlab.xyz/v1",
    api_key_env="FIIT_API_KEY",
    per_minute=20,
    per_day=5000,
    per_model_limits=True,
    # confirmed live 2026-11-21 (`Retry`, valid JSON from both)
    structured_output_models=frozenset({"qwen3.8-flash-next", "gemma4-26b-a4b-hpc"}),
    timeout=900.0,
    allowed_models=frozenset({"qwen3.8-flash-next", "gemma4-26b-a4b-hpc"}),
)

PROVIDERS = {c.name: c for c in (GROQ, OPENROUTER, FIIT)}


@dataclass(frozen=True)
class ModelInfo:
    id: str
    context_length: int | None
    structured_output: bool  # accepts response_format with a JSON schema


class OpenAICompatProvider:
    def __init__(
        self,
        config: ProviderConfig,
        api_key: str,
        *,
        timeout: float | None = None,
        transport: httpx2.BaseTransport | None = None,
    ) -> None:
        self.config = config
        self._http = httpx2.Client(
            base_url=config.base_url,
            timeout=config.timeout if timeout is None else timeout,
            transport=transport,
            headers={"Authorization": f"Bearer {api_key}", **config.headers},
        )

    @classmethod
    def from_env(cls, config: ProviderConfig = GROQ) -> "OpenAICompatProvider":
        api_key = os.environ.get(config.api_key_env, "").strip()
        if not api_key:
            raise ProviderError(f"{config.api_key_env} is not set")
        return cls(config, api_key)

    def complete(self, request: ChatRequest) -> Completion:
        allowed = self.config.allowed_models
        if allowed is not None and request.model not in allowed:
            # not served to us: the extractor stops instead of failing chunk by chunk
            raise ModelUnavailable(
                f"{self.config.name}: model {request.model!r} is not allowed here; allowed: "
                f"{', '.join(sorted(allowed))} (paid models share the team's budget, SPEC §8)"
            )
        body = self._send("POST", "/chat/completions", json=chat_payload(request))
        return parse_completion(body, request.model)

    def list_models(self) -> list[ModelInfo]:
        """Active models. OpenRouter reports structured-output support; for Groq the config does."""
        data = self._send("GET", "/models").get("data")
        models = []
        for item in data if isinstance(data, list) else []:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            if item.get("active") is False:
                continue
            context = item.get("context_length", item.get("context_window"))
            params = item.get("supported_parameters") or []
            models.append(
                ModelInfo(
                    item["id"],
                    context if isinstance(context, int) else None,
                    "structured_outputs" in params
                    or item["id"] in self.config.structured_output_models,
                )
            )
        return sorted(models, key=lambda m: m.id)

    def _send(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = self._http.request(method, url, **kwargs)
        except httpx2.ReadTimeout as e:
            raise RequestTimeout(f"no answer within {self.config.timeout:.0f}s: {e}") from e
        except httpx2.TimeoutException as e:
            raise TransientError(f"timeout: {e}") from e
        except httpx2.TransportError as e:
            raise TransientError(f"transport error: {e}") from e

        status = response.status_code
        try:
            body = response.json()
        except ValueError:
            body = None
        if not isinstance(body, dict):
            # e.g. an HTML 429 from a proxy in front of the API: its Retry-After still counts
            headers = {k.lower(): v for k, v in response.headers.items()}
            _raise_for(status if status >= 400 else 502, "response is not a JSON object", headers)
        error = body.get("error")
        if _schema_failed(error):
            return body  # the model answered, just not in the schema: a result, not a failure
        if status >= 400 or error:
            _raise_error(status, error, response.headers)
        return body


def chat_payload(request: ChatRequest) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": request.model,
        "messages": [{"role": m.role, "content": m.content} for m in request.messages],
        "temperature": request.temperature,
    }
    if request.max_tokens is not None:
        payload["max_tokens"] = request.max_tokens
    if request.reasoning_effort is not None:
        payload["reasoning_effort"] = request.reasoning_effort
    if request.thinking is not None:
        payload["chat_template_kwargs"] = {"enable_thinking": request.thinking}
    if request.response_schema is not None:
        # best effort, not strict: strict needs every property required, and the answer's aren't
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {"name": "answer", "schema": request.response_schema},
        }
    return payload


def parse_completion(body: dict[str, Any], requested_model: str) -> Completion:
    """Turn a chat-completions body into a Completion. Also used to replay recorded bodies.

    A Groq schema failure becomes a Completion with the model's own output as content, so the
    answer parser judges it like any other malformed answer.
    """
    error = body.get("error")
    if isinstance(error, dict) and _schema_failed(error):
        generation = error.get("failed_generation")
        return Completion(
            content=generation if isinstance(generation, str) else None,
            refusal=None,
            finish_reason=SCHEMA_FAILED,
            model=str(body.get("model") or requested_model),
            raw=body,
        )
    choices = body.get("choices")
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        raise TransientError("response has no choices")
    choice = choices[0]
    if error := choice.get("error"):
        _raise_error(502, error, {})
    message = choice.get("message")
    message = message if isinstance(message, dict) else {}
    content, refusal = message.get("content"), message.get("refusal")
    finish_reason = choice.get("finish_reason")
    return Completion(
        content=content if isinstance(content, str) else None,
        refusal=refusal if isinstance(refusal, str) and refusal else None,
        finish_reason=finish_reason if isinstance(finish_reason, str) else None,
        model=str(body.get("model") or requested_model),
        raw=body,
    )


def _schema_failed(error: object) -> bool:
    return isinstance(error, dict) and error.get("code") == SCHEMA_FAILED


def _raise_error(status: int, error: object, headers: Mapping[str, str]) -> NoReturn:
    """`error` is {message, type, code}. OpenRouter's code is the HTTP status, sometimes sent
    with HTTP 200; Groq's is a string such as `model_decommissioned`."""
    info = error if isinstance(error, dict) else {}
    code = info.get("code")
    if isinstance(code, int) and code >= 400:
        status = code
    elif status < 400:
        status = 502
    message = str(info.get("message") or error or "unknown error")
    if isinstance(code, str) and code in _GONE_CODES:
        raise ModelUnavailable(f"HTTP {status}: {message}")
    # LiteLLM, once the key's budget is spent: HTTP 400, type `budget_exceeded`. It blocks every
    # model of the key, the free ones too, so the run pauses
    if info.get("type") == "budget_exceeded" or "budget has been exceeded" in message.lower():
        raise QuotaExhausted(f"HTTP {status}: {message}")
    merged = {k.lower(): v for k, v in headers.items()}
    metadata = info.get("metadata")
    if isinstance(metadata, dict):
        if isinstance(metadata.get("headers"), dict):
            merged |= {str(k).lower(): str(v) for k, v in metadata["headers"].items()}
        # OpenRouter's "Provider returned error" alone hides who failed and why; the upstream says
        if upstream := metadata.get("raw"):
            message += f" ({metadata.get('provider_name') or 'upstream'}: {str(upstream)[:300]})"
    _raise_for(status, message, merged)


def _raise_for(status: int, message: str, headers: Mapping[str, str]) -> NoReturn:
    detail = f"HTTP {status}: {message}"
    if status == 429:
        raise RateLimited(detail, retry_after=_retry_after(headers))
    if any(m in message.lower() for m in _GONE_MESSAGES):
        raise ModelUnavailable(detail)
    if status in _TRANSIENT_STATUS:
        raise TransientError(detail)
    raise ProviderError(detail)


def _retry_after(headers: Mapping[str, str]) -> float | None:
    """Seconds to wait: `Retry-After` (seconds or an HTTP date; Groq sends it with every 429),
    else OpenRouter's `X-RateLimit-Reset` (epoch ms)."""
    if value := headers.get("retry-after"):
        try:
            return max(0.0, float(value))
        except ValueError:
            pass
        try:
            when = parsedate_to_datetime(value)
        except (TypeError, ValueError):
            pass
        else:
            when = when if when.tzinfo else when.replace(tzinfo=UTC)
            return max(0.0, when.timestamp() - time.time())
    if reset := headers.get("x-ratelimit-reset"):
        try:
            return max(0.0, float(reset) / 1000 - time.time())
        except ValueError:
            pass
    return None
