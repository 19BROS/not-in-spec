"""GitHub Actions OIDC verification and project authorization (SPEC §11).

Signing keys come only from GitHub's fixed JWKS endpoint. Neither the token header nor
request URLs choose a key server. Tokens are verified before any claims are used.
"""

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

ISSUER = "https://token.actions.githubusercontent.com"
AUDIENCE = "notinspec"
JWKS_URL = f"{ISSUER}/.well-known/jwks"
_SHA = re.compile(r"[0-9a-f]{40}")
_PULL = re.compile(r"refs/pull/([1-9][0-9]*)/merge")


class IdentityError(ValueError):
    """An invalid or expired token; HTTP 401."""


class IdentityUnavailable(RuntimeError):
    """GitHub's keys could not be read; a service error, never a setup error."""


class ForbiddenUpload(ValueError):
    """A verified workflow is not authorized for this project; HTTP 403."""


@dataclass(frozen=True)
class WorkflowIdentity:
    repository_id: int
    github_run_id: int
    github_run_attempt: int
    event: str
    ref: str
    sha: str
    workflow_ref: str
    pr_number: int | None
    claims: dict[str, Any]


class GithubOidc:
    def __init__(self, key: Callable[[str], Any] | None = None) -> None:
        import jwt

        client = jwt.PyJWKClient(JWKS_URL, timeout=10)
        self._key = key or (lambda token: client.get_signing_key_from_jwt(token).key)

    def verify(self, token: str) -> WorkflowIdentity:
        import jwt

        if not token or len(token) > 16_384:
            raise IdentityError("missing or invalid GitHub OIDC token")
        try:
            claims = jwt.decode(
                token,
                self._key(token),
                algorithms=["RS256"],
                issuer=ISSUER,
                audience=AUDIENCE,
                options={"require": ["exp", "iat", "nbf", "iss", "aud", "sub"]},
            )
            for field in ("event_name", "ref", "sha", "workflow_ref", "repository_visibility"):
                if not isinstance(claims.get(field), str) or not claims[field]:
                    raise IdentityError(f"GitHub OIDC token has no valid {field}")
            if not _SHA.fullmatch(claims["sha"]):
                raise IdentityError("GitHub OIDC token has no valid sha")
            event, ref = claims["event_name"], claims["ref"]
            pull = _PULL.fullmatch(ref)
            if event == "pull_request" and pull is None:
                raise IdentityError("pull_request token must identify refs/pull/N/merge")
            # Store only the claims needed for audit, never the bearer token itself.
            audit = {
                name: claims[name]
                for name in (
                    "iss",
                    "aud",
                    "sub",
                    "exp",
                    "iat",
                    "nbf",
                    "repository_id",
                    "run_id",
                    "run_attempt",
                    "event_name",
                    "ref",
                    "sha",
                    "workflow_ref",
                    "repository_visibility",
                )
            }
            return WorkflowIdentity(
                _positive_id(claims, "repository_id"),
                _positive_id(claims, "run_id"),
                _positive_id(claims, "run_attempt"),
                event,
                ref,
                claims["sha"],
                claims["workflow_ref"],
                int(pull[1]) if pull else None,
                audit,
            )
        except jwt.PyJWKClientConnectionError as error:
            raise IdentityUnavailable("GitHub signing keys are temporarily unavailable") from error
        except (jwt.PyJWTError, KeyError, TypeError, ValueError) as error:
            raise IdentityError("invalid or expired GitHub OIDC token") from error


def _positive_id(claims: Mapping[str, Any], name: str) -> int:
    value = claims.get(name)
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise IdentityError(f"invalid {name}")
    text = str(value)
    if not re.fullmatch(r"[1-9][0-9]{0,18}", text) or int(text) > 2**63 - 1:
        raise IdentityError(f"invalid {name}")
    result = int(text)
    if name == "run_attempt" and result > 2**31 - 1:
        raise IdentityError(f"invalid {name}")
    return result


def authorize(
    identity: WorkflowIdentity,
    *,
    repository_id: int | None,
    default_branch: str | None,
    workflow_path: str | None,
) -> None:
    """The registered numeric repository ID and workflow path define the project boundary."""
    if identity.repository_id != repository_id:
        raise ForbiddenUpload("repository is not registered")
    if identity.claims["repository_visibility"] != "public":
        raise ForbiddenUpload("only public repositories are supported")
    if identity.event not in ("pull_request", "push", "workflow_dispatch"):
        raise ForbiddenUpload("this workflow event is not allowed")
    path, separator, ref = identity.workflow_ref.partition("@")
    if not separator or not ref or not workflow_path or path != workflow_path:
        raise ForbiddenUpload("workflow path does not match the registered workflow")
    if identity.event != "pull_request" and identity.ref != f"refs/heads/{default_branch}":
        raise ForbiddenUpload("push and workflow_dispatch must use the registered default branch")
