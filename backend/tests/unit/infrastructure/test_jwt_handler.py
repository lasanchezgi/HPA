from datetime import UTC, timedelta

import pytest

from src.domain.exceptions import InvalidCredentialsError
from src.infrastructure.security.jwt_handler import JWTHandler

SECRET = "test-secret-key"


@pytest.fixture
def handler():
    return JWTHandler(secret_key=SECRET, algorithm="HS256", expire_minutes=30)


def test_create_and_decode_token_returns_correct_subject(handler):
    token = handler.create_access_token(subject="user-123")
    payload = handler.decode_token(token)
    assert payload["sub"] == "user-123"


def test_expired_token_raises_exception():
    handler = JWTHandler(secret_key=SECRET, algorithm="HS256", expire_minutes=0)
    from datetime import datetime

    from jose import jwt as jose_jwt

    expire = datetime.now(UTC) + timedelta(seconds=-1)
    token = jose_jwt.encode({"sub": "u1", "exp": expire}, SECRET, algorithm="HS256")

    with pytest.raises(InvalidCredentialsError):
        handler.decode_token(token)


def test_invalid_token_raises_exception(handler):
    with pytest.raises(InvalidCredentialsError):
        handler.decode_token("not.a.valid.token")


def test_token_contains_expected_claims(handler):
    token = handler.create_access_token(subject="user-abc")
    payload = handler.decode_token(token)
    assert "sub" in payload
    assert "exp" in payload
    assert payload["sub"] == "user-abc"
