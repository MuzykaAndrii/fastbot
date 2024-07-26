from typing import Protocol


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