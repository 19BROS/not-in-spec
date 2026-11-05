# NOT-IN-SPEC GitHub Action

Tests how well LLMs can use your software from its documentation, on every PR that changes the docs ([SPEC §11](../docs/SPEC.md#11-github-action)).

> **Mock.** The image runs [`mock.py`](mock.py): real inputs, outputs and exit codes, fake numbers. It is replaced by the real CLI from `core` without changing this interface.

## Usage

Add `notinspec.yaml` to your repo ([example](../deploy/fixtures/notinspec.yaml), paths are relative to it) and this workflow:

```yaml
# .github/workflows/notinspec.yml
on:
  pull_request:
    paths: ["docs/**", "openapi.yaml", "notinspec.yaml"]
  push:
    branches: [main]
    paths: ["docs/**", "openapi.yaml", "notinspec.yaml"]

permissions:
  contents: read
  pull-requests: write # PR comment

jobs:
  notinspec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with: { fetch-depth: 0 } # git history, to find the changed docs
      - uses: 19BROS/not-in-spec/action@v0
        with:
          api-key: ${{ secrets.LLM_API_KEY }}
          server-url: https://147-175-151-17.sslip.io # optional: send results to our server
          server-token: ${{ secrets.NOTINSPEC_TOKEN }}
```

## What it does

1. Skips pull requests from forks (they get no secrets) with a warning.
2. Runs the `notinspec-cli` image: `notinspec ci --config <config> --out notinspec-out`.
3. Uploads `notinspec-out/` as the artifact `notinspec-results`: `results.json`, `report.html`, `comment.md`.
4. On a PR, creates or updates **one** comment (found by `<!-- notinspec -->`).
5. If `server-url` is set, POSTs `results.json` to `<server-url>/api/runs` with the token. Only `https://` (or localhost). A failure is a warning, never a red PR.
6. Fails the job when the CLI exits non-zero, which is the PR's status check.

| Exit code | Meaning |
|---|---|
| 0 | pass |
| 1 | documentation change lowers usage (or a new finding), see the comment |
| 2 | bad config, or the CLI crashed |

To demo a red PR with the mock, add `<!-- notinspec-mock: fail -->` to a changed docs file.

## Inputs

| Input | Default | |
|---|---|---|
| `config` | `notinspec.yaml` | path to the config |
| `api-key`, `base-url` | – | model API (unused by the mock) |
| `server-url`, `server-token` | – | where to send results |
| `image` | `ghcr.io/19bros/notinspec-cli:<this release>` | |
| `github-token` | `github.token` | for the PR comment |

Output `verdict`: `pass` or `fail`.

## `results.json` (schema v0)

Example: [example-results.json](example-results.json). One row per **level × model × mode**, never averaged into one score. `baseline_passed` is the same row on `main`. `verdict` and `reasons` say why the check failed.

## Releases

1. In a PR, set the `image` default in [action.yml](action.yml) to `notinspec-cli:X.Y.Z` and merge it.
2. Tag that commit on `main` with `vX.Y.Z` and push the tag.
3. The [release workflow](../.github/workflows/release.yml) checks the pinned version, pushes `ghcr.io/19bros/notinspec-cli:X.Y.Z` and moves the git tag `vX`.

Pinning the exact image keeps `@vX.Y.Z` and its image together: an old `action.yml` never runs a newer CLI with other arguments.
