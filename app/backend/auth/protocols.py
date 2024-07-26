from typing import Protocol


class UserProtocol(Protocol):
    id: int
    email: str
    password_hash: str | bytes


class UserServiceProtocol(Protocol):
    def get_by_email(self, email: str) -> UserProtocol:
        pass

    def get_by_id(self, id: int) -> UserProtocol:
        pass