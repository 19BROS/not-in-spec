# Sphinx XML examples

Real Sphinx documentation built with `sphinx-build -b xml` (SPEC §6.1): input for the Sphinx
reader and the demo. **MVP supports Sphinx 9.x only**; other versions are future work.

| Library | Release | Sphinx | Docstrings | Field shape (SPEC §6.1) | Licence |
|---|---|---|---|---|---|
| `urllib3/` | 2.8.0 | 9.1.0 | reST `:param:` | A, B | MIT |
| `trio/` | v0.35.0 | 9.1.1 | Google `Args:` via napoleon | A, B | MIT or Apache-2.0 |
| `hydra-zen/` | v0.17.2 | 9.1.0 | NumPy via numpydoc | C | MIT |

Each folder holds `xml/` (the build output plus `build-env.txt`), `build-warnings.txt` (the
project's own Sphinx warnings), the library's licence and a `notinspec.yaml`.
The XML is the libraries' documentation, redistributed under their licences.

## Rebuilding

Needs Docker. The build runs the library's code, so it runs only in a container with no
secrets (SPEC §1.1). Each library uses its own pinned docs dependencies from its release tag.

```sh
core/examples/sphinx/build.sh trio            # → core/examples/sphinx/trio/xml/
```

Determinism check (done for all three on 2026-11-17): build twice from different checkout paths
and compare. The only difference is the absolute path in `source=` on `<document>` and on
`<literal_block>` from `literalinclude`; the reader normalizes it before hashing.

```sh
core/examples/sphinx/build.sh trio /tmp/trio-a /src
core/examples/sphinx/build.sh trio /tmp/trio-b /home/other/checkout
sed -i 's#/home/other/checkout#/src#g' /tmp/trio-b/xml/*.xml
diff -r -x build-env.txt /tmp/trio-a/xml /tmp/trio-b/xml   # no output expected
```

`'at 0x…'` addresses found in the XML (8) are static text in hand-written doctest output, not
autodoc values, so they are the same in every build.

## Adding a library

1. Add a `case` to `build.sh` with the release tag, its own docs install and the Sphinx source
   folder. Check that its lock or requirements pin Sphinx 9.x for Python 3.12.
2. Build, then look at what the reader will meet:
   `uv run python core/examples/sphinx/census.py core/examples/sphinx/<lib>/xml`
3. Copy the licence and add `notinspec.yaml`.
