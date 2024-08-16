from typing import Any

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.users.models import User
from app.backend.vocabulary.dal import VocabularySetDAL


@pytest.fixture(scope="function")
def vocabulary_dal(session: AsyncSession) -> VocabularySetDAL:
    return VocabularySetDAL(session)



@pytest.fixture(scope="session")
def mock_users_list() -> list[dict[str, Any]]:
    return [
        {"id": 1, "username": "voca_test_user1", "email": "voca_test_user1@example.com", "password_hash": b"pwd1", "is_superuser": False},
        {"id": 2, "username": "voca_test_user2", "email": "voca_test_user2@example.com", "password_hash": b"pwd2", "is_superuser": False},
        {"id": 3, "username": "voca_test_user3", "email": "voca_test_user3@example.com", "password_hash": b"pwd3", "is_superuser": False},
        {"id": 4, "username": "voca_test_user4", "email": "voca_test_user4@example.com", "password_hash": b"pwd4", "is_superuser": False},
    ]


@pytest.fixture(scope="function")
async def create_mock_users(session: AsyncSession, mock_users_list: list[dict[str, Any]]) -> None:
    for mock_user in mock_users_list:
        stmt = insert(User).values(**mock_user).returning(User)
        await session.execute(stmt)