from fastapi import FastAPI

from notinspec import __version__

app = FastAPI(title="NOT-IN-SPEC", version=__version__)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
