import json
from pathlib import Path

import pytest

from notinspec.claims import JsonlCallLog, JsonlClaimStore, LlmCall, RawClaim, ReuseKey

KEY = ReuseKey("abc", "p > Guide", "x", "acme/model", 1)
CLAIM = RawClaim("c1", "Timeouts are in seconds.", "in seconds", "fact")


def _call(n: int) -> LlmCall:
    return LlmCall(
        run_id="r",
        role="claim-extractor",
        extractor="x",
        chunk_id=f"chunk{n}",
        model="acme/model",
        prompt_hash="h",
        request={"model": "acme/model"},
        response={"choices": []} if n else None,
        error=None if n else "ProviderError: down",
        time="2026-11-17T00:00:00+00:00",
    )


def test_call_log_only_appends(tmp_path: Path) -> None:
    path = tmp_path / "llm-calls.jsonl"
    path.write_text('{"earlier": true}\n', encoding="utf-8")
    log = JsonlCallLog(path)
    log.append(_call(0))
    log.append(_call(1))
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == '{"earlier": true}'
    assert [json.loads(line)["chunk_id"] for line in lines[1:]] == ["chunk0", "chunk1"]
    assert json.loads(lines[1])["response"] is None


def test_claim_store_survives_a_new_process(tmp_path: Path) -> None:
    path = tmp_path / "claims-store.jsonl"
    store = JsonlClaimStore(path)
    assert store.get(KEY) is None
    store.put(KEY, (CLAIM,))
    store.put(ReuseKey("def", "p", "x", "acme/model", 1), ())
    reopened = JsonlClaimStore(path)
    assert reopened.get(KEY) == (CLAIM,)
    assert reopened.get(ReuseKey("def", "p", "x", "acme/model", 1)) == ()
    assert reopened.get(ReuseKey("abc", "p > Guide", "x", "acme/model", 2)) is None


def test_later_entry_wins(tmp_path: Path) -> None:
    path = tmp_path / "claims-store.jsonl"
    JsonlClaimStore(path).put(KEY, (CLAIM,))
    JsonlClaimStore(path).put(KEY, ())
    assert JsonlClaimStore(path).get(KEY) == ()


def test_broken_store_is_an_error(tmp_path: Path) -> None:
    path = tmp_path / "claims-store.jsonl"
    path.write_text('{"key": {"content_hash": "a"}}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="claims-store.jsonl:1"):
        JsonlClaimStore(path)
