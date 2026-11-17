"""The supported ingestion subset of notinspec.yaml (SPEC section 2.3).

Paths are relative to the config, not the terminal's working directory. `claims:` sets the
claim extractors and which chunks they read. Other top-level settings (models, budget,
thresholds) are left for later pipeline stages.
"""

import hashlib
import os
from dataclasses import dataclass, field
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


_DOC_FIELDS = frozenset({"paths", "openapi", "changelog", "sphinx_xml", "version"})
_CLAIMS_FIELDS = frozenset({"extractors", "sources"})


@dataclass(frozen=True)
class ClaimsConfig:
    """`claims:` in the config. Empty tuples mean the defaults."""

    extractors: tuple[str, ...] = ()  # model IDs; () = the two default extractors (SPEC §6.4)
    sources: tuple[str, ...] = ()  # glob patterns over a chunk's `source`; () = every chunk


@dataclass(frozen=True)
class IngestConfig:
    root: Path
    content_hash: str
    project: str  # root of every breadcrumb (SPEC section 6.1)
    paths: tuple[str, ...]
    openapi: str | None
    changelog: str | None
    sphinx_xml: str | None = None  # folder with `sphinx-build -b xml` output + build-env.txt
    claims: ClaimsConfig = field(default_factory=ClaimsConfig)


def load_config(path: Path) -> IngestConfig:
    try:
        data = path.read_bytes()
        config = yaml.load(data.decode("utf-8-sig"), Loader=_ConfigLoader)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ConfigError(f"cannot read config {path}: {exc}") from exc
    if not isinstance(config, dict) or not isinstance(config.get("docs"), dict):
        raise ConfigError("config must contain a docs mapping")
    docs = config["docs"]
    if "sphinx" in docs:
        raise ConfigError(
            "docs.sphinx was replaced by docs.sphinx_xml: build the XML with "
            "`sphinx-build -b xml` in a separate job without secrets and point to its folder"
        )
    if unknown := sorted(set(docs) - _DOC_FIELDS):
        raise ConfigError(f"unknown docs field(s): {', '.join(unknown)}")
    sphinx_xml = _optional_path(docs.get("sphinx_xml"), "docs.sphinx_xml")
    if sphinx_xml == ".":
        raise ConfigError("docs.sphinx_xml must be a folder below the config directory")
    paths = docs.get("paths", [])
    if not isinstance(paths, list):
        raise ConfigError("docs.paths must be a list of relative file patterns")
    patterns = tuple(relative_path(value, "docs.paths") for value in paths)
    openapi = _optional_path(docs.get("openapi"), "docs.openapi")
    changelog = _optional_path(docs.get("changelog"), "docs.changelog")
    if not patterns and openapi is None and changelog is None and sphinx_xml is None:
        raise ConfigError(
            "configure at least one of docs.sphinx_xml, docs.paths, docs.openapi or docs.changelog"
        )
    root = path.resolve().parent
    return IngestConfig(
        root=root,
        content_hash=hashlib.sha256(data).hexdigest(),
        project=_project(config.get("project"), root),
        paths=patterns,
        openapi=openapi,
        changelog=changelog,
        sphinx_xml=sphinx_xml,
        claims=_claims(config.get("claims")),
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


def _project(value: object, root: Path) -> str:
    """`project:` from the config; default: the repo name (in CI) or the config's folder."""
    if value is None:
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        return repository.rpartition("/")[2] or root.name
    if not isinstance(value, str) or not value.strip():
        raise ConfigError("project must be a non-empty string")
    if ">" in value or "\n" in value:
        raise ConfigError("project must be one line without '>' (it starts every breadcrumb)")
    return value.strip()


def _claims(value: object) -> ClaimsConfig:
    if value is None:
        return ClaimsConfig()
    if not isinstance(value, dict):
        raise ConfigError("claims must be a mapping")
    if unknown := sorted(set(value) - _CLAIMS_FIELDS):
        raise ConfigError(f"unknown claims field(s): {', '.join(unknown)}")
    extractors = _strings(value.get("extractors", []), "claims.extractors")
    if len(set(extractors)) != len(extractors):
        raise ConfigError("claims.extractors must not repeat a model")
    return ClaimsConfig(extractors, _strings(value.get("sources", []), "claims.sources"))


def _strings(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        raise ConfigError(f"{name} must be a list of non-empty strings")
    return tuple(v.strip() for v in value)


def _optional_path(value: object, field: str) -> str | None:
    return None if value is None else relative_path(value, field)
