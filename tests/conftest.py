from typing import Any

import pytest
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

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


@pytest.fixture(scope="function")
async def session():
    async with database.session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def clean_db(session: AsyncSession):
    yield None

    tables = reversed(Base.metadata.sorted_tables)
    for table in tables:
        await session.execute(text(f'TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;'))

    await session.commit()


@pytest.fixture(scope="session")
def mock_users_data() -> list[dict[str, Any]]:
    return [
        {"id": 1, "username": "test_user1", "email": "voca_test_user1@example.com", "password_hash": b"pwd1", "is_superuser": False},
        {"id": 2, "username": "test_user2", "email": "voca_test_user2@example.com", "password_hash": b"pwd2", "is_superuser": False},
        {"id": 3, "username": "test_user3", "email": "voca_test_user3@example.com", "password_hash": b"pwd3", "is_superuser": False},
        {"id": 4, "username": "test_user4", "email": "voca_test_user4@example.com", "password_hash": b"pwd4", "is_superuser": False},
    ]


@pytest.fixture(scope="session")
def mock_user() -> dict[str, Any]:
    return {"id": 5, "username": "lonely", "email": "someuser@example.com", "password_hash": b"pwd4", "is_superuser": False}


@pytest.fixture(scope="function")
async def db_mock_user(session: AsyncSession, mock_user: dict[str, Any]) -> User: # type: ignore
    """Creates db-persistent mock user"""
    stmt = insert(User).values(**mock_user).returning(User)
    mock_user = await session.scalar(stmt)
    await session.commit()

    yield mock_user

    await session.execute(delete(User).filter_by(id=mock_user.id))
    await session.commit()


@pytest.fixture(scope="function")
async def session_mock_users(session: AsyncSession, mock_users_data: list[dict[str, Any]]) -> list[User]:
    """Creates session-persistent 4 mock users"""
    stmt = insert(User).values(mock_users_data).returning(User)
    users = await session.scalars(stmt)
    return list(users.unique().all())


@pytest.fixture(scope="function")
async def db_mock_users(session: AsyncSession, mock_users_data: list[dict[str, Any]]) -> list[User]: # type: ignore
    """Creates database-persistent 4 mock users"""
    # Setup
    stmt = insert(User).values(mock_users_data).returning(User)
    users = await session.scalars(stmt)
    await session.commit()

    users_list = list(users.unique().all())
    yield users_list
    
    # Teardown
    stmt1 = delete(User).where(User.id.in_([u.id for u in users_list]))
    await session.execute(stmt1)
    await session.commit()


@pytest.fixture(scope="function")
async def mock_vocabulary(session: AsyncSession, session_mock_users: list[User]) -> VocabularySet:
    """
    Creates and returns session-persistent mock vocabulary
    """
    owner = session_mock_users[2]
    mock_vocabulary = {"owner_id": owner.id, "name": "Session test Vocabulary", "is_active": False}
    stmt = insert(VocabularySet).values(**mock_vocabulary).returning(VocabularySet)
    result = await session.execute(stmt)
    return result.scalar_one()


@pytest.fixture(scope="function")
async def db_mock_vocabulary(session: AsyncSession, db_mock_users: list[User]) -> VocabularySet:  # type: ignore
    """
    Creates and returns database-persistent mock vocabulary
    """
    # Setup
    owner = db_mock_users[2]
    mock_vocabulary = {"owner_id": owner.id, "name": "Database test Vocabulary", "is_active": False}
    stmt = insert(VocabularySet).values(**mock_vocabulary).returning(VocabularySet)
    vocabulary = await session.scalar(stmt)
    await session.commit()

    yield vocabulary
    # Teardown
    await session.execute(delete(VocabularySet).where(VocabularySet.id == vocabulary.id))
    await session.commit()
