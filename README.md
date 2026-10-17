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

## License

[MIT](LICENSE)
