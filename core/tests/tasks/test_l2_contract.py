"""The test-item contract for L2: claim reference, claim source, open prompt, schema 3."""

import json
from dataclasses import replace

import pytest

from notinspec.inventory import Source
from notinspec.inventory.objects import SOURCE_CONFIDENCE, SOURCE_PRIORITY
from notinspec.tasks import (
    ClaimReference,
    GenerationResult,
    Subject,
    TaskText,
    dumps,
    loads,
)
from notinspec.tasks import (
    TestItem as Item,
)

CLAIM = (
    "Setting the total parameter of urllib3.util.Retry to False disables retries"
    " and implies raise_on_redirect=False."
)


def l2_item(**changes: object) -> Item:
    item = Item(
        project="urllib3",
        chunk_id="c-retry",
        chunk_ids=("c-retry",),
        level="L2",
        question_kind="claim",
        reference=ClaimReference(
            Subject("urllib3.util.Retry", "total"), CLAIM, "c-retry/qwen3.8-flash-next/c3"
        ),
        sources=(Source("claim", section_id="s-retry"),),
        wording=TaskText(
            "What happens when Retry's total is set to False?",
            ("What does total=False do in Retry?", "Effect of passing False as total to Retry?"),
            "llm-qwen3.8-flash-next-v1",
            answer="disables retries",
        ),
        input_snapshot_hash="h",
        docs_version="latest",
        generator_version=4,
        operator_version=1,
    )
    return replace(item, **changes) if changes else item


def test_claim_reference_roundtrip() -> None:
    item = l2_item()
    result = GenerationResult((item,), ())
    again = loads(dumps(result))
    assert again.items == result.items
    assert again.items[0].id == item.id


def test_l2_identity_ignores_wording() -> None:
    other = TaskText(
        "Which retries stop when total is False?",
        ("a different paraphrase", "and another one"),
        "llm-qwen3.8-flash-next-v1",
        answer="raise_on_redirect=False",
    )
    assert l2_item(wording=other).id == l2_item().id


def test_l2_needs_answer() -> None:
    wording = replace(l2_item().wording, answer=None)
    with pytest.raises(ValueError):
        l2_item(wording=wording)


def test_claim_kind_needs_l2() -> None:
    with pytest.raises(ValueError):
        l2_item(level="L1")


def test_claim_source_is_low_and_not_merged() -> None:
    assert SOURCE_CONFIDENCE["claim"] == "low"
    assert "claim" not in SOURCE_PRIORITY


def test_l2_prompt_is_open() -> None:
    prompt = l2_item().model_prompt()
    assert prompt.answer_format == "open"
    assert prompt.text == l2_item().wording.text


def test_schema_2_rejected() -> None:
    with pytest.raises(ValueError, match="unsupported task schema version"):
        loads(json.dumps({"schema_version": 2, "items": [], "skipped": []}))
