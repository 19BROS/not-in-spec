# build context: repo root (uv workspace)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
# HF_HOME: the NLI model lives on the hf-models volume, fetched once by the deploy
# (`python -m notinspec.nli fetch`, docs/DEPLOY.md). HF_HUB_OFFLINE: a run never downloads it.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1 PATH="/app/.venv/bin:$PATH" \
    HF_HOME=/models HF_HUB_OFFLINE=1
# dependencies first (torch CPU is ~700 MB), so a code change does not reinstall them
COPY pyproject.toml uv.lock ./
COPY core/pyproject.toml core/
COPY api/pyproject.toml api/
COPY worker/pyproject.toml worker/
RUN uv sync --locked --no-dev --package notinspec-worker --extra nli --no-install-workspace
COPY . .
# /models and /runs owned by app: a named volume copies this owner on first use
RUN uv sync --locked --no-dev --package notinspec-worker --extra nli && useradd --system app \
    && mkdir /models /runs && chown app /models /runs
USER app
CMD ["notinspec-worker"]
