# build context: repo root (uv workspace)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1 PATH="/app/.venv/bin:$PATH"
COPY . .
RUN uv sync --locked --no-dev --package notinspec-api && useradd --system app
USER app
EXPOSE 8000
HEALTHCHECK CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
CMD ["uvicorn", "notinspec_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
