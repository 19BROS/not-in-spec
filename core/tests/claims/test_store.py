import json
from dataclasses import replace
from pathlib import Path

import pytest

from notinspec.claims import (
    JsonlCallLog,
    JsonlClaimStore,
    LlmCall,
    RawClaim,
    ReuseKey,
    StoredAnswer,
)
from notinspec.claims.parse import PARSER_VERSION

KEY = ReuseKey("abc", "p > Guide", "x", "acme/model", 1)
OTHER = ReuseKey("def", "p", "x", "acme/model", 1)
CLAIM = RawClaim("c1", "Timeouts are in seconds.", "in seconds", "fact")
ANSWER = StoredAnswer((CLAIM,), ("claim 2: unknown type 'opinion'",), "r1", "h1", "acme/model-1")
EMPTY = StoredAnswer((), (), "r2", "h2", "acme/model-1")


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
    store.put(KEY, ANSWER)
    store.put(OTHER, EMPTY)
    reopened = JsonlClaimStore(path)
    assert reopened.get(KEY) == ANSWER
    assert reopened.get(OTHER) == EMPTY
    assert reopened.get(ReuseKey("abc", "p > Guide", "x", "acme/model", 2)) is None
    assert reopened.warnings == []


def test_later_entry_wins(tmp_path: Path) -> None:
    path = tmp_path / "claims-store.jsonl"
    JsonlClaimStore(path).put(KEY, ANSWER)
    JsonlClaimStore(path).put(KEY, EMPTY)
    assert JsonlClaimStore(path).get(KEY) == EMPTY


def test_cut_off_last_line_is_removed_with_a_warning(tmp_path: Path) -> None:
    path = tmp_path / "claims-store.jsonl"
    store = JsonlClaimStore(path)
    store.put(KEY, ANSWER)
    store.put(OTHER, EMPTY)
    whole = path.read_bytes()
    path.write_bytes(whole[:-30])  # killed while writing the second entry
    reopened = JsonlClaimStore(path)
    assert reopened.get(KEY) == ANSWER and reopened.get(OTHER) is None
    assert len(reopened.warnings) == 1
    assert "claims-store.jsonl:2: removed a cut-off last line" in reopened.warnings[0]
    # the file is usable again: the next entry starts on its own line
    reopened.put(OTHER, EMPTY)
    again = JsonlClaimStore(path)
    assert again.get(OTHER) == EMPTY and again.warnings == []


def test_whole_last_line_without_its_newline_is_kept(tmp_path: Path) -> None:
    path = tmp_path / "claims-store.jsonl"
    JsonlClaimStore(path).put(KEY, ANSWER)
    path.write_bytes(path.read_bytes().rstrip(b"\n"))
    store = JsonlClaimStore(path)
    assert store.get(KEY) == ANSWER and store.warnings == []
    store.put(OTHER, EMPTY)
    assert JsonlClaimStore(path).get(OTHER) == EMPTY


def test_broken_line_in_the_middle_is_an_error(tmp_path: Path) -> None:
    path = tmp_path / "claims-store.jsonl"
    store = JsonlClaimStore(path)
    store.put(KEY, ANSWER)
    store.put(OTHER, EMPTY)
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(f'{{"key": {{"content_hash": "a"}}}}\n{lines[1]}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="claims-store.jsonl:1"):
        JsonlClaimStore(path)


def test_reasoning_effort_is_part_of_the_key(tmp_path: Path) -> None:
    path = tmp_path / "claims-store.jsonl"
    # an entry written before the key had `reasoning_effort`
    old = {"key": {k: v for k, v in vars(KEY).items() if k != "reasoning_effort"}}
    old["answer"] = {
        "claims": [vars(CLAIM)],
        "problems": [],
        "run_id": "r1",
        "prompt_hash": "h1",
        "model": "acme/model-1",
    }
    path.write_text(json.dumps(old) + "\n", encoding="utf-8")
    store = JsonlClaimStore(path)
    assert store.get(KEY) is not None
    assert store.get(ReuseKey("abc", "p > Guide", "x", "acme/model", 1, "low")) is None


def test_an_answer_parsed_by_an_older_parser_is_not_reused(tmp_path: Path) -> None:
    path = tmp_path / "claims-store.jsonl"
    # an entry written before the key had `parser_version`: parser 1 stored cut-off answers
    old = {"key": {k: v for k, v in vars(KEY).items() if k != "parser_version"}}
    old["answer"] = {
        "claims": [vars(CLAIM)],
        "problems": [],
        "run_id": "r1",
        "prompt_hash": "h1",
        "model": "acme/model-1",
    }
    path.write_text(json.dumps(old) + "\n", encoding="utf-8")
    store = JsonlClaimStore(path)
    assert store.get(KEY) is not None  # KEY has no parser version either
    assert store.get(replace(KEY, parser_version=PARSER_VERSION)) is None
