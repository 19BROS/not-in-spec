# build context: repo root (uv workspace)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1 PATH="/app/.venv/bin:$PATH"
COPY . .
RUN uv sync --locked --no-dev --package notinspec-worker && useradd --system app
USER app
CMD ["notinspec-worker"]
