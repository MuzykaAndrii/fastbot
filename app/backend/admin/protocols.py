from typing import Any, Protocol

from fastapi import (
    Request,
    Response,
)


class AuthServiceProtocol(Protocol):
    def login_user(self, response: Response, login_data: Any) -> Any: ...
    def get_user_from_token(self, token: str) -> Any: ...
    def logout_user(self, request: Request) -> Any: ...