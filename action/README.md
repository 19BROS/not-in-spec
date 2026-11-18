# NOT-IN-SPEC GitHub Action

Tests how well LLMs can use your software from its documentation, on every PR that changes the docs ([SPEC §11](../docs/SPEC.md#11-github-action)).

The Action is a **thin client of our service**. It computes nothing and needs no model key. It packs your docs, uploads them with a GitHub OIDC token, waits for the run, and then writes one PR comment and the status check.

> **Not live yet.** Our upload API ([SPEC §11.1](../docs/SPEC.md#111-upload-api)) is still being built, and CI tests this Action against [`stub.py`](stub.py). Don't tag a release until the API is deployed: `@v0` still points to the old mock Action.

## Usage

Your repo must be **public** and **registered** as a project with us: its repository ID, default branch and workflow path. Add `notinspec.yaml` ([SPEC §2.3](../docs/SPEC.md#23-what-the-tool-needs-from-the-user), paths are relative to it) and this workflow:

```yaml
# .github/workflows/notinspec.yml  (this path is registered with your project)
on:
  pull_request:
    types: [opened, synchronize, reopened, closed] # closed: drops the PR's candidate tests
  push:
    branches: [main] # main runs: the baseline for later PRs
  workflow_dispatch: # the first main run of a new project

concurrency:
  group: notinspec-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  # runs your project's code (conf.py, autodoc imports), so it gets no secrets and no OIDC token
  build:
    if: github.event.action != 'closed'
    runs-on: ubuntu-latest
    permissions: { contents: read }
    steps:
      - uses: actions/checkout@v7
      - run: |
          python3 -m venv .venv && . .venv/bin/activate
          pip install -e . -r docs/requirements.txt   # whatever your docs build needs
          sphinx-build -b xml docs build/xml
          { sphinx-build --version; python --version; pip freeze; } > build/xml/build-env.txt
      # only with an OpenAPI spec: one file without external $refs (SPEC §11)
      - run: npx --yes @redocly/cli@2 bundle openapi.yaml -o build/openapi.yaml
      - uses: actions/upload-artifact@v7
        with: { name: notinspec-inputs, path: build/ }

  upload:
    needs: build
    # also on closed, when build is skipped
    if: ${{ !cancelled() && (needs.build.result == 'success' || github.event.action == 'closed') }}
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write # the OIDC token proves to us which repo and workflow sent the docs
      pull-requests: write # the PR comment
    steps:
      - uses: actions/checkout@v7
        with: { fetch-depth: 2 } # the merge commit's first parent finds the baseline
      - if: github.event.action != 'closed'
        uses: actions/download-artifact@v7
        with: { name: notinspec-inputs, path: build/ }
      - uses: 19BROS/not-in-spec/action@v0
```

```yaml
# notinspec.yaml
project: "mylib"               # root of every breadcrumb; default: the repo name
docs:
  sphinx_xml: "build/xml/"     # from the build job
  paths: ["README.md"]         # Markdown outside Sphinx, optional
  openapi: "build/openapi.yaml"  # bundled in the build job, optional
```

### Sphinx docs

> **Sphinx 9.x only.** The reader reads XML built by Sphinx 9 and checks the first line of `build-env.txt` (`sphinx-build 9.1.0`). Without `build-env.txt`, or with another Sphinx major version, the upload fails. Other versions are future work ([SPEC §16.3](../docs/SPEC.md#163-future-development)).

- **We never build Sphinx** ([SPEC §1.1](../docs/SPEC.md#11-what-we-are-not-building)). `sphinx-build` runs your project's code, so it runs in your `build` job. That job has no secrets and no OIDC token. It is a separate VM, so build code cannot reach the token of the `upload` job.
- `build-env.txt` is **required**, and the output of `sphinx-build --version` must be its first line. Autodoc output depends on the Sphinx version, the extensions and the installed library, so the same docs commit can build to different XML ([SPEC §6.1](../docs/SPEC.md#61-reading-and-chunking)).
- Keep the `sphinx-build` command your project already uses (extensions, `-D` options) and change only the builder to `xml`.

## What it does

1. **Skips** fork PRs, which get no OIDC token, with a warning. It also skips merged PRs on `closed`, because the next main run takes over their candidates.
2. **Closed PR:** sends a `closed` event and stops. A closed PR has no build and no comment.
3. **Packs** the inputs with `notinspec pack` from `core/` at the Action's own ref. The server selects inputs with the same code, so both sides always agree on what the inputs are. The archive is uploaded as an artifact with the run's status.
4. **Uploads** the archive to `POST /api/uploads` with an OIDC token whose audience is `server-url`. On a PR it also sends the head commit and the merge commit's first parent.
5. **Polls** the run every 15 s, without a token, because results are public.
6. **Comments:** writes **one** comment per PR (found by `<!-- notinspec -->`) and updates it on every push. On `push` and `workflow_dispatch` the result goes to the job summary.
7. **Fails the job**, which is the status check, as the table below shows.

| What happened | Job | Comment |
|---|---|---|
| verdict `pass` | ✓ | the run's comment |
| verdict `fail` | ✗ | the run's comment |
| run `error` (bad inputs) or a bad setup (config, no `id-token: write`, upload rejected with `4xx`) | ✗ | the error |
| our service is down, answers `5xx`, or the run takes longer than `timeout-minutes` | ✓ with a warning | "no result" |

An outage on our side never blocks your merges.

## Inputs and outputs

| Input | Default | |
|---|---|---|
| `config` | `notinspec.yaml` | path to the config |
| `server-url` | `https://147-175-151-17.sslip.io` | our service. It is also the OIDC audience, so it must match what we expect |
| `timeout-minutes` | `60` | how long to wait for the run |
| `github-token` | `github.token` | for the PR comment |

Outputs: `verdict` (`pass`, `fail`, or empty when there is no result) and `run-url`.

## Development

- [`client.sh`](client.sh) holds the logic, and [`action.yml`](action.yml) wires it into the job.
- [`stub.py`](stub.py) fakes the upload API (standard library only). It does not check the token. A run is `done` on the second poll, and its verdict is `fail` when an input contains `<!-- notinspec-mock: fail -->`.
- The CI job `action` in [ci.yml](../.github/workflows/ci.yml) runs the Action against the stub and checks the archive and the exit codes. Its last step shows how to run `client.sh` without the Action.

## Releases

1. Tag a commit on `main` with `vX.Y.Z` and push the tag.
2. The [release workflow](../.github/workflows/release.yml) moves `vX` to that commit.

The Action has no image of its own: it runs `core/` from the same commit, so `@vX.Y.Z` always runs the code of its own release.
