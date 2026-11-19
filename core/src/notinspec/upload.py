"""An uploaded inputs archive (SPEC §11.1) -> one demo run, like `notinspec demo --no-claims`.

The archive is untrusted (SPEC §11): it is unpacked with limits into a temporary folder, read,
and only the run's artifacts stay in `runs_dir/<run id>/`.

shortcut: a run folder on disk instead of Postgres, like `notinspec demo`
(docs/plans/demo-cli-web.md); the API lists only folders that have run.json.
"""

import gzip
import json
import logging
import os
import re
import shutil
import tarfile
import tempfile
import zlib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Literal

from notinspec.adapters.canonical import canonical_json
from notinspec.adapters.openapi import SpecLoadError
from notinspec.config import ConfigError, load_config
from notinspec.demo import build_demo_run
from notinspec.ingestion import ingest
from notinspec.report import NOT_EVALUATED, build_results, write_artifacts
from notinspec.sphinx import SphinxInputError

__all__ = [
    "CONFIG_NAME",
    "MAX_MEMBERS",
    "MAX_MEMBER_BYTES",
    "MAX_TOTAL_BYTES",
    "ArchiveError",
    "UploadResult",
    "extract_archive",
    "process_upload",
]

log = logging.getLogger(__name__)

CONFIG_NAME = "notinspec.yaml"  # the config's name in the archive (`notinspec pack`, PR #43)

# What one archive may unpack to. The upload body is at most 25 MB (SPEC §11.1), but gzip
# shrinks text and XML 10x or more, so a valid archive can unpack to far more than it weighs,
# and a crafted one (a gzip bomb) to gigabytes. Big real inputs: GitHub's OpenAPI spec is
# about 12 MB, the committed Sphinx XML of urllib3, trio and hydra-zen a few MB each.
MAX_TOTAL_BYTES = 250 * 1024 * 1024  # all files together
MAX_MEMBERS = 20_000  # files and folders
MAX_MEMBER_BYTES = 50 * 1024 * 1024  # one file
# Headers, PAX records and padding come on top of the file data. Decompression stops past
# this, so even a header that claims gigabytes is never read into memory.
_MAX_STREAM_BYTES = MAX_TOTAL_BYTES + MAX_MEMBERS * 4096

# the folder the inputs go to when the caller gives no project: fixed, so the default project
# (the config folder's name) and with it every chunk ID stay the same from run to run
_DEFAULT_FOLDER = "upload"
_NAME = re.compile(r"[A-Za-z0-9_.-]{1,100}")  # GitHub repo names; the API's run ID rule
_COMMIT = re.compile(r"[0-9a-f]{40}")

_MB = 1024 * 1024
_PACK = "write it with `notinspec pack`"


class ArchiveError(ValueError):
    """The uploaded archive cannot be used; the message is meant for the repo owner."""


@dataclass(frozen=True)
class UploadResult:
    """How processing one upload ended: what the run's status needs (SPEC §11.1)."""

    run_id: str
    status: Literal["done", "error"]
    error_kind: Literal["input", "internal"] | None  # input: the repo owner can fix it
    error: str | None
    verdict: Literal["pass", "fail"] | None  # always None: no evaluation exists yet
    comment_md: str  # the PR comment without our marker


def extract_archive(archive: Path, dest: Path) -> tuple[str, ...]:
    """Unpack an inputs archive into `dest` (new or empty); return its file names, sorted.

    Every member is checked before it is written: regular files and folders only, no absolute
    paths or `..`, within the size and count limits. On `ArchiveError` `dest` may hold part of
    the archive; the caller removes it.
    """
    dest.mkdir(parents=True, exist_ok=True)
    if any(dest.iterdir()):
        raise ValueError(f"destination is not empty: {dest}")
    members = _Members()
    try:
        # stream mode: members are checked and written one by one, never all read first
        with _LimitedGzip(archive) as raw, tarfile.open(fileobj=raw, mode="r|") as tar:
            for member in tar:
                if members.add(member):
                    # the data filter checks paths again: defence in depth, not the main check
                    tar.extract(member, dest, filter="data")
    except tarfile.FilterError as error:
        name = error.tarinfo.name
        raise ArchiveError(f"inputs archive: {name}: rejected ({type(error).__name__})") from error
    except (tarfile.TarError, EOFError, gzip.BadGzipFile, zlib.error) as error:
        raise ArchiveError(f"inputs archive is not a valid tar.gz ({_PACK}): {error}") from error
    if CONFIG_NAME not in members.files:
        raise ArchiveError(
            f"inputs archive has no {CONFIG_NAME} at its root ({_PACK}, which stores the config "
            f"under that name)"
        )
    return tuple(sorted(members.files))


class _LimitedGzip(gzip.GzipFile):
    """Decompresses at most `_MAX_STREAM_BYTES`; more raises `ArchiveError`."""

    def __init__(self, path: Path) -> None:
        super().__init__(path, "rb")
        self._read = 0

    def read(self, size: int | None = -1) -> bytes:
        data = super().read(size)
        self._read += len(data)
        if self._read > _MAX_STREAM_BYTES:
            raise ArchiveError(_too_big("all files together are", MAX_TOTAL_BYTES))
        return data


class _Members:
    """The checks on each member, before it is written."""

    def __init__(self) -> None:
        self.files: set[str] = set()
        self._folders: set[str] = set()
        self._count = 0
        self._total = 0

    def add(self, member: tarfile.TarInfo) -> bool:
        """False for a member with nothing to write (the root folder `.`)."""
        self._count += 1
        if self._count > MAX_MEMBERS:
            raise ArchiveError(f"inputs archive has more than {MAX_MEMBERS} files and folders")
        name = member.name
        if not (member.isdir() or (member.isreg() and not member.issparse())):
            raise ArchiveError(
                f"inputs archive: {name} is a {_kind(member)}; only regular files are allowed "
                f"({_PACK}, which never stores links)"
            )
        path = PurePosixPath(name)
        if (
            "\\" in name
            or "\0" in name
            or path.is_absolute()
            or PureWindowsPath(name).drive
            or ".." in path.parts
        ):
            raise ArchiveError(
                f"inputs archive: {name}: paths must be relative and stay inside the archive"
            )
        if not path.parts:
            return False
        key = path.as_posix()
        parents = {p.as_posix() for p in path.parents if p.parts}
        if key in self.files:
            raise ArchiveError(f"inputs archive: {key} appears twice")
        if member.isreg() and key in self._folders:
            raise ArchiveError(f"inputs archive: {key} is both a file and a folder")
        if clash := sorted(parents & self.files):
            raise ArchiveError(f"inputs archive: {clash[0]} is both a file and a folder")
        self._folders |= parents
        if member.isdir():
            self._folders.add(key)
            return True
        if member.size > MAX_MEMBER_BYTES:
            raise ArchiveError(_too_big(f"{key} is", MAX_MEMBER_BYTES))
        self._total += member.size
        if self._total > MAX_TOTAL_BYTES:
            raise ArchiveError(_too_big("all files together are", MAX_TOTAL_BYTES))
        self.files.add(key)
        return True


def _kind(member: tarfile.TarInfo) -> str:
    if member.issym():
        return "symbolic link"
    if member.islnk():
        return "hard link"
    if member.ischr() or member.isblk():
        return "device"
    if member.isfifo():
        return "FIFO"
    if member.issparse():
        return "sparse file"
    return f"special member (tar type {member.type!r})"


def _too_big(what: str, limit: int) -> str:
    size = f"{limit // _MB} MB" if limit % _MB == 0 else f"{limit} bytes"
    return f"inputs archive: {what} larger than {size} unpacked"


# Errors caused by the uploaded inputs; the repo owner can fix them. Anything else is ours.
_INPUT_ERRORS: tuple[type[Exception], ...] = (
    ArchiveError,  # extract_archive: format, limits, links, paths, no config
    tarfile.TarError,  # extract_archive wraps these; kept in case one escapes
    ConfigError,  # load_config, and ingest: missing inputs, bad paths, Sphinx XML problems
    SphinxInputError,  # ingest wraps it into ConfigError; kept in case one escapes
    SpecLoadError,  # ingest: OpenAPI spec not parseable, not a mapping, or not 3.x
)
_INTERNAL = "internal error in NOT-IN-SPEC, not caused by your inputs"


def process_upload(
    archive: Path,
    runs_dir: Path,
    run_id: str,
    *,
    project: str | None = None,
    commit: str | None = None,
    web_url: str | None = None,
) -> UploadResult:
    """Unpack, ingest and write `runs_dir/<run_id>/` with run.json last, as `notinspec demo
    --no-claims` does. No claims, NLI, LLM or DB.

    From the OIDC token (SPEC §11): `project` is the repo name, the default of the config's
    `project:`, so breadcrumbs never contain the temporary folder's random name; `commit` is
    the token's `sha` (default: NOTINSPEC_COMMIT, else all zeros). Problems in the inputs and
    our own failures come back as an error result, with no run folder left behind. Raises only
    for a bad `run_id`, `project` or `commit` and for a run folder that already exists.
    """
    for field, value in (("run_id", run_id), ("project", project)):
        if value is not None and (not _NAME.fullmatch(value) or value in (".", "..")):
            raise ValueError(f"{field} must match {_NAME.pattern} and not be . or ..: {value!r}")
    if project is not None and project.lower() == ".git":
        raise ValueError("project must not be .git")
    if commit is not None and not _COMMIT.fullmatch(commit):
        raise ValueError(f"commit must be a 40-character lowercase SHA: {commit!r}")
    out = runs_dir / run_id
    out.mkdir(parents=True)  # FileExistsError: another run's folder is never replaced
    workdir = tempfile.TemporaryDirectory(prefix="notinspec-upload-")
    root = Path(workdir.name) / (project or _DEFAULT_FOLDER)
    try:
        with workdir:
            counts = _run(archive, root, out, run_id, commit)
    except _INPUT_ERRORS as error:
        shutil.rmtree(out, ignore_errors=True)
        message = _relative(str(error), root)
        log.info("upload %s: input error: %s", run_id, message)
        return UploadResult(run_id, "error", "input", message, None, _failed(message))
    except Exception:
        shutil.rmtree(out, ignore_errors=True)
        log.exception("upload %s: internal error", run_id)
        message = f"{_INTERNAL} (run {run_id})"
        return UploadResult(run_id, "error", "internal", message, None, _failed(message))
    return UploadResult(run_id, "done", None, None, None, _comment(counts, web_url))


def _run(archive: Path, root: Path, out: Path, run_id: str, commit: str | None) -> dict[str, Any]:
    """`cli._demo` without claims; returns the ingestion counts of results.json."""
    extract_archive(archive, root)
    config = load_config(root / CONFIG_NAME)
    ingestion = ingest(config, output=out)
    # the folder above the inputs: without a commit, git must never read a .git from the archive
    results = build_results(ingestion, root.parent, commit=commit)
    write_artifacts(out, ingestion, results)
    run = build_demo_run(
        json.loads((out / "ingestion.json").read_bytes()),
        json.loads((out / "results.json").read_bytes()),
        None,
        run_id,
    )
    # last, and atomic: a run.json that exists is complete (the API lists only those)
    partial = out / "run.json.tmp"
    partial.write_bytes(canonical_json(run, pretty=True))
    os.replace(partial, out / "run.json")
    counts: dict[str, Any] = results["ingestion"]
    return counts


def _relative(message: str, root: Path) -> str:
    """Server paths out of a message: `<tmp>/<project>/docs/a.md` -> `docs/a.md`."""
    for base in sorted({str(root), str(root.resolve())}, key=len, reverse=True):
        message = message.replace(base + os.sep, "").replace(base, ".")
    return message


def _comment(counts: dict[str, Any], web_url: str | None) -> str:
    """Counts only: never an averaged level or one overall score (AGENTS.md)."""
    lines = [
        "**NOT-IN-SPEC: inputs read, no verdict yet.**",
        "",
        f"{counts['files']} files, {counts['chunks']} chunks, {counts['symbols']} symbols, "
        f"{counts['changes']} changes, {counts['conflicts']} conflicts between sources.",
    ]
    if counts["warnings"]:
        lines.append(f"{len(counts['warnings'])} warnings, listed in the run.")
    lines += ["", NOT_EVALUATED]
    if web_url:
        lines += ["", f"[Full results]({web_url})"]
    return "\n".join(lines) + "\n"


def _failed(message: str) -> str:
    return f"**NOT-IN-SPEC: the run failed.**\n\n{message}\n"
