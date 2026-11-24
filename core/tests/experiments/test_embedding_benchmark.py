"""No model loading: exercise visibility accounting and cache invalidation boundaries."""

import re
import runpy
from pathlib import Path

ROOT = Path(__file__).parents[3]
experiment = runpy.run_path(str(ROOT / "experiments/embeddings/benchmark.py"))


class FakeTokenizer:
    def __call__(self, text, *, truncation, max_length=None, return_offsets_mapping=False):
        words = list(re.finditer(r"\S+", text))
        if truncation:
            words = words[: max_length - 2]
        return {
            "input_ids": [101, *(w.group() for w in words), 102],
            "offset_mapping": [(0, 0), *(w.span() for w in words), (0, 0)],
        }


def test_cache_changes_with_encoding_settings(monkeypatch):
    key = experiment["cache_key"](["same text"])
    monkeypatch.setitem(experiment["ENCODING"], "max_length", 512)
    assert experiment["cache_key"](["same text"]) != key
    monkeypatch.setitem(experiment["ENCODING"], "max_length", 256)
    monkeypatch.setitem(experiment["ENCODING"], "pooling", "different-pooling")
    assert experiment["cache_key"](["same text"]) != key


def test_edits_outside_the_window_are_separate_from_visible_edits(monkeypatch):
    monkeypatch.setitem(experiment["ENCODING"], "max_length", 6)
    for before, inside in (("a b c d e target", False), ("target a b c d e", True)):
        case = {
            "before": before,
            "after": before.replace("target", "other"),
            "edit": {"old": "target", "new": "other", "start": before.index("target")},
        }
        audit = experiment["audit_edit_window"](case, FakeTokenizer())
        assert audit["edit_inside_window"] == {"before": inside, "after": inside}
        assert audit["encoded_input_changed"] == inside
        assert audit["truncated"] == {"before": True, "after": True}


def test_skipping_audit_does_not_count_truncation_or_tokenization_blind_spots():
    base = {
        "semantic_change": True,
        "cosine": 1.0,
        "edit_inside_window": {"before": True, "after": True},
        "encoded_input_changed": True,
    }
    rows = [
        {**base, "kind": "visible"},
        {**base, "kind": "truncated", "edit_inside_window": {"before": False, "after": False}},
        {**base, "kind": "same-tokens", "encoded_input_changed": False},
    ]
    assert experiment["skipping_audit"](rows, 0.99) == ["visible"]


def test_unit_mutates_prose_and_negation_is_before_the_old_truncated_tail():
    cases = {c["kind"]: c for c in experiment["diff_cases"]()}
    unit = cases["unit"]
    assert "the given number of milliseconds" in unit["after"]
    assert "trio.sleep(seconds: float)" in unit["before"]
    assert "trio.sleep(seconds: float)" in unit["after"]
    assert cases["negation"]["edit"]["old"] == "will not work by default"
    assert cases["truncation_control"]["edit"]["old"] == "isn’t required"
