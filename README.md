# NOT-IN-SPEC

Measures how reliably language models answer questions about a specific API, and how that changes over time. Team project 2026/2027, no. 8.

- What we build and why: [docs/SPEC.md](docs/SPEC.md) (start here), [docs/FAQ.md](docs/FAQ.md), [docs/INSPIRATION.md](docs/INSPIRATION.md), [docs/assignment.md](docs/assignment.md)
- How to work in the repo (layout, commands, rules, git worktrees): [AGENTS.md](AGENTS.md)
- How production runs, backups, rollback, VM access: [docs/DEPLOY.md](docs/DEPLOY.md)

## Quick start

```sh
uv sync --all-packages && uv run pytest
cd web && npm ci && npm run dev
```

Full stack: `cp deploy/.env.example deploy/.env && docker compose -f deploy/docker-compose.yml up --build`, then open http://localhost:8080.

## CI/CD

| Workflow | When | What |
|---|---|---|
| `ci.yml` | every PR and push to `main` | ruff, mypy, pytest (coverage gate on core), oxlint + web build, Compose smoke test; on `main` also pushes images to GHCR |
| `deploy.yml` | after CI succeeds on a push to `main` | self-hosted runner on the faculty VM pulls images and runs `docker compose up -d` |

### One-time GitHub setup (repo admin)

1. Create the repo under the team org (public), push `main`.
2. **Settings → Branches:** protect `main` by requiring a PR and the `python`, `web` and `compose` checks to pass.
3. **Settings → Actions → General → Fork pull request workflows:** require approval for all external contributors.
4. **Settings → Environments:** create `production` and limit deployment branches to `main` (optionally add required reviewers).
5. **VM:** install Docker, register a self-hosted runner for this repo with the extra label **`notinspec-deploy`**, and create `/opt/notinspec/.env` from [deploy/.env.example](deploy/.env.example) with `IMAGE_OWNER=<org in lowercase>`.
6. Until step 5 is done, deploy runs sit queued. Disable `Deploy` in the Actions tab if that bothers you.

## License

[MIT](LICENSE)
