"""Recorded NLI scores, so unit tests and CI never load the real model (SPEC §13).

Like `FakeProvider` for LLMs: `RecordingNli` wraps the real model and keeps every score, and
`RecordedNli` replays them. A recording file is a JSON list of {"model", "revision", "premise",
"hypothesis", "entailment", "neutral", "contradiction", "truncated"}, sorted, so re-recording
the same pairs gives the same file. Scores are keyed by (model, revision, premise, hypothesis):
a new revision needs new recordings.
"""

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from notinspec.nli.local import MODEL_ID, REVISION
from notinspec.nli.scores import NliModel, NliScores

type Key = tuple[str, str, str, str]  # (model, revision, premise, hypothesis)


def _entry(key: Key, s: NliScores) -> dict[str, Any]:
    model, revision, premise, hypothesis = key
    return {
        "model": model,
        "revision": revision,
        "premise": premise,
        "hypothesis": hypothesis,
        "entailment": s.entailment,
        "neutral": s.neutral,
        "contradiction": s.contradiction,
        "truncated": s.truncated,
    }


def _read(path: Path) -> dict[Key, NliScores]:
    entries = json.loads(path.read_text(encoding="utf-8"))
    return {
        (e["model"], e["revision"], e["premise"], e["hypothesis"]): NliScores(
            e["entailment"], e["neutral"], e["contradiction"], e.get("truncated", False)
        )
        for e in entries
    }


def _write(path: Path, scores: dict[Key, NliScores]) -> None:
    entries = [_entry(k, scores[k]) for k in sorted(scores)]
    text = json.dumps(entries, indent=2, ensure_ascii=False, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8", newline="\n")  # same bytes on every OS


class RecordedNli:
    """NliModel that replays recorded scores; an unknown pair is an error, never a guess."""

    def __init__(
        self, scores: dict[Key, NliScores], model_id: str = MODEL_ID, revision: str = REVISION
    ) -> None:
        self.model_id = model_id
        self.revision = revision
        self._scores = scores
        self.calls: list[tuple[str, str]] = []

    @classmethod
    def load(cls, path: Path, model_id: str = MODEL_ID, revision: str = REVISION) -> "RecordedNli":
        return cls(_read(path), model_id, revision)

    def score(self, pairs: Sequence[tuple[str, str]]) -> list[NliScores]:
        self.calls.extend(pairs)
        out = []
        for premise, hypothesis in pairs:
            key = (self.model_id, self.revision, premise, hypothesis)
            if key not in self._scores:
                raise LookupError(
                    f"no recorded NLI score for {self.model_id}@{self.revision[:12]}: "
                    f"premise {premise[:60]!r}, hypothesis {hypothesis[:60]!r}"
                )
            out.append(self._scores[key])
        return out


class RecordingNli:
    """Wraps a real model and keeps every score, to be saved as a test fixture."""

    def __init__(self, inner: NliModel) -> None:
        self.model_id = inner.model_id
        self.revision = inner.revision
        self._inner = inner
        self._scores: dict[Key, NliScores] = {}

    def score(self, pairs: Sequence[tuple[str, str]]) -> list[NliScores]:
        scores = self._inner.score(pairs)
        for (premise, hypothesis), s in zip(pairs, scores, strict=True):
            self._scores[(self.model_id, self.revision, premise, hypothesis)] = s
        return scores

    def save(self, path: Path) -> None:
        """Writes the scores into `path`, keeping the entries already there (new ones win)."""
        existing = _read(path) if path.exists() else {}
        _write(path, existing | self._scores)
