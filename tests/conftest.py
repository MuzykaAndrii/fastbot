from typing import Any

import pytest
import asyncio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.components.config import app_settings
from app.backend.components.db import database
from app.config import AppModes
from app.backend.db.base import Base
from app.backend.users.models import User  # noqa
from app.backend.vocabulary.models import VocabularySet, LanguagePair  # noqa


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    assert app_settings.MODE == AppModes.TEST

    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="function")
async def session():
    async with database.session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def mock_users_list() -> list[dict[str, Any]]:
    return [
        {"id": 1, "username": "test_user1", "email": "voca_test_user1@example.com", "password_hash": b"pwd1", "is_superuser": False},
        {"id": 2, "username": "test_user2", "email": "voca_test_user2@example.com", "password_hash": b"pwd2", "is_superuser": False},
        {"id": 3, "username": "test_user3", "email": "voca_test_user3@example.com", "password_hash": b"pwd3", "is_superuser": False},
        {"id": 4, "username": "test_user4", "email": "voca_test_user4@example.com", "password_hash": b"pwd4", "is_superuser": False},
    ]


@pytest.fixture(scope="session")
def mock_user() -> dict[str, Any]:
    return {"username": "lonely", "email": "someuser@example.com", "password_hash": b"pwd4", "is_superuser": False}


@pytest.fixture(scope="function")
async def create_mock_users(session: AsyncSession, mock_users_list: list[dict[str, Any]]) -> None:
    for mock_user in mock_users_list:
        stmt = insert(User).values(**mock_user).returning(User)
        await session.execute(stmt)