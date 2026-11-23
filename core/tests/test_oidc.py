"""Real RSA signatures and authorization rules, with no calls to GitHub."""

import time
from dataclasses import replace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from notinspec.oidc import (
    AUDIENCE,
    ISSUER,
    ForbiddenUpload,
    GithubOidc,
    IdentityError,
    IdentityUnavailable,
    authorize,
)


@pytest.fixture(scope="module")
def key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture
def claims():
    now = int(time.time())
    return dict(
        iss=ISSUER,
        aud=AUDIENCE,
        sub="repo:team/repo:pull_request",
        exp=now + 300,
        iat=now,
        nbf=now - 1,
        repository_id="123",
        run_id="456",
        run_attempt="1",
        event_name="pull_request",
        ref="refs/pull/7/merge",
        sha="a" * 40,
        workflow_ref="team/repo/.github/workflows/check.yml@refs/pull/7/merge",
        repository_visibility="public",
    )


def verify(key, claims):
    return GithubOidc(lambda _: key.public_key()).verify(jwt.encode(claims, key, algorithm="RS256"))


def allow(identity):
    authorize(
        identity,
        repository_id=123,
        default_branch="main",
        workflow_path="team/repo/.github/workflows/check.yml",
    )


def test_signature_and_identity(key, claims):
    identity = verify(key, claims)
    allow(identity)
    assert (identity.repository_id, identity.github_run_id, identity.pr_number) == (123, 456, 7)
    assert "token" not in identity.claims
    wrong = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with pytest.raises(IdentityError):
        GithubOidc(lambda _: wrong.public_key()).verify(jwt.encode(claims, key, algorithm="RS256"))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("aud", "wrong"),
        ("iss", "https://evil.invalid"),
        ("exp", 1),
        ("nbf", 9999999999),
        ("sha", "../x"),
        ("repository_id", True),
        ("run_id", "0"),
        ("run_attempt", "2147483648"),
        ("ref", "refs/heads/main"),
    ],
)
def test_invalid_signed_claims(key, claims, field, value):
    claims[field] = value
    with pytest.raises(IdentityError):
        verify(key, claims)


def test_missing_and_unsigned(key, claims):
    del claims["repository_id"]
    with pytest.raises(IdentityError):
        verify(key, claims)
    with pytest.raises(IdentityError):
        GithubOidc(lambda _: key.public_key()).verify(jwt.encode(claims, "", algorithm="none"))


def test_key_service_outage():
    def unavailable(_):
        raise jwt.PyJWKClientConnectionError("offline")

    with pytest.raises(IdentityUnavailable):
        GithubOidc(unavailable).verify("a.b.c")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("repository_id", 124),
        ("event", "pull_request_target"),
        ("workflow_ref", "team/repo/.github/workflows/evil.yml@main"),
        ("claims", {"repository_visibility": "private"}),
    ],
)
def test_project_boundary(key, claims, field, value):
    with pytest.raises(ForbiddenUpload):
        allow(replace(verify(key, claims), **{field: value}))


def test_default_branch_only_for_non_pr(key, claims):
    claims.update(event_name="push", ref="refs/heads/main")
    allow(verify(key, claims))
    claims["ref"] = "refs/heads/feature"
    with pytest.raises(ForbiddenUpload):
        allow(verify(key, claims))
