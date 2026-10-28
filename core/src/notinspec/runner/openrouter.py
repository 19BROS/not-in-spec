"""OpenRouter chat completions (OpenAI-compatible API), mapped onto the Provider contract."""

import os
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, NoReturn

import httpx2

from notinspec.runner.provider import (
    ChatRequest,
    Completion,
    ModelUnavailable,
    ProviderError,
    RateLimited,
    TransientError,
)

BASE_URL = "https://openrouter.ai/api/v1"
_TRANSIENT_STATUS = frozenset({408, 500, 502, 503, 504, 520, 522, 524, 529})


@dataclass(frozen=True)
class ModelInfo:
    id: str
    context_length: int | None
    structured_output: bool  # accepts response_format with a JSON schema


class OpenRouterProvider:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        timeout: float = 120.0,
        transport: httpx2.BaseTransport | None = None,
    ) -> None:
        self._http = httpx2.Client(
            base_url=base_url,
            timeout=timeout,
            transport=transport,
            headers={"Authorization": f"Bearer {api_key}", "X-Title": "notinspec"},
        )

    @classmethod
    def from_env(cls) -> "OpenRouterProvider":
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            raise ProviderError("OPENROUTER_API_KEY is not set")
        return cls(api_key)

    def complete(self, request: ChatRequest) -> Completion:
        body = self._send("POST", "/chat/completions", json=chat_payload(request))
        return parse_completion(body, request.model)

    def list_models(self) -> list[ModelInfo]:
        data = self._send("GET", "/models").get("data")
        models = []
        for item in data if isinstance(data, list) else []:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            context = item.get("context_length")
            params = item.get("supported_parameters") or []
            models.append(
                ModelInfo(
                    item["id"],
                    context if isinstance(context, int) else None,
                    "structured_outputs" in params,
                )
            )
        return sorted(models, key=lambda m: m.id)

    def _send(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = self._http.request(method, url, **kwargs)
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
            _raise_for(status if status >= 400 else 502, "response is not a JSON object", {})
        error = body.get("error")
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
    if request.response_schema is not None:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {"name": "answer", "schema": request.response_schema},
        }
    return payload


def parse_completion(body: dict[str, Any], requested_model: str) -> Completion:
    """Turn a chat-completions body into a Completion. Also used to replay recorded bodies."""
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


def _raise_error(status: int, error: object, headers: Mapping[str, str]) -> NoReturn:
    """OpenRouter puts {code, message, metadata} in `error`, sometimes with HTTP 200."""
    info = error if isinstance(error, dict) else {}
    code = info.get("code")
    if isinstance(code, int) and code >= 400:
        status = code
    elif status < 400:
        status = 502
    message = str(info.get("message") or error or "unknown error")
    merged = {k.lower(): v for k, v in headers.items()}
    metadata = info.get("metadata")
    if isinstance(metadata, dict):
        if isinstance(metadata.get("headers"), dict):
            merged |= {str(k).lower(): str(v) for k, v in metadata["headers"].items()}
        # "Provider returned error" alone hides who failed and why; the upstream says
        if upstream := metadata.get("raw"):
            message += f" ({metadata.get('provider_name') or 'upstream'}: {str(upstream)[:300]})"
    _raise_for(status, message, merged)


def _raise_for(status: int, message: str, headers: Mapping[str, str]) -> NoReturn:
    detail = f"HTTP {status}: {message}"
    if status == 429:
        raise RateLimited(detail, retry_after=_retry_after(headers))
    if status == 404 or "not a valid model" in message.lower():
        raise ModelUnavailable(detail)
    if status in _TRANSIENT_STATUS:
        raise TransientError(detail)
    raise ProviderError(detail)


def _retry_after(headers: Mapping[str, str]) -> float | None:
    """Seconds to wait: `Retry-After`, else OpenRouter's `X-RateLimit-Reset` (epoch ms)."""
    try:
        if value := headers.get("retry-after"):
            return max(0.0, float(value))
        if reset := headers.get("x-ratelimit-reset"):
            return max(0.0, float(reset) / 1000 - time.time())
    except ValueError:
        pass
    return None
