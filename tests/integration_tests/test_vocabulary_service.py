from datetime import datetime, timedelta
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from app.backend.users.models import User
from app.backend.vocabulary.models import LanguagePair, VocabularySet
from app.backend.vocabulary.services import VocabularyService
from app.shared.exceptions import NoVocabulariesFound
from app.shared.schemas import LanguagePairSchema, LanguagePairsAppendSchema, VocabularyCreateSchema


async def test_create_vocabulary(vocabulary_service: VocabularyService, db_mock_user: User, clean_db):
    # Arrange
    vocabulary_data = VocabularyCreateSchema(
        owner_id=db_mock_user.id,
        name="Test Vocabulary",
        language_pairs=[
            {"word": "hello", "translation": "hola"},
            {"word": "world", "translation": "mundo"},
        ]
    )

    # Act
    new_vocabulary = await vocabulary_service.create_vocabulary(vocabulary_data)

    # Assert
    assert new_vocabulary.name == vocabulary_data.name
    assert len(new_vocabulary.language_pairs) == len(vocabulary_data.language_pairs)
    assert new_vocabulary.owner_id == db_mock_user.id


async def test_append_language_pairs_to_vocabulary(
    session: AsyncSession,
    vocabulary_service: VocabularyService,
    db_mock_vocabulary: VocabularySet,
    clean_db,
):
    # Arrange
    append_data = LanguagePairsAppendSchema(
        user_id=db_mock_vocabulary.owner_id,
        vocabulary_id=db_mock_vocabulary.id,
        language_pairs=[
            LanguagePairSchema(word="apple", translation="manzana"),
            LanguagePairSchema(word="banana", translation="plátano"),
        ]
    )

    # Act
    await vocabulary_service.append_language_pairs_to_vocabulary(append_data)

    # Assert
    query = select(LanguagePair).where(LanguagePair.vocabulary_id == db_mock_vocabulary.id)
    results = await session.execute(query)
    lang_pairs = results.scalars().all()

    assert len(lang_pairs) == len(append_data.language_pairs)
    for appended, fetched in zip(append_data.language_pairs, lang_pairs):
        assert appended.word == fetched.word
        assert appended.translation == fetched.translation


async def test_get_recent_user_vocabulary(
    session: AsyncSession,
    vocabulary_service: VocabularyService,
    db_mock_user: User,
    clean_db
):
    # Arrange
    owner = db_mock_user
    vocabularies = [
        {"id": 1, "owner_id": owner.id, "name": "First Vocabulary", "created_at": datetime.now()},
        {"id": 2, "owner_id": owner.id, "name": "Second Vocabulary", "created_at": datetime.now() + timedelta(seconds=1)},
        {"id": 3, "owner_id": owner.id, "name": "Third Vocabulary", "created_at": datetime.now() + timedelta(seconds=2)},
    ]
    newest_vocabulary = vocabularies[2]
    await session.execute(insert(VocabularySet).values(vocabularies))
    await session.commit()

    # Act
    recent_vocabulary = await vocabulary_service.get_recent_user_vocabulary(db_mock_user.id)

    # Assert
    assert recent_vocabulary.id == newest_vocabulary["id"]
    assert recent_vocabulary.name == newest_vocabulary["name"]


async def test_get_recent_user_vocabulary_no_vocabularies(vocabulary_service: VocabularyService, db_mock_user: User):
    # Act & Assert
    with pytest.raises(NoVocabulariesFound):
        await vocabulary_service.get_recent_user_vocabulary(db_mock_user.id)