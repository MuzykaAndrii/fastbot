from datetime import datetime, timedelta
from typing import Any

import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.vocabulary.dal import VocabularySetDAL
from app.backend.vocabulary.models import VocabularySet


async def test_create_vocabulary(vocabulary_dal: VocabularySetDAL, create_mock_users, mock_users_list: list[dict[str, Any]]):
    owner = mock_users_list[0]
    new_vocabulary = await vocabulary_dal.create(owner_id=owner["id"], name="Test Vocabulary", is_active=True)

    assert new_vocabulary.id is not None
    assert new_vocabulary.owner_id == owner["id"]
    assert new_vocabulary.name == "Test Vocabulary"
    assert new_vocabulary.is_active is True


async def test_get_latest_user_vocabulary(session: AsyncSession, vocabulary_dal: VocabularySetDAL, create_mock_users, mock_users_list: list[dict[str, Any]]):
    owner = mock_users_list[2]
    mock_vocabularies = [
        {"owner_id": owner["id"], "name": "First Vocabulary", "created_at": datetime.now()},
        {"owner_id": owner["id"], "name": "Second Vocabulary", "created_at": datetime.now() + timedelta(seconds=1)},
        {"owner_id": owner["id"], "name": "Third Vocabulary", "created_at": datetime.now() + timedelta(seconds=2)},
    ]

    for mock_vocabulary in mock_vocabularies:
        stmt = insert(VocabularySet).values(**mock_vocabulary)
        await session.execute(stmt)

    latest_vocabulary = await vocabulary_dal.get_latest_user_vocabulary(user_id=owner["id"])

    assert latest_vocabulary.name == mock_vocabularies[2]["name"]


async def test_change_vocabulary_status(session: AsyncSession, vocabulary_dal: VocabularySetDAL, create_mock_users, mock_users_list: list[dict[str, Any]]):
    owner = mock_users_list[2]
    mock_vocabulary = {"id": 20, "owner_id": owner["id"], "name": "Test Vocabulary"}
    stmt = insert(VocabularySet).values(**mock_vocabulary).returning(VocabularySet)
    db_vocabulary = await session.scalar(stmt)

    await vocabulary_dal.make_active(vocabulary_id=db_vocabulary.id)
    assert db_vocabulary.is_active is True

    await vocabulary_dal.make_inactive(vocabulary_id=db_vocabulary.id)
    assert db_vocabulary.is_active is False


async def test_disable_user_active_vocabulary(
    session: AsyncSession,
    vocabulary_dal: VocabularySetDAL,
    create_mock_users,
    mock_users_list: list[dict[str, Any]]
):
    user = mock_users_list[0]
    mock_vocabulary_1 = {"owner_id": user["id"], "name": "Active Vocabulary", "is_active": True}
    mock_vocabulary_2 = {"owner_id": user["id"], "name": "Inactive Vocabulary", "is_active": False}

    await session.execute(insert(VocabularySet).values(**mock_vocabulary_1))
    await session.execute(insert(VocabularySet).values(**mock_vocabulary_2))

    await vocabulary_dal.disable_user_active_vocabulary(user_id=user["id"])

    stmt = select(VocabularySet).filter_by(owner_id=user['id'])
    vocabularies = await session.scalars(stmt)

    for vocab in vocabularies:
        assert vocab.is_active is False


async def test_get_vocabulary_that_latest_than_given(
    session: AsyncSession,
    vocabulary_dal: VocabularySetDAL,
    create_mock_users,
    mock_users_list: list[dict[str, Any]]
):
    user = mock_users_list[3]
    mock_vocabulary_1 = {
        "id": 1,
        "owner_id": user["id"],
        "name": "Latest vocabulary",
        "created_at": datetime.now(),
        "is_active": False
    }
    mock_vocabulary_2 = {
        "id": 2,
        "owner_id": user["id"],
        "name": "Earliest vocabulary",
        "created_at": datetime.now() + timedelta(seconds=1),
        "is_active": False
    }
    stmt1 = insert(VocabularySet).values(mock_vocabulary_1)
    stmt2 = insert(VocabularySet).values(mock_vocabulary_2)
    await session.execute(stmt1)
    await session.execute(stmt2)

    latest_vocabulary = await vocabulary_dal.get_vocabulary_that_latest_than_given(user_id=user["id"], vocabulary_id=mock_vocabulary_2["id"])
    assert latest_vocabulary is not None
    assert latest_vocabulary.name == mock_vocabulary_1["name"]