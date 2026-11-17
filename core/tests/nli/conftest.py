from pathlib import Path

import pytest

from notinspec.nli import Label, RecordedNli
from notinspec.nli.bench import SAMPLE

# Longer than 512 tokens, so the premise is cut. The claim is in the first sentence.
_FILLER = "This same mechanism also handles redirects, and the number of retries can be set. "
LONG_PAIR = (
    "urllib3 > User Guide > Retrying Requests:\n\n"
    "urllib3 can automatically retry idempotent requests. " + _FILLER * 40,
    "urllib3 can automatically retry idempotent requests.",
)


@pytest.fixture(scope="session")
def recorded_path() -> Path:
    """Scores of the real model (MODEL_ID at REVISION, fp32) for `pairs`, recorded by
    test_real_model.py with RECORD_NLI=1. Unit tests replay them; CI never loads the model."""
    return Path(__file__).parent / "fixtures" / "deberta-large.json"


@pytest.fixture(scope="session")
def pairs() -> tuple[tuple[str, str], ...]:
    return (*SAMPLE, LONG_PAIR)


@pytest.fixture(scope="session")
def gold() -> tuple[Label, ...]:
    """Hand labels of `pairs` (experiments/nli); the pinned model gets all of them right."""
    return ("entailment",) * 3 + ("neutral",) * 3 + ("contradiction",) * 3 + ("entailment",)


@pytest.fixture
def recorded_nli(recorded_path: Path) -> RecordedNli:
    return RecordedNli.load(recorded_path)
