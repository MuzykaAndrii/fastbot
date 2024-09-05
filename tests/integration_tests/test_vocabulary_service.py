from datetime import datetime, timedelta
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select

from app.backend.users.models import User
from app.backend.vocabulary.models import LanguagePair, VocabularySet
from app.backend.vocabulary.services import VocabularyService
from app.shared.exceptions import NoVocabulariesFound, VocabularyIsAlreadyActive
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


async def test_disable_active_vocabulary_and_enable_given(
    session: AsyncSession,
    vocabulary_service: VocabularyService,
    db_mock_user: User,
    clean_db,
):
    # Arrange
    user = db_mock_user
    vocabularies = [
        {"id": 1, "owner_id": user.id, "name": "First Vocabulary", "is_active": False},
        {"id": 2, "owner_id": user.id, "name": "Second Vocabulary", "is_active": True},
        {"id": 3, "owner_id": user.id, "name": "Third Vocabulary", "is_active": False},
    ]
    vocabulary_to_activate = vocabularies[0]
    stmt = insert(VocabularySet).values(vocabularies)
    await session.execute(stmt)
    await session.commit()

    # Act
    activated_vocabulary = await vocabulary_service.disable_active_vocabulary_and_enable_given(user.id, vocabulary_to_activate["id"])

    # Assert
    assert activated_vocabulary.id == vocabulary_to_activate["id"]
    assert activated_vocabulary.name == vocabulary_to_activate["name"]

    stmt = select(func.count()).select_from(VocabularySet).filter_by(owner_id=user.id, is_active=True)
    active_vocabularies_count = await session.scalar(stmt)
    assert active_vocabularies_count == 1  # Ensure that we have only one active vocabulary


async def test_disable_active_vocabulary_and_enable_given_already_active(
    session: AsyncSession,
    vocabulary_service: VocabularyService,
    db_mock_user: User,
    clean_db,
):
    # Arrange
    user = db_mock_user
    stmt = insert(VocabularySet).values(owner_id=user.id, name="Test vocabulary", is_active=True).returning(VocabularySet)
    already_active_vocabulary = await session.scalar(stmt)
    await session.commit()

    # Act & Assert
    with pytest.raises(VocabularyIsAlreadyActive):
        await vocabulary_service.disable_active_vocabulary_and_enable_given(user.id, already_active_vocabulary.id)


async def test_delete_vocabulary(
    session: AsyncSession,
    vocabulary_service: VocabularyService,
    db_mock_vocabulary: VocabularySet,
    clean_db,
):
    # Arrange
    vocabulary_to_delete = db_mock_vocabulary
    user = vocabulary_to_delete.owner

    # Act
    deleted_vocabulary = await vocabulary_service.delete_vocabulary(user.id, vocabulary_to_delete.id)

    # Assert
    assert deleted_vocabulary.id == vocabulary_to_delete.id
    assert deleted_vocabulary.name == vocabulary_to_delete.name

    query = select(VocabularySet).filter_by(id=vocabulary_to_delete.id)
    result = await session.execute(query)
    assert result.scalar_one_or_none() is None # Ensure it's deleted


async def test_get_next_and_previous_vocabulary(
    session: AsyncSession,
    vocabulary_service: VocabularyService,
    db_mock_user: User,
    clean_db,
):
    # Arrange
    owner = db_mock_user
    vocabularies = [
        {"id": 3, "owner_id": owner.id, "name": "First Vocabulary", "created_at": datetime.now() + timedelta(minutes=3)},
        {"id": 2, "owner_id": owner.id, "name": "Second Vocabulary", "created_at": datetime.now() + timedelta(minutes=2)},
        {"id": 1, "owner_id": owner.id, "name": "Third Vocabulary", "created_at": datetime.now() + timedelta(minutes=1)},
    ]
    current_vocabulary_id = vocabularies[1]["id"]
    next_vocabulary = vocabularies[2]
    previous_vocabulary = vocabularies[0]

    await session.execute(insert(VocabularySet).values(vocabularies))
    await session.commit()

    # Act
    next_vocabulary_result = await vocabulary_service.get_next_vocabulary(owner.id, current_vocabulary_id)
    previous_vocabulary_result = await vocabulary_service.get_previous_vocabulary(owner.id, current_vocabulary_id)

    # Assert
    assert next_vocabulary_result.id == next_vocabulary["id"]
    assert next_vocabulary_result.name == next_vocabulary["name"]

    assert previous_vocabulary_result.id == previous_vocabulary["id"]
    assert previous_vocabulary_result.name == previous_vocabulary["name"]


async def test_get_all_user_vocabularies(
    session: AsyncSession,
    vocabulary_service: VocabularyService,
    db_mock_user: User,
    clean_db,
):
    # Arrange
    owner = db_mock_user
    vocabularies = [
        {"id": 1, "owner_id": owner.id, "name": "First Vocabulary"},
        {"id": 2, "owner_id": owner.id, "name": "Second Vocabulary"},
        {"id": 3, "owner_id": owner.id, "name": "Third Vocabulary"},
    ]
    await session.execute(insert(VocabularySet).values(vocabularies))
    await session.commit()

    # Act
    all_vocabularies = await vocabulary_service.get_all_user_vocabularies(owner.id)

    # Assert
    assert len(all_vocabularies) == len(vocabularies)
    for vocab, expected_vocab in zip(all_vocabularies, vocabularies):
        assert vocab.id == expected_vocab["id"]
        assert vocab.name == expected_vocab["name"]
