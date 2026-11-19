"""The upload archive the Action sends to our service (SPEC section 11.1).

The client selects inputs with the same `plan_ingestion` the server runs on the unpacked
archive, so both sides always agree on what the inputs are.
"""

import gzip
import io
import tarfile
from pathlib import Path

from notinspec.config import ConfigError, load_config
from notinspec.ingestion import plan_ingestion

CONFIG_NAME = "notinspec.yaml"  # the config's name inside the archive, whatever it is in the repo
_SPHINX_FILES = ("*.xml", "build-env.txt")


def pack_inputs(config_path: Path, archive: Path) -> tuple[str, ...]:
    """Write `archive` (tar.gz) and return its paths; the same inputs give the same bytes."""
    config = load_config(config_path)
    target = archive.resolve()
    # written next to the target and renamed at the end, so a failure never touches `archive`;
    # as the output it is never an input
    partial = target.with_name(f".{target.name}.partial")
    partial.unlink(missing_ok=True)
    plan, _ = plan_ingestion(config, output=partial)
    files: dict[str, Path] = {}
    for item in plan:
        if item.kind != "sphinx":
            files[item.source] = item.path  # resolved and checked by plan_ingestion
            continue
        # only what the Sphinx reader reads, not images or objects.inv
        for path in (p for pattern in _SPHINX_FILES for p in item.path.rglob(pattern)):
            resolved = path.resolve()
            # a link pointing out of the config folder must never ship that file
            if not resolved.is_relative_to(config.root) or not resolved.is_file():
                raise ConfigError(f"input is not a file inside the config directory: {path}")
            files[path.relative_to(config.root).as_posix()] = resolved
    if CONFIG_NAME in files:
        raise ConfigError(f"an input must not be {CONFIG_NAME} in the config folder")
    files[CONFIG_NAME] = config_path.resolve()
    if target in files.values():
        raise ConfigError(f"the archive must not be the config or an input: {archive}")

    # mtime 0 and owner 0 (TarInfo defaults), sorted names: no build-specific bytes
    try:
        with (
            partial.open("wb") as raw,
            gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as compressed,
            tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as tar,
        ):
            for name in sorted(files):
                data = files[name].read_bytes()
                info = tarfile.TarInfo(name)
                info.size = len(data)
                info.mode = 0o644
                tar.addfile(info, io.BytesIO(data))
        partial.replace(target)
    finally:
        partial.unlink(missing_ok=True)
    return tuple(sorted(files))
