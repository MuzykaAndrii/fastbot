import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.backend.vocabulary.dal import LanguagePairDAL
from app.backend.vocabulary.models import LanguagePair, VocabularySet




async def test_create_language_pair(lp_dal: LanguagePairDAL, mock_vocabulary: VocabularySet):
    mock_lp = {"vocabulary_id": mock_vocabulary.id, "word": "hello", "translation": "hola"}

    language_pair = await lp_dal.create(**mock_lp)

    assert language_pair.id is not None
    assert language_pair.word == mock_lp["word"]
    assert language_pair.translation == mock_lp["translation"]
    assert language_pair.vocabulary_id == mock_vocabulary.id


async def test_create_language_pair_with_invalid_data(session: AsyncSession, lp_dal: LanguagePairDAL):
    mock_language_pair = {"vocabulary_id": 999, "word": "hello", "translation": "hola"}  # Non-existent vocabulary_id

    with pytest.raises(IntegrityError):
        await lp_dal.create(**mock_language_pair)


async def test_get_by_id_language_pair(session: AsyncSession, lp_dal: LanguagePairDAL, mock_vocabulary: VocabularySet):
    mock_lp = {"vocabulary_id": mock_vocabulary.id, "word": "hello", "translation": "hola"}
    stmt = insert(LanguagePair).values(**mock_lp).returning(LanguagePair)
    result = await session.execute(stmt)
    created_pair = result.scalar_one()

    fetched_pair = await lp_dal.get_by_id(created_pair.id)
    
    assert fetched_pair is not None
    assert fetched_pair.id == created_pair.id
    assert fetched_pair.word == mock_lp["word"]
    assert fetched_pair.translation == mock_lp["translation"]


async def test_get_non_existent_language_pair(lp_dal: LanguagePairDAL):
    non_existent_id = 9999
    fetched_pair = await lp_dal.get_by_id(non_existent_id)
    assert fetched_pair is None


async def test_bulk_create_language_pairs(session: AsyncSession, lp_dal: LanguagePairDAL, mock_vocabulary: VocabularySet):
    mock_lps = [
        {"id": 1, "vocabulary_id": mock_vocabulary.id, "word": "hello", "translation": "hola"},
        {"id": 2, "vocabulary_id": mock_vocabulary.id, "word": "world", "translation": "mundo"},
    ]

    await lp_dal.bulk_create(mock_lps)
    created_lps = await session.scalars(select(LanguagePair).filter_by(vocabulary_id=mock_vocabulary.id).order_by(LanguagePair.id))

    assert len(list(created_lps)) == len(mock_lps)

    for created, mock in zip(created_lps, mock_lps):
        assert created.id == mock["id"]
        assert created.vocabulary_id == mock["vocabulary_id"]
        assert created.word == mock["word"]
        assert created.translation == mock["translation"]


async def test_delete_by_id_language_pair(session: AsyncSession, lp_dal: LanguagePairDAL, mock_vocabulary: VocabularySet):
    mock_language_pair = {"vocabulary_id": mock_vocabulary.id, "word": "hello", "translation": "hola"}
    stmt = insert(LanguagePair).values(**mock_language_pair).returning(LanguagePair)
    result = await session.execute(stmt)
    language_pair = result.scalar_one()

    deleted_lp = await lp_dal.delete_by_id(language_pair.id)

    assert deleted_lp.id == language_pair.id

    unexist_lp = await session.scalar(select(LanguagePair).filter_by(id=language_pair.id))
    assert unexist_lp is None


async def test_delete_non_existent_language_pair(lp_dal: LanguagePairDAL):
    non_existent_id = 9999
    with pytest.raises(NoResultFound):
        await lp_dal.delete_by_id(non_existent_id)