from pathlib import Path

import pytest

from notinspec.config import ConfigError, load_config


def test_config_root_is_its_own_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "project" / "notinspec.yaml"
    path.parent.mkdir()
    path.write_text('\ufeffdocs:\n  paths: ["docs/**/*.md"]\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    config = load_config(path)
    assert config.root == path.parent.resolve()
    assert config.paths == ("docs/**/*.md",)
    assert len(config.content_hash) == 64


@pytest.mark.parametrize(
    "text, message",
    [
        ("docs: [", "cannot read config"),
        ("[]", "docs mapping"),
        ("docs: {}", "at least one"),
        ("docs: {paths: docs}", "list of relative"),
        ("docs: {paths: [false]}", "non-empty relative"),
        ('docs: {paths: [""]}', "non-empty relative"),
        ('docs: {paths: ["../*.md"]}', "inside the config directory"),
        ('docs: {paths: ["/tmp/*.md"]}', "inside the config directory"),
        ("docs: {openapi: 'C:\\outside.yaml'}", "inside the config directory"),
        ("docs: {openapi: 42}", "non-empty relative"),
        ('docs: {sphinx: "docs/", paths: ["README.md"]}', "sphinx is not supported"),
        ('docs: {paths: ["guide.md"], openpai: api.yaml}', "unknown docs field"),
        ('docs: {paths: ["guide.md"], paths: ["other.md"]}', "duplicate config key"),
        ('docs: {paths: ["guide.md"]}\ndocs: {openapi: api.yaml}', "duplicate config key"),
        ('docs: {paths: ["guide.md"], 1: value}', "config keys must be strings"),
    ],
)
def test_invalid_config_is_explained(tmp_path: Path, text: str, message: str) -> None:
    path = tmp_path / "notinspec.yaml"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ConfigError, match=message):
        load_config(path)


def test_openapi_only_config(tmp_path: Path) -> None:
    path = tmp_path / "notinspec.yaml"
    path.write_text("docs: {openapi: openapi.yaml}", encoding="utf-8")
    config = load_config(path)
    assert config.paths == ()
    assert config.openapi == "openapi.yaml"


def test_missing_config_is_explained(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="cannot read config"):
        load_config(tmp_path / "missing.yaml")
