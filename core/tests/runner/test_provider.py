from dataclasses import fields, replace

from notinspec.runner import ChatRequest, Message
from notinspec.runner.provider import _HASHED_ALWAYS
from notinspec.verify import ANSWER_SCHEMA

OLD_HASH = "ca2999651cca272ccb1f4baa0c92380e8322f70f37e488250c9d813d3531aae4"


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
        replace(request_, reasoning_effort="low"),
        replace(request_, thinking=False),
    ]
    hashes = {request_.prompt_hash(), *(v.prompt_hash() for v in variants)}
    assert len(hashes) == len(variants) + 1


def test_an_unset_reasoning_effort_keeps_older_hashes(request_: ChatRequest) -> None:
    # the hash of this request before `reasoning_effort` existed; recordings rely on it
    assert request_.reasoning_effort is None
    assert request_.prompt_hash() == OLD_HASH


def test_every_parameter_added_later_defaults_to_none() -> None:
    # left out of the hash while None; a later parameter with another default would change
    # every recorded hash
    later = [f for f in fields(ChatRequest) if f.name not in _HASHED_ALWAYS]
    assert [f.name for f in later] == ["reasoning_effort", "thinking"]
    assert all(f.default is None for f in later)
