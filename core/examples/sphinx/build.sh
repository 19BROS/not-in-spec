#!/usr/bin/env bash
# Build the Sphinx XML of one example library in a throwaway container.
#
#   core/examples/sphinx/build.sh <lib> [<out-dir>] [<checkout-path-in-container>]
#
# sphinx-build runs the library's code (conf.py, autodoc imports, pip build hooks), so it
# runs only inside the container: no secrets, and the only host mount is the output folder
# (SPEC §1.1). Each library is built with its OWN pinned docs dependencies from the release
# tag below; we never add extensions. MVP supports Sphinx 9.x only.
#
# Output: <out-dir>/xml/*.xml + xml/build-env.txt, <out-dir>/build-warnings.txt.
# Determinism check: build twice with different checkout paths and diff (see README.md).
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
lib=$1
out=${2:-$here/$lib}
src=${3:-/src}
image=python:3.12.15-slim  # Sphinx 9.2 needs Python 3.13; all three pin 9.1.x for 3.12

case $lib in
  urllib3)
    repo=https://github.com/urllib3/urllib3 ref=2.8.0
    install='pip install -q uv==0.9.* && UV_PROJECT_ENVIRONMENT=/venv uv sync -q --frozen --group docs --extra socks --extra brotli --extra zstd && . /venv/bin/activate'
    freeze='uv pip freeze --python /venv/bin/python'
    docs=docs ;;
  trio)
    repo=https://github.com/python-trio/trio ref=v0.35.0
    install='pip install -q -r docs-requirements.txt && pip install -q .'
    freeze='pip freeze'
    docs=docs/source ;;
  hydra-zen)
    repo=https://github.com/mit-ll-responsible-ai/hydra-zen ref=v0.17.2
    install='pip install -q . && pip install -q -r docs/requirements.txt'
    freeze='pip freeze'
    docs=docs/source ;;
  *) echo "unknown library: $lib (add a case above)" >&2; exit 2 ;;
esac

rm -rf "$out/xml"
mkdir -p "$out"
MSYS_NO_PATHCONV=1 docker run --rm -v "$out:/out" "$image" bash -c "
  set -euo pipefail
  apt-get update -qq && apt-get install -y -qq git make >/dev/null
  git clone -q --depth 1 --branch $ref $repo $src && cd $src
  commit=\$(git rev-parse HEAD)
  $install
  sphinx-build -q -b xml -d /tmp/doctrees $docs /out/xml 2> /tmp/warnings.txt \
    || { cat /tmp/warnings.txt; exit 1; }
  sed -e 's#^$src/#<checkout>/#' /tmp/warnings.txt > /out/build-warnings.txt
  { sphinx-build --version; python --version; echo \"source $repo @ $ref\";
    echo \"commit \$commit\"; $freeze; } > /out/xml/build-env.txt
"
head -1 "$out/xml/build-env.txt"
