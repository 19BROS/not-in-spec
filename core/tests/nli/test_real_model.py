"""The real cross-encoder (SPEC §13: marked slow, skipped in CI, which has no torch).

Runs only where `notinspec[nli]` is installed and the pinned model is already in the HF cache;
it never downloads. RECORD_NLI=1 re-records tests/nli/fixtures/deberta-large.json instead of
comparing with it (do that after bumping MODEL_ID / REVISION, in the same PR).
"""

import os
from pathlib import Path

import pytest

from notinspec.nli import MODEL_ID, REVISION, Label, RecordedNli, RecordingNli, TransformersNli
from notinspec.nli.bench import FILES, fetch

pytestmark = pytest.mark.slow
pytest.importorskip("transformers")
hub = pytest.importorskip("huggingface_hub")
if any(
    not isinstance(hub.try_to_load_from_cache(MODEL_ID, f, revision=REVISION), str) for f in FILES
):
    pytest.skip("pinned NLI model not in the HF cache", allow_module_level=True)

Pairs = tuple[tuple[str, str], ...]


@pytest.fixture(scope="module")
def real() -> TransformersNli:
    return TransformersNli()


def test_real_model_matches_the_recorded_scores(
    real: TransformersNli, pairs: Pairs, gold: tuple[Label, ...], recorded_path: Path
) -> None:
    if os.environ.get("RECORD_NLI") == "1":
        recording = RecordingNli(real)
        recording.score(pairs)
        recorded_path.parent.mkdir(parents=True, exist_ok=True)
        recording.save(recorded_path)
    scores = real.score(pairs)
    recorded = RecordedNli.load(recorded_path).score(pairs)
    assert [s.label for s in scores] == list(gold)
    for got, want in zip(scores, recorded, strict=True):
        assert got.truncated == want.truncated
        # CPU kernels differ a little between machines; decisions must not
        assert got.entailment == pytest.approx(want.entailment, abs=1e-3)
        assert got.contradiction == pytest.approx(want.contradiction, abs=1e-3)


def test_a_long_premise_is_cut_and_marked(real: TransformersNli, pairs: Pairs) -> None:
    short, long = real.score(pairs[-2:])
    assert not short.truncated
    assert long.truncated


def test_batch_size_does_not_change_scores(real: TransformersNli, pairs: Pairs) -> None:
    one = TransformersNli(batch_size=1, backend=real.load()).score(pairs[:4])
    many = real.score(pairs[:4])
    for a, b in zip(one, many, strict=True):
        assert a.entailment == pytest.approx(b.entailment, abs=1e-4)


def test_fetch_finds_the_cached_model_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(hub.constants, "HF_HUB_OFFLINE", True)
    path = fetch()
    assert path.name == REVISION
    assert all((path / f).is_file() for f in FILES)
