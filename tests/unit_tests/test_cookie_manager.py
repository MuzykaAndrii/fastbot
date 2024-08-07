import pytest
from unittest.mock import MagicMock
from fastapi import Request, Response

from app.backend.cookie.cookie import FastAPICookieManager


COOKIE_NAME = "test_cookie"
COOKIE_VALUE = "test_value"


@pytest.fixture
def response_with_mocks() -> Response:
    response = MagicMock(spec=Response)
    response.cookies = {}
    def mock_set_cookie(name, value, httponly, samesite, secure):
        response.cookies[name] = value
    def mock_delete_cookie(name):
        if name in response.cookies:
            del response.cookies[name]
    response.set_cookie = mock_set_cookie
    response.delete_cookie = mock_delete_cookie
    return response


@pytest.fixture
def req() -> Request:
    return MagicMock(Request)


@pytest.fixture
def cookie_manager() -> FastAPICookieManager:
    return FastAPICookieManager(COOKIE_NAME)


def test_set_cookie(response_with_mocks: Response, cookie_manager: FastAPICookieManager) -> None:
    response = cookie_manager.set_cookie(response_with_mocks, COOKIE_VALUE)
    assert COOKIE_NAME in response.cookies
    assert response.cookies[COOKIE_NAME] == COOKIE_VALUE


def test_get_cookie(req: Request, cookie_manager: FastAPICookieManager) -> None:
    req.cookies = {COOKIE_NAME: COOKIE_VALUE}
    cookie_value = cookie_manager.get_cookie(req)
    assert cookie_value == COOKIE_VALUE


def test_delete_cookie(response_with_mocks: Response, cookie_manager: FastAPICookieManager) -> None:
    response = cookie_manager.set_cookie(response_with_mocks, COOKIE_VALUE)
    response = cookie_manager.delete_cookie(response)
    assert COOKIE_NAME not in response.cookies
