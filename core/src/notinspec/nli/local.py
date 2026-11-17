"""The local NLI cross-encoder (SPEC §6.4): transformers sequence classification, CPU only.

torch and transformers come from the optional extra `notinspec[nli]` and are imported only when
the model is loaded, so the rest of `core` works without them. The weights are read from the
Hugging Face cache (`HF_HOME`) at a pinned revision. The worker runs with `HF_HUB_OFFLINE=1`, so
a missing model is an error, never a download in the middle of a run; `python -m notinspec.nli
fetch` downloads it once.
"""

import logging
from collections.abc import Sequence
from typing import Any, Protocol

from notinspec.nli.scores import LABELS, Label, NliScores

log = logging.getLogger(__name__)

# Chosen in experiments/nli (runs 001-007). Pinned: a new upload under the same name must not
# change grounding decisions silently. Bump both together, and re-record the test scores.
MODEL_ID = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
REVISION = "b3546ea6b0346eb6f8d5d68b13c7dc6d0376b3d7"  # main as of 2024-04-11
MAX_LENGTH = 512  # tokens of premise + hypothesis; the model's position limit
BATCH_SIZE = 8  # experiments/nli default; pairs are sorted by length, so little padding


class NliUnavailable(RuntimeError):
    """The model cannot be loaded: the extra is not installed or the weights are not cached."""


class Backend(Protocol):
    """A loaded model. Tests replace it with a fake, so batching is tested without torch."""

    def lengths(self, pairs: Sequence[tuple[str, str]]) -> list[int]:
        """Tokens of each pair before truncation."""
        ...

    def probabilities(
        self, pairs: Sequence[tuple[str, str]], max_length: int
    ) -> list[dict[Label, float]]:
        """Label probabilities of each pair, premise truncated to fit max_length tokens."""
        ...


class TransformersNli:
    """NliModel on the real cross-encoder. Loads the model on first use (or on load())."""

    def __init__(
        self,
        model_id: str = MODEL_ID,
        revision: str = REVISION,
        *,
        batch_size: int = BATCH_SIZE,
        threads: int | None = None,  # torch CPU threads; None = torch's default (fastest, run 003)
        max_length: int = MAX_LENGTH,
        backend: Backend | None = None,
    ) -> None:
        if batch_size < 1:
            raise ValueError("batch_size must be at least 1")
        self.model_id = model_id
        self.revision = revision
        self.batch_size = batch_size
        self.threads = threads
        self.max_length = max_length
        self._backend = backend

    def load(self) -> Backend:
        if self._backend is None:
            self._backend = _TorchBackend(self.model_id, self.revision, self.threads)
        return self._backend

    def score(self, pairs: Sequence[tuple[str, str]]) -> list[NliScores]:
        backend = self.load()
        # similar lengths in one batch = less padding; results go back in input order
        order = sorted(range(len(pairs)), key=lambda i: len(pairs[i][0]) + len(pairs[i][1]))
        out: list[NliScores | None] = [None] * len(pairs)
        truncated = 0
        for start in range(0, len(order), self.batch_size):
            idx = order[start : start + self.batch_size]
            batch = [pairs[i] for i in idx]
            lengths = backend.lengths(batch)
            probs = backend.probabilities(batch, self.max_length)
            for i, n, p in zip(idx, lengths, probs, strict=True):
                cut = n > self.max_length
                truncated += cut
                out[i] = NliScores(p["entailment"], p["neutral"], p["contradiction"], cut)
        if truncated:
            log.warning(
                "%s: %d of %d premises cut at %d tokens", self.model_id, truncated, len(pairs),
                self.max_length,
            )  # fmt: skip
        return [s for s in out if s is not None]


class _TorchBackend:
    def __init__(self, model_id: str, revision: str, threads: int | None) -> None:
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer
        except ImportError as e:
            raise NliUnavailable("NLI needs the optional dependencies: notinspec[nli]") from e
        from transformers.utils import logging as hf_logging

        hf_logging.disable_progress_bar()  # one bar line per layer group floods the worker log
        if threads:
            torch.set_num_threads(threads)
        try:
            self._tokenizer: Any = AutoTokenizer.from_pretrained(model_id, revision=revision)
            # Always fp32: transformers otherwise keeps the checkpoint dtype, and this checkpoint
            # is fp16, which is ~9x slower on CPU with the same decisions (experiments/nli run 003)
            self._model: Any = AutoModelForSequenceClassification.from_pretrained(
                model_id, revision=revision, dtype=torch.float32
            ).eval()
        except OSError as e:
            raise NliUnavailable(
                f"{model_id} at {revision[:12]} is not in the Hugging Face cache; "
                "download it once with `python -m notinspec.nli fetch` (needs network)"
            ) from e
        id2label = {int(i): str(label).lower() for i, label in self._model.config.id2label.items()}
        if sorted(id2label.values()) != sorted(LABELS):
            raise NliUnavailable(f"{model_id}: expected labels {LABELS}, got {id2label}")
        self._labels: list[Label] = [
            next(label for label in LABELS if label == id2label[i]) for i in sorted(id2label)
        ]
        self._torch: Any = torch

    def lengths(self, pairs: Sequence[tuple[str, str]]) -> list[int]:
        enc = self._tokenizer([p for p, _ in pairs], [h for _, h in pairs], verbose=False)
        return [len(ids) for ids in enc["input_ids"]]

    def probabilities(
        self, pairs: Sequence[tuple[str, str]], max_length: int
    ) -> list[dict[Label, float]]:
        enc = self._tokenizer(
            [p for p, _ in pairs],
            [h for _, h in pairs],
            truncation="only_first",  # cut the premise, never the claim
            max_length=max_length,
            padding=True,
            return_tensors="pt",
        )
        with self._torch.inference_mode():
            logits = self._model(**enc).logits
        rows: list[list[float]] = self._torch.softmax(logits, dim=-1).tolist()
        return [dict(zip(self._labels, row, strict=True)) for row in rows]
