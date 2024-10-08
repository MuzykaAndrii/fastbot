from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.backend.components.unitofwork import UnitOfWork
from app.backend.users.dal import UserDAL
from app.backend.users.models import User
from app.backend.vocabulary.dal import LanguagePairDAL, VocabularySetDAL
from app.backend.vocabulary.models import LanguagePair, VocabularySet


async def test_uow_initialization(uow: UnitOfWork):    
    async with uow:
        assert isinstance(uow.users, UserDAL)
        assert isinstance(uow.vocabularies, VocabularySetDAL)
        assert isinstance(uow.language_pairs, LanguagePairDAL)


async def test_uow_no_session_leak(uow: UnitOfWork):
    try:
        async with uow:
            raise Exception("Force exception to test session leak")
    except Exception:
        pass
    
    assert not uow.session.in_transaction()
    
    with pytest.raises(Exception):
        await uow.session.execute("SELECT 1")


async def test_uow_commit(
    uow: UnitOfWork,
    session: AsyncSession,
    mock_user: dict[str, Any],
    clean_db,
):
    async with uow:
        user = await uow.users.create(**mock_user)
        vocabulary = await uow.vocabularies.create(owner_id=user.id, name="UOW Test Vocabulary")
        lp = await uow.language_pairs.create(vocabulary_id=vocabulary.id, word="Hello", translation="Hola")

    created_user = await session.scalar(select(User).filter_by(id=user.id))
    created_vocabulary = await session.scalar(select(VocabularySet).filter_by(id=vocabulary.id))
    created_lp = await session.scalar(select(LanguagePair).filter_by(id=lp.id))

    assert created_user is not None
    assert created_vocabulary is not None
    assert created_lp is not None


async def test_uow_rollback(
    uow: UnitOfWork,
    session: AsyncSession,
    mock_user: dict[str, Any],
    clean_db,
):
    with pytest.raises(Exception):
        async with uow:
            user = await uow.users.create(**mock_user)
            vocabulary = await uow.vocabularies.create(owner_id=user.id, name="UOW Test Vocabulary")
            lp = await uow.language_pairs.create(vocabulary_id=vocabulary.id, word="Hello", translation="Hola")
            raise Exception("Test Rollback")

    non_existent_user = await session.scalar(select(User).filter_by(id=user.id))
    non_existent_vocabulary = await session.scalar(select(VocabularySet).filter_by(id=vocabulary.id))
    non_existent_lp = await session.scalar(select(LanguagePair).filter_by(id=lp.id))

    assert non_existent_user is None
    assert non_existent_vocabulary is None
    assert non_existent_lp is None


async def test_uow_double_save(uow: UnitOfWork, session: AsyncSession, mock_user: dict[str, Any], clean_db):
    async with uow:
        user = await uow.users.create(**mock_user)
        await uow.save()

        user.username = "new_username"
        await uow.save()
    
    stmt = select(User).filter_by(id=user.id)
    result = await session.execute(stmt)
    saved_user = result.scalar_one()
    
    assert saved_user.username == "new_username"


async def test_uow_nested_contexts(uow: UnitOfWork, session: AsyncSession, mock_user: dict[str, Any], clean_db):    
    async with uow:
        async with uow:  # Intentionally using the same UnitOfWork instance
            user = await uow.users.create(**mock_user)
            await uow.save()
        
        # Verify that nested context didn't cause issues
        stmt = select(User).filter_by(id=user.id)
        result = await session.execute(stmt)
        saved_user = result.scalar_one()
        
        assert saved_user is not None


async def test_uow_persistent_false_mode(
    uow: UnitOfWork,
    session: AsyncSession,
    mock_user: dict[str, Any],
    clean_db
):
    async with uow(persistent=False):
        user = await uow.users.create(**mock_user)
        vocabulary = await uow.vocabularies.create(owner_id=user.id, name="Persistent False Test")

    non_existent_user = await session.scalar(select(User).filter_by(id=user.id))
    non_existent_vocabulary = await session.scalar(select(VocabularySet).filter_by(id=vocabulary.id))

    assert non_existent_user is None
    assert non_existent_vocabulary is None