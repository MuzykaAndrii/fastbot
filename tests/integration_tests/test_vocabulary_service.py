from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.backend.users.models import User
from app.backend.vocabulary.models import LanguagePair, VocabularySet
from app.backend.vocabulary.services import VocabularyService
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