from typing import Any

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.users.dal import UserDAL
from app.backend.users.models import User


@pytest.fixture(scope="function")
async def user_dal(session: AsyncSession) -> UserDAL:
    return UserDAL(session)


@pytest.fixture(scope="session")
def mock_users_list() -> list[dict[str, Any]]:
    return [
        {"username": "user1", "email": "user1@example.com", "password_hash": b"pwd1", "is_superuser": False},
        {"username": "user2", "email": "user2@example.com", "password_hash": b"pwd2", "is_superuser": False},
        {"username": "user3", "email": "user3@example.com", "password_hash": b"pwd3", "is_superuser": False},
        {"username": "admin", "email": "admin@example.com", "password_hash": b"pwd5", "is_superuser": True},
    ]


@pytest.fixture(scope="session")
def mock_user() -> dict[str, Any]:
    return {"username": "lonely", "email": "someuser@example.com", "password_hash": b"pwd4", "is_superuser": False}


@pytest.fixture(scope="function")
async def create_mock_users(session: AsyncSession, mock_users_list: list[dict[str, Any]]) -> None:
    for mock_user in mock_users_list:
        stmt = insert(User).values(**mock_user).returning(User)
        await session.execute(stmt)