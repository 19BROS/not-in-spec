"""Asking models: providers (Groq or another OpenAI-compatible API, recorded fake), rate limiting,
caching, retries."""

from notinspec.runner.client import CacheKey, MemoryCache, ModelClient, ResponseCache
from notinspec.runner.fake import FakeProvider, RecordingProvider
from notinspec.runner.openai_compat import (
    GROQ,
    OPENROUTER,
    PROVIDERS,
    ModelInfo,
    OpenAICompatProvider,
    ProviderConfig,
)
from notinspec.runner.provider import (
    ChatRequest,
    Completion,
    Message,
    ModelUnavailable,
    Provider,
    ProviderError,
    QuotaExhausted,
    RateLimited,
    TransientError,
)
from notinspec.runner.ratelimit import Limiters, RateLimiter

__all__ = [
    "GROQ",
    "OPENROUTER",
    "PROVIDERS",
    "CacheKey",
    "ChatRequest",
    "Completion",
    "FakeProvider",
    "Limiters",
    "MemoryCache",
    "Message",
    "ModelClient",
    "ModelInfo",
    "ModelUnavailable",
    "OpenAICompatProvider",
    "Provider",
    "ProviderConfig",
    "ProviderError",
    "QuotaExhausted",
    "RateLimited",
    "RateLimiter",
    "RecordingProvider",
    "ResponseCache",
    "TransientError",
]
