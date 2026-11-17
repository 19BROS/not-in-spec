"""NLI runtime without the real model: recorded scores and a fake backend (SPEC §13)."""

import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

import pytest

from notinspec.nli import (
    DECISION_RULE,
    MODEL_ID,
    REVISION,
    Label,
    NliScores,
    NliUnavailable,
    NliVersion,
    RecordedNli,
    RecordingNli,
    TransformersNli,
)
from notinspec.nli.__main__ import main
from notinspec.nli.bench import bench

Pairs = tuple[tuple[str, str], ...]


class FakeBackend:
    """Entailment = 1 / premise length in characters, so the order of results is visible.
    One token per character."""

    def __init__(self) -> None:
        self.batches: list[list[tuple[str, str]]] = []

    def lengths(self, pairs: Sequence[tuple[str, str]]) -> list[int]:
        return [len(p) + len(h) for p, h in pairs]

    def probabilities(
        self, pairs: Sequence[tuple[str, str]], max_length: int
    ) -> list[dict[Label, float]]:
        self.batches.append(list(pairs))
        return [
            {"entailment": 1 / len(p), "neutral": 1 - 1 / len(p), "contradiction": 0.0}
            for p, _ in pairs
        ]


# ------------------------------------------------------------------ scores


@pytest.mark.parametrize(
    ("scores", "label"),
    [
        ((0.8, 0.15, 0.05), "entailment"),
        ((0.3, 0.6, 0.1), "neutral"),
        ((0.1, 0.2, 0.7), "contradiction"),
        ((0.4, 0.4, 0.2), "entailment"),  # a tie goes to the earlier label
        ((0.2, 0.4, 0.4), "neutral"),
    ],
)
def test_label_is_the_argmax(scores: tuple[float, float, float], label: str) -> None:
    assert NliScores(*scores).label == label


def test_version_records_model_revision_and_rule(recorded_nli: RecordedNli) -> None:
    assert NliVersion.of(recorded_nli) == NliVersion(MODEL_ID, REVISION, "argmax")
    assert DECISION_RULE == "argmax"


# ------------------------------------------------------------------ recorded


def test_recorded_scores_replay_the_real_model(
    recorded_nli: RecordedNli, pairs: Pairs, gold: tuple[Label, ...]
) -> None:
    scores = recorded_nli.score(pairs)
    assert [s.label for s in scores] == list(gold)
    assert [s.truncated for s in scores] == [False] * (len(pairs) - 1) + [True]
    assert recorded_nli.calls == list(pairs)


def test_unknown_pair_is_an_error(recorded_nli: RecordedNli) -> None:
    with pytest.raises(LookupError, match="no recorded NLI score"):
        recorded_nli.score([("urllib3 > Foo:\n\nBar.", "Baz.")])


def test_another_revision_does_not_reuse_scores(recorded_path: Path, pairs: Pairs) -> None:
    other = RecordedNli.load(recorded_path, revision="0" * 40)
    with pytest.raises(LookupError):
        other.score(pairs[:1])


def test_recording_round_trip_merges_and_is_stable(
    recorded_nli: RecordedNli, pairs: Pairs, tmp_path: Path
) -> None:
    path = tmp_path / "scores.json"
    first = RecordingNli(recorded_nli)
    first.score(pairs[:3])
    first.save(path)
    second = RecordingNli(recorded_nli)
    second.score(pairs[3:])
    second.save(path)  # keeps the first three
    replay = RecordedNli.load(path)
    assert replay.score(pairs) == recorded_nli.score(pairs)

    # re-recording the same pairs in another order writes the same bytes
    again = RecordingNli(recorded_nli)
    again.score(list(reversed(pairs)))
    again.save(tmp_path / "again.json")
    assert (tmp_path / "again.json").read_bytes() == path.read_bytes()


# ------------------------------------------------------------------ TransformersNli


def test_results_come_back_in_input_order_batched_by_length() -> None:
    backend = FakeBackend()
    nli = TransformersNli(batch_size=2, backend=backend)
    pairs = [("x" * n, "h") for n in (5, 1, 4, 2, 3)]
    scores = nli.score(pairs)
    assert [round(1 / s.entailment) for s in scores] == [5, 1, 4, 2, 3]
    assert [[len(p) for p, _ in b] for b in backend.batches] == [[1, 2], [3, 4], [5]]


def test_a_pair_over_max_length_is_marked_truncated(caplog: pytest.LogCaptureFixture) -> None:
    nli = TransformersNli(max_length=10, backend=FakeBackend())
    scores = nli.score([("x" * 9, "h"), ("x" * 10, "h")])
    assert [s.truncated for s in scores] == [False, True]
    assert "1 of 2 premises cut at 10 tokens" in caplog.text


def test_no_pairs_no_batches() -> None:
    backend = FakeBackend()
    assert TransformersNli(backend=backend).score([]) == []
    assert backend.batches == []


def test_batch_size_must_be_positive() -> None:
    with pytest.raises(ValueError):
        TransformersNli(batch_size=0)


def test_without_the_extra_loading_fails_clearly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "torch", None)
    monkeypatch.setitem(sys.modules, "transformers", None)
    nli = TransformersNli()
    assert (nli.model_id, nli.revision) == (MODEL_ID, REVISION)
    with pytest.raises(NliUnavailable, match=r"notinspec\[nli\]"):
        nli.score([("a", "b")])


def test_importing_nli_does_not_import_torch() -> None:
    code = "import sys, notinspec.nli, notinspec.nli.bench; assert 'torch' not in sys.modules"
    subprocess.run([sys.executable, "-c", code], check=True)


# ------------------------------------------------------------------ bench / __main__


def test_bench_counts_pairs(recorded_nli: RecordedNli) -> None:
    result = bench(recorded_nli, pairs=12)
    assert result.pairs == 12
    assert len(recorded_nli.calls) == 12
    assert result.pairs_per_second > 0


def test_main_bench_prints_a_report(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "notinspec.nli.__main__.TransformersNli",
        lambda **kw: TransformersNli(**kw, backend=FakeBackend()),
    )
    assert main(["bench", "--pairs", "4", "--batch", "2"]) == 0
    out = capsys.readouterr().out
    assert f'"revision": "{REVISION}"' in out
    assert '"pairs": 4' in out


def test_main_reports_a_missing_model(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def missing() -> Path:
        raise NliUnavailable("not in the Hugging Face cache")

    monkeypatch.setattr("notinspec.nli.__main__.fetch", missing)
    assert main(["fetch"]) == 1
    assert "not in the Hugging Face cache" in capsys.readouterr().err
