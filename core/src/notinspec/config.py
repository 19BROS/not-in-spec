"""The supported ingestion subset of notinspec.yaml (SPEC section 2.3).

Paths are relative to the config, not the terminal's working directory. Other top-level
settings (models, budget, thresholds) are left for later pipeline stages.
"""

import hashlib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

import yaml


class ConfigError(ValueError):
    """The configuration cannot be used by the ingestion prototype."""


class _ConfigLoader(yaml.SafeLoader):
    """Do not silently replace an earlier config entry with a duplicate key."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        self.flatten_mapping(node)
        result: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ConfigError(
                    f"config keys must be strings (line {key_node.start_mark.line + 1})"
                )
            if key in result:
                raise ConfigError(
                    f"duplicate config key {key!r} (line {key_node.start_mark.line + 1})"
                )
            result[key] = self.construct_object(value_node, deep=deep)
        return result


_DOC_FIELDS = frozenset({"paths", "openapi", "changelog", "sphinx", "version"})


@dataclass(frozen=True)
class IngestConfig:
    root: Path
    content_hash: str
    paths: tuple[str, ...]
    openapi: str | None
    changelog: str | None


def load_config(path: Path) -> IngestConfig:
    try:
        data = path.read_bytes()
        config = yaml.load(data.decode("utf-8-sig"), Loader=_ConfigLoader)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ConfigError(f"cannot read config {path}: {exc}") from exc
    if not isinstance(config, dict) or not isinstance(config.get("docs"), dict):
        raise ConfigError("config must contain a docs mapping")
    docs = config["docs"]
    if unknown := sorted(set(docs) - _DOC_FIELDS):
        raise ConfigError(f"unknown docs field(s): {', '.join(unknown)}")
    if docs.get("sphinx") is not None:
        raise ConfigError(
            "docs.sphinx is not supported yet; use docs.paths for Markdown or docs.openapi"
        )
    paths = docs.get("paths", [])
    if not isinstance(paths, list):
        raise ConfigError("docs.paths must be a list of relative file patterns")
    patterns = tuple(relative_path(value, "docs.paths") for value in paths)
    openapi = _optional_path(docs.get("openapi"), "docs.openapi")
    changelog = _optional_path(docs.get("changelog"), "docs.changelog")
    if not patterns and openapi is None and changelog is None:
        raise ConfigError("configure at least one of docs.paths, docs.openapi or docs.changelog")
    return IngestConfig(
        root=path.resolve().parent,
        content_hash=hashlib.sha256(data).hexdigest(),
        paths=patterns,
        openapi=openapi,
        changelog=changelog,
    )


def relative_path(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\0" in value:
        raise ConfigError(f"{field} must contain non-empty relative paths")
    value = value.replace("\\", "/")
    if (
        PurePosixPath(value).is_absolute()
        or PureWindowsPath(value).drive
        or ".." in PurePosixPath(value).parts
    ):
        raise ConfigError(f"{field}: paths must stay inside the config directory: {value}")
    return PurePosixPath(value).as_posix()


def _optional_path(value: object, field: str) -> str | None:
    return None if value is None else relative_path(value, field)
