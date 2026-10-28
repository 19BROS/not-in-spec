from typing import Any

import pytest

from notinspec.runner import ChatRequest, Message


@pytest.fixture
def request_() -> ChatRequest:
    return ChatRequest(
        model="acme/model-a:free",
        messages=(Message("system", "Answer with JSON."), Message("user", "Create a charge.")),
    )


@pytest.fixture
def body() -> dict[str, Any]:
    """A chat-completions response body as OpenRouter returns it."""
    return {
        "id": "gen-1",
        "model": "acme/model-a-2026-09:free",
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": '{"method": "GET", "path": "/pets/1"}',
                    "refusal": None,
                },
            }
        ],
        "usage": {"prompt_tokens": 12, "completion_tokens": 9},
    }
