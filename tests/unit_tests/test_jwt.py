from typing import Any
from datetime import datetime, timedelta, UTC

import pytest
from jose import jwt

from app.backend.jwt.exceptions import JWTExpiredError, JwtMissingError, JwtNotValidError
from app.backend.jwt.jwt import JoseEncoder, Jwt, Token


SECRET_KEY = "testsecret"
ALGORITHM = "HS256"
LIFETIME_MINUTES = 5


@pytest.fixture
def encoder() -> JoseEncoder:
    return JoseEncoder(SECRET_KEY, ALGORITHM)


@pytest.fixture
def jwt_instance(encoder: JoseEncoder) -> Jwt:
    return Jwt(encoder, LIFETIME_MINUTES)


def create_token(sub: Any, lifetime_minutes: int) -> str:
    exp = datetime.now(UTC) + timedelta(minutes=lifetime_minutes)
    return jwt.encode({"sub": sub, "exp": exp.timestamp()}, SECRET_KEY, algorithm=ALGORITHM)


def test_encode(encoder: JoseEncoder) -> None:
    payload = {"sub": "test_subject", "exp": (datetime.now(UTC) + timedelta(minutes=5)).timestamp()}
    encoded = encoder.encode(payload)
    assert isinstance(encoded, str)


def test_decode(encoder: JoseEncoder) -> None:
    payload = {"sub": "test_subject", "exp": (datetime.now(UTC) + timedelta(minutes=5)).timestamp()}
    encoded = encoder.encode(payload)
    decoded = encoder.decode(encoded)
    assert decoded["sub"] == payload["sub"]
    assert decoded["exp"] == payload["exp"]


def test_decode_invalid_token(encoder: JoseEncoder) -> None:
    with pytest.raises(JwtNotValidError):
        encoder.decode("invalid.token.here")


def test_create_token(jwt_instance: Jwt) -> None:
    token = jwt_instance.create("test_subject")
    assert isinstance(token, str)


def test_read_token(jwt_instance: Jwt) -> None:
    encoded_token = create_token("test_subject", LIFETIME_MINUTES)
    token = jwt_instance.read(encoded_token)
    assert token.sub == "test_subject"
    assert isinstance(token.exp, float)


def test_read_expired_token(jwt_instance: Jwt) -> None:
    encoded_token = create_token("test_subject", 0)
    with pytest.raises(JWTExpiredError):
        jwt_instance.read(encoded_token)


def test_read_missing_token(jwt_instance: Jwt) -> None:
    with pytest.raises(JwtMissingError):
        jwt_instance.read("")


def test_token_is_expired() -> None:
    token = Token("test_subject", (datetime.now(UTC) - timedelta(minutes=1)).timestamp())
    assert token.is_expired


def test_token_is_not_expired() -> None:
    token = Token("test_subject", (datetime.now(UTC) + timedelta(minutes=1)).timestamp())
    assert not token.is_expired
