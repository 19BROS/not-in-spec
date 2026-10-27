import os
from collections.abc import Callable
from pathlib import Path

import pytest

from notinspec.adapters.canonical import canonical_json

GOLDEN_DIR = Path(__file__).parent / "golden"


@pytest.fixture
def fixtures() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).parents[3]


@pytest.fixture
def golden() -> Callable[[str, object], None]:
    """Compare an object with golden/<name>.json. Run with UPDATE_GOLDEN=1 to rewrite the file.

    When output changes on purpose, regenerate the golden files in the same PR so the reviewer
    sees exactly what changed.
    """

    def check(name: str, obj: object) -> None:
        path = GOLDEN_DIR / f"{name}.json"
        actual = canonical_json(obj, pretty=True).decode()
        if os.environ.get("UPDATE_GOLDEN") == "1":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(actual, encoding="utf-8")
            return
        if not path.exists():
            pytest.fail(f"missing golden file {path}; run with UPDATE_GOLDEN=1 to create it")
        assert actual == path.read_text(encoding="utf-8"), (
            f"output differs from {path.name}; if intended, rerun with UPDATE_GOLDEN=1"
        )

    return check
