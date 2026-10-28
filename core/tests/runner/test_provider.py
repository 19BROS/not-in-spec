from dataclasses import replace

from notinspec.runner import ChatRequest, Message
from notinspec.verify import ANSWER_SCHEMA


def test_prompt_hash_is_stable(request_: ChatRequest) -> None:
    same = ChatRequest(
        model="acme/model-a:free",
        messages=(Message("system", "Answer with JSON."), Message("user", "Create a charge.")),
    )
    assert request_.prompt_hash() == same.prompt_hash()
    assert len(request_.prompt_hash()) == 64


def test_prompt_hash_covers_everything_sent(request_: ChatRequest) -> None:
    variants = [
        replace(request_, model="acme/model-b:free"),
        replace(request_, messages=request_.messages[:1]),
        replace(request_, temperature=0.7),
        replace(request_, max_tokens=100),
        replace(request_, response_schema=ANSWER_SCHEMA),
    ]
    hashes = {request_.prompt_hash(), *(v.prompt_hash() for v in variants)}
    assert len(hashes) == len(variants) + 1
