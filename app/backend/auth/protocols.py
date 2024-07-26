from typing import Protocol

from fastapi import Request, Response


class UserProtocol(Protocol):
    id: int
    email: str
    password_hash: str | bytes


class UserServiceProtocol(Protocol):
    async def get_by_email(self, email: str) -> UserProtocol:
        pass

    async def get_by_id(self, id: int) -> UserProtocol:
        pass


class PasswordServiceProtocol(Protocol):
    def get_hash(self, password: str) -> bytes:
        pass

    def verify(self, raw_password: str, hashed_password: bytes) -> bool:
        pass


class CookieManagerProtocol(Protocol):
    def set_cookie(self, response_obj: Response, data: str) -> Response:
        pass

    def get_cookie(self, request: Request) -> str | None:
        pass

    def delete_cookie(self, response: Response) -> Response:
        pass