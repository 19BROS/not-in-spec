"""What an NLI model returns, and what every grounding decision records (SPEC §6.4)."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Protocol

type Label = Literal["entailment", "neutral", "contradiction"]

LABELS: tuple[Label, ...] = ("entailment", "neutral", "contradiction")
# Decision = the label with the highest probability; a tie goes to the earlier label in LABELS.
DECISION_RULE = "argmax"


@dataclass(frozen=True)
class NliScores:
    """Probabilities for one (premise, hypothesis) pair."""

    entailment: float
    neutral: float
    contradiction: float
    # the premise did not fit the model's token limit and its end was cut off; the decision was
    # made on less text than the grounding step chose, so record it with the decision
    truncated: bool = False

    @property
    def label(self) -> Label:
        return max(LABELS, key=lambda label: float(getattr(self, label)))


class NliModel(Protocol):
    model_id: str
    revision: str  # pinned Hugging Face commit of the weights

    def score(self, pairs: Sequence[tuple[str, str]]) -> list[NliScores]:
        """Scores (premise, hypothesis) pairs, in input order."""
        ...


@dataclass(frozen=True)
class NliVersion:
    """Recorded with every decision, so it can be reproduced (SPEC §6.4)."""

    model_id: str
    revision: str
    decision_rule: str = DECISION_RULE

    @classmethod
    def of(cls, model: NliModel) -> "NliVersion":
        return cls(model.model_id, model.revision)
