import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from notinspec.oidc import GithubOidc
from notinspec_api import hosted
from notinspec_api.main import app


@pytest.fixture(autouse=True)
def dependencies():
    yield
    app.dependency_overrides.clear()


def test_missing_and_invalid_bearer_tokens():
    app.dependency_overrides[hosted.verifier] = lambda: GithubOidc(lambda _: "unused")
    with TestClient(app) as client:
        for authorization in ("", "Basic abc", "Bearer invalid.token"):
            assert (
                client.post("/uploads", headers={"Authorization": authorization}).status_code == 401
            )


def test_disabled_service(monkeypatch):
    monkeypatch.delenv("NOTINSPEC_UPLOADS_ENABLED", raising=False)
    hosted.service.cache_clear()
    with TestClient(app) as client:
        assert client.get("/runs/anything").status_code == 503


def test_streamed_multipart_size_limit():
    test_app = FastAPI()
    test_app.add_middleware(hosted.UploadBodyLimit, limit=64)

    @test_app.post("/uploads")
    async def consume(request: Request):
        return {"size": len(await request.body())}

    with TestClient(test_app) as client:
        assert client.post("/uploads", content=b"a" * 64).status_code == 200
        # No Content-Length header: the streaming limit still applies.
        assert client.post("/uploads", content=iter([b"a" * 40, b"b" * 40])).status_code == 413
