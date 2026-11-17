"""Real ingestion, independent of the CLI, API and report format.

This stage reads all configured inputs. It does not generate tasks, evaluate models,
perform cross-checks or decide whether documentation is good enough for an LLM.
"""

import hashlib
from dataclasses import dataclass
from pathlib import Path

from notinspec.adapters.canonical import content_hash
from notinspec.adapters.openapi import NormalizedSpec, load_spec_bytes, normalize
from notinspec.chunking import (
    CHUNKER_VERSION,
    DEFAULT_SOFT_LIMIT,
    Chunk,
    Document,
    chunk_documents,
    normalize_text,
)
from notinspec.config import ConfigError, IngestConfig

INGESTION_SCHEMA_VERSION = 3  # 2: chunk id is the location, project added; 3: Block fields
_TEXT_SUFFIXES = frozenset({".md", ".markdown", ".txt"})


@dataclass(frozen=True)
class InputFile:
    source: str
    kind: str
    content_hash: str


@dataclass(frozen=True)
class OpenApiInput:
    source: str
    spec: NormalizedSpec  # adapter output, not the complete v3 inventory model


@dataclass(frozen=True)
class PlannedInput:
    source: str
    path: Path
    kind: str  # "markdown" | "openapi" | "sphinx" (a folder)
    xml_files: int = 0  # sphinx only: number of *.xml files in the folder


def plan_ingestion(
    config: IngestConfig, *, output: Path
) -> tuple[tuple[PlannedInput, ...], tuple[str, ...]]:
    """Select readable-format input paths without parsing content or writing anything."""
    output = output.resolve()
    if config.root.is_relative_to(output):
        raise ConfigError("output must not be the config directory or one of its parents")
    if output.exists() and not output.is_dir():
        raise ConfigError("output must be a directory")
    sphinx = _sphinx_folder(config, config.sphinx_xml, output) if config.sphinx_xml else None
    paths, warnings = _inputs(config, output)
    if not paths and sphinx is None:
        raise ConfigError("no input files matched the configured documentation")
    spec_path = _file(config, config.openapi) if config.openapi else None
    plan = []
    for source, path in sorted(paths.items()):
        if sphinx and path.is_relative_to(sphinx.path):
            if source in (config.openapi, config.changelog):
                raise ConfigError(f"{source}: explicit input inside docs.sphinx_xml")
            continue  # the Sphinx reader owns its folder (e.g. build-env.txt is not docs)
        kind = "openapi" if path == spec_path else "markdown"
        if kind == "markdown" and path.suffix.lower() not in _TEXT_SUFFIXES:
            raise ConfigError(f"{source}: unsupported text format; use Markdown or llms.txt")
        plan.append(PlannedInput(source, path, kind))
    if sphinx:
        plan.append(sphinx)
    return tuple(plan), tuple(warnings)


@dataclass(frozen=True)
class Ingestion:
    schema_version: int
    config_hash: str
    input_hash: str
    project: str
    chunker_version: int
    soft_limit: int
    files: tuple[InputFile, ...]
    chunks: tuple[Chunk, ...]
    openapi: tuple[OpenApiInput, ...]
    warnings: tuple[str, ...]


def ingest(
    config: IngestConfig, *, output: Path, soft_limit: int = DEFAULT_SOFT_LIMIT
) -> Ingestion:
    """Parse one snapshot. No absolute local paths or config secrets enter the output."""
    if soft_limit <= 0:
        raise ValueError("soft_limit must be positive")
    plan, plan_warnings = plan_ingestion(config, output=output)
    warnings = list(plan_warnings)
    files: list[InputFile] = []
    documents: list[Document] = []
    specs: list[OpenApiInput] = []
    for item in plan:
        source, path, kind = item.source, item.path, item.kind
        if kind == "sphinx":  # TODO(core/sphinx-demo step 5): read_sphinx_xml once PR A merges
            raise ConfigError(f"{source}: the Sphinx XML reader is not merged yet")
        data = path.read_bytes()
        files.append(InputFile(source, kind, hashlib.sha256(data).hexdigest()))
        if kind == "openapi":
            loaded = load_spec_bytes(data, source)
            spec = normalize(loaded.document)
            specs.append(OpenApiInput(source, spec))
            warnings.extend(f"{source}: {p}" for p in sorted(set(loaded.problems + spec.problems)))
            if loaded.problem_count > len(loaded.problems):
                warnings.append(
                    f"{source}: showing only {len(loaded.problems)} validation problems"
                )
        else:
            try:
                text = data.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = data.decode("utf-8-sig", errors="replace")
                warnings.append(f"{source}: invalid UTF-8 characters were replaced")
            documents.append(Document(source, normalize_text(text)))
    chunks = chunk_documents(documents, project=config.project, soft_limit=soft_limit)
    if documents and not chunks:
        warnings.append("text inputs contain no documentation content")
    return Ingestion(
        schema_version=INGESTION_SCHEMA_VERSION,
        config_hash=config.content_hash,
        input_hash=content_hash({f.source: f.content_hash for f in files}),
        project=config.project,
        chunker_version=CHUNKER_VERSION,
        soft_limit=soft_limit,
        files=tuple(files),
        chunks=chunks,
        openapi=tuple(specs),
        warnings=tuple(sorted(set(warnings))),
    )


def _file(config: IngestConfig, source: str) -> Path:
    path = (config.root / source).resolve()
    if not path.is_relative_to(config.root):
        raise ConfigError(f"input resolves outside the config directory: {source}")
    if not path.is_file():
        raise ConfigError(f"input is not a file: {source}")
    return path


def _inputs(config: IngestConfig, output: Path) -> tuple[dict[str, Path], list[str]]:
    paths: dict[str, Path] = {}
    warnings: list[str] = []
    for pattern in config.paths:
        matched = False
        for candidate in sorted(config.root.glob(pattern)):
            if not candidate.is_file():
                continue
            source = candidate.relative_to(config.root).as_posix()
            path = _file(config, source)
            if path.is_relative_to(output):
                continue  # a second run must not ingest its own comment.md
            paths[source] = path
            matched = True
        if not matched:
            warnings.append(f"no input files matched docs.paths pattern: {pattern}")
    for explicit_source in (config.openapi, config.changelog):
        if explicit_source:
            path = _file(config, explicit_source)
            if path.is_relative_to(output):
                raise ConfigError(
                    f"explicit input must not be inside the output directory: {explicit_source}"
                )
            paths[explicit_source] = path
    return paths, warnings


def _sphinx_folder(config: IngestConfig, source: str, output: Path) -> PlannedInput:
    """The `sphinx-build -b xml` folder: checked for shape only, nothing is parsed here."""
    path = (config.root / source).resolve()
    if not path.is_relative_to(config.root):
        raise ConfigError(f"docs.sphinx_xml resolves outside the config directory: {source}")
    if not path.is_dir():
        raise ConfigError(f"docs.sphinx_xml is not a folder: {source}")
    if path.is_relative_to(output) or output.is_relative_to(path):
        raise ConfigError("docs.sphinx_xml and the output directory must not contain each other")
    if not (path / "build-env.txt").is_file():
        raise ConfigError(
            f"{source}: build-env.txt is missing; write `sphinx-build --version` into it "
            "when you build the XML (see action/README.md)"
        )
    xml_files = sum(1 for p in path.rglob("*.xml") if p.is_file())
    if not xml_files:
        raise ConfigError(f"{source}: no *.xml files; build them with `sphinx-build -b xml`")
    return PlannedInput(source, path, "sphinx", xml_files)
