#!/usr/bin/env bash
# Build the Sphinx reader's golden fixture three ways with Sphinx 9 (SPEC §13):
#
#   core/tests/fixtures/sphinx/build.sh     # → xml-napoleon/, xml-numpydoc/, xml-plain/
#
# napoleon: Google and NumPy docstrings → field lists (shapes A, B); numpydoc: NumPy → shape C,
# Google stays a definition list; plain: only reST `:param:` fields are fields.
# The project is our own tiny code, so this runs locally, no container. CI never runs it: the
# XML is committed. The checkout path in `source=` is rewritten to /src, so the files do not
# depend on where they were built (and hold no local paths).
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1  # autodoc imports fixturelib.py
here=$(cd "$(dirname "$0")" && pwd)
run=(uv run --isolated --no-project --python 3.12 --with sphinx==9.1.1 --with numpydoc==1.11.0
     --with myst-parser==5.2.0)
for style in napoleon numpydoc plain; do
  out=$here/xml-$style
  doctrees=$(mktemp -d)
  rm -rf "$out"
  FIXTURE_DOCSTRINGS=$style "${run[@]}" sphinx-build -q -E -b xml -d "$doctrees" \
    "$here/project/docs" "$out"
  rm -rf "$doctrees"
  "${run[@]}" python - "$out" "$here/project" <<'PY'
import importlib.metadata
import platform
import re
import sys
from pathlib import Path

import sphinx

out, project = Path(sys.argv[1]), Path(sys.argv[2]).resolve().as_posix().lower()


def relocate(match: re.Match[str]) -> str:
    value = match[2].replace("\\", "/")
    if value.lower().startswith(project):
        value = "/src" + value[len(project):]
    return f"{match[1]}{value}{match[3]}"


for path in sorted(out.rglob("*.xml")):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'(\ssource=")([^"]*)(")', relocate, text)
    path.write_text(text, encoding="utf-8", newline="\n")
pins = sorted(f"{d.metadata['Name']}=={d.version}" for d in importlib.metadata.distributions())
env = [f"sphinx-build {sphinx.__version__}", f"Python {platform.python_version()}", *pins]
(out / "build-env.txt").write_text("\n".join(env) + "\n", encoding="utf-8", newline="\n")
PY
  echo "$style: $(ls "$out"/*.xml | wc -l) documents"
done
