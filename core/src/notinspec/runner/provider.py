"""What the runner asks a model, what comes back, and how a provider fails."""

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Literal, Protocol

type Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class Message:
    role: Role
    content: str


@dataclass(frozen=True)
class ChatRequest:
    """Everything sent to the model. Recorded with every result (SPEC §3)."""

    model: str
    messages: tuple[Message, ...]
    temperature: float = 0.0
    max_tokens: int | None = None
    response_schema: dict[str, Any] | None = None  # JSON Schema for structured output

    def prompt_hash(self) -> str:
        """sha256 over the whole request, so any change to prompt or parameters is a new prompt."""
        canonical = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()


@dataclass(frozen=True)
class Completion:
    content: str | None
    refusal: str | None  # the provider's own refusal field, if it set one
    finish_reason: str | None
    model: str  # exact model ID that answered, as reported by the provider
    raw: dict[str, Any]  # the provider's full response body; stored as-is, append-only


class ProviderError(Exception):
    """No answer was obtained. Not retried unless a subclass says so."""


class TransientError(ProviderError):
    """Network failure, timeout or server error: safe to retry."""


class RateLimited(TransientError):
    def __init__(self, message: str, retry_after: float | None = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after  # seconds, if the provider said


class ModelUnavailable(ProviderError):
    """The model is gone or not served. A normal state shown on the leaderboard, not a crash."""


class QuotaExhausted(ProviderError):
    """The request budget is used up. The run pauses and resumes later (SPEC §2.8)."""


class Provider(Protocol):
    def complete(self, request: ChatRequest) -> Completion: ...
