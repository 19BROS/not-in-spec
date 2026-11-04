from pathlib import Path

import pytest


@pytest.fixture
def fixtures() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).parents[3]
