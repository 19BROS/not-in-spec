import os
from collections.abc import Callable

import pytest

from notinspec.adapters.canonical import canonical_json


@pytest.fixture
def golden(request: pytest.FixtureRequest) -> Callable[[str, object], None]:
    """Compare an object with golden/<name>.json next to the test file.

    Run with UPDATE_GOLDEN=1 to rewrite the file. When output changes on purpose, regenerate the
    golden files in the same PR so the reviewer sees exactly what changed.
    """
    golden_dir = request.path.parent / "golden"

    def check(name: str, obj: object) -> None:
        path = golden_dir / f"{name}.json"
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
