"""NLI for claim grounding and K5 (SPEC §6.4): the local cross-encoder and its recorded fake.

Importing this package never imports torch; only TransformersNli.load() / score() does.
"""

from notinspec.nli.local import (
    MAX_LENGTH,
    MODEL_ID,
    REVISION,
    NliUnavailable,
    TransformersNli,
)
from notinspec.nli.recorded import RecordedNli, RecordingNli
from notinspec.nli.scores import DECISION_RULE, LABELS, Label, NliModel, NliScores, NliVersion

__all__ = [
    "DECISION_RULE",
    "LABELS",
    "MAX_LENGTH",
    "MODEL_ID",
    "REVISION",
    "Label",
    "NliModel",
    "NliScores",
    "NliUnavailable",
    "NliVersion",
    "RecordedNli",
    "RecordingNli",
    "TransformersNli",
]
