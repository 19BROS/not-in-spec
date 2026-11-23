"""HTTP adapter for core's hosted upload service (SPEC §11.1)."""

import os
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any

from anyio import to_thread
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.datastructures import UploadFile
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from notinspec.config import ConfigError
from notinspec.db import database_url, make_engine
from notinspec.db.hosted import (
    MAX_UPLOAD_BYTES,
    HostedService,
    ReplayConflict,
    UploadTooLarge,
    upload_meta,
)
from notinspec.oidc import (
    ForbiddenUpload,
    GithubOidc,
    IdentityError,
    IdentityUnavailable,
    WorkflowIdentity,
)
from notinspec.upload import ArchiveError

router = APIRouter()


@lru_cache
def service() -> HostedService:
    if os.environ.get("NOTINSPEC_UPLOADS_ENABLED") != "1":
        raise HTTPException(503, "uploads are disabled")
    return HostedService(
        make_engine(database_url()),
        Path(os.environ.get("NOTINSPEC_UPLOADS_DIR", "tmp/uploads")),
        Path(os.environ.get("NOTINSPEC_RUNS_DIR", "tmp/runs")),
        os.environ.get("NOTINSPEC_PUBLIC_URL", "https://147-175-151-17.sslip.io"),
    )


@lru_cache
def verifier() -> GithubOidc:
    return GithubOidc()


def _call(function: Callable[..., Any], *args: Any) -> Any:
    try:
        return function(*args)
    except IdentityError as error:
        raise HTTPException(401, str(error)) from error
    except ForbiddenUpload as error:
        raise HTTPException(403, str(error)) from error
    except ReplayConflict as error:
        raise HTTPException(409, str(error)) from error
    except UploadTooLarge as error:
        raise HTTPException(413, str(error)) from error
    except (ConfigError, ArchiveError) as error:
        raise HTTPException(422, str(error)) from error
    except (IdentityUnavailable, SQLAlchemyError) as error:
        raise HTTPException(503, "upload service is temporarily unavailable") from error


def identity(
    check: Annotated[GithubOidc, Depends(verifier)], authorization: str = Header("")
) -> WorkflowIdentity:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(401, "a GitHub OIDC bearer token is required")
    result: WorkflowIdentity = _call(check.verify, token)
    return result


@router.post("/uploads")
async def upload(
    request: Request,
    workflow: Annotated[WorkflowIdentity, Depends(identity)],
    hosted: Annotated[HostedService, Depends(service)],
) -> JSONResponse:
    async with request.form(max_files=2, max_fields=1, max_part_size=MAX_UPLOAD_BYTES) as form:
        if sorted(form.keys()) != ["archive", "meta"] or len(form.multi_items()) != 2:
            raise HTTPException(422, "send exactly archive and meta")
        archive, meta = form["archive"], form["meta"]
        if not isinstance(archive, UploadFile):
            raise HTTPException(422, "archive must be a tar.gz file")
        if isinstance(meta, UploadFile):
            meta_bytes = await meta.read(8193)
            if len(meta_bytes) > 8192:
                raise HTTPException(422, "meta is too large")
            try:
                meta = meta_bytes.decode("utf-8")
            except UnicodeError as error:
                raise HTTPException(422, "meta must be UTF-8 JSON") from error
        metadata = _call(upload_meta, meta)
        content = await archive.read(MAX_UPLOAD_BYTES + 1)
        result, created = await to_thread.run_sync(
            _call, hosted.accept, workflow, content, metadata
        )
    return JSONResponse(result, status_code=202 if created else 200)


@router.get("/runs/{run_id}")
def run_status(run_id: str, hosted: Annotated[HostedService, Depends(service)]) -> dict[str, Any]:
    result: dict[str, Any] | None = _call(hosted.status, run_id)
    if result is None:
        raise HTTPException(404, "run not found")
    return result


@router.post("/pr-closed", status_code=202)
def pr_closed(
    workflow: Annotated[WorkflowIdentity, Depends(identity)],
    hosted: Annotated[HostedService, Depends(service)],
) -> dict[str, str]:
    _call(hosted.close_pr, workflow)
    return {"status": "accepted"}


class UploadBodyLimit:
    """Limit streamed multipart bodies before Starlette spools files to disk."""

    def __init__(self, app: ASGIApp, limit: int = MAX_UPLOAD_BYTES + 65_536) -> None:
        self.app, self.limit = app, limit

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["path"] != "/uploads":
            await self.app(scope, receive, send)
            return
        total = 0

        async def limited_receive() -> Message:
            nonlocal total
            message = await receive()
            total += len(message.get("body", b""))
            if total > self.limit:
                raise UploadTooLarge("multipart upload exceeds the size limit")
            return message

        try:
            await self.app(scope, limited_receive, send)
        except UploadTooLarge as error:
            await JSONResponse({"detail": str(error)}, status_code=413)(scope, receive, send)
