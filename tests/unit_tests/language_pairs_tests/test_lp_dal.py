from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.vocabulary.dal import LanguagePairDAL
from app.backend.vocabulary.models import LanguagePair, VocabularySet




async def test_create_language_pair(lp_dal: LanguagePairDAL, mock_vocabulary: VocabularySet):
    mock_lp = {"vocabulary_id": mock_vocabulary.id, "word": "hello", "translation": "hola"}

    language_pair = await lp_dal.create(**mock_lp)

    assert language_pair.id is not None
    assert language_pair.word == mock_lp["word"]
    assert language_pair.translation == mock_lp["translation"]
    assert language_pair.vocabulary_id == mock_vocabulary.id


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