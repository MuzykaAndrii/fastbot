import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from app.backend.users.models import User
from app.backend.vocabulary.exceptions import NoActiveVocabulariesError
from app.backend.vocabulary.models import LanguagePair, VocabularySet
from app.backend.vocabulary.services import LanguagePairService


async def test_get_random_lang_pair_from_every_active_vocabulary(
    session: AsyncSession,
    lp_service: LanguagePairService,
    db_mock_users: list[User],
    clean_db,
):
    # Arrange
    users = db_mock_users
    vocabularies = [
        {"id": 1, "owner_id": users[0].id, "name": "U1 First Vocabulary", "is_active": True},
        {"id": 2, "owner_id": users[0].id, "name": "U1 Second Vocabulary", "is_active": False},
        {"id": 3, "owner_id": users[1].id, "name": "U2 First Vocabulary", "is_active": True},
        {"id": 4, "owner_id": users[1].id, "name": "U2 Second Vocabulary", "is_active": False},
        {"id": 5, "owner_id": users[2].id, "name": "U3 First Vocabulary", "is_active": True},
        {"id": 6, "owner_id": users[2].id, "name": "U3 Second Vocabulary", "is_active": False},
        {"id": 7, "owner_id": users[3].id, "name": "U4 First Vocabulary", "is_active": True},
        {"id": 8, "owner_id": users[3].id, "name": "U5 Second Vocabulary", "is_active": False},
    ]

    language_pairs = [
        {"word": "hello", "translation": "hola", "vocabulary_id": vocabularies[0]["id"]},
        {"word": "goodbye", "translation": "adiós", "vocabulary_id": vocabularies[0]["id"]},
        {"word": "world", "translation": "mundo", "vocabulary_id": vocabularies[1]["id"]},
        {"word": "peace", "translation": "paz", "vocabulary_id": vocabularies[1]["id"]},
        {"word": "apple", "translation": "manzana", "vocabulary_id": vocabularies[2]["id"]},
        {"word": "banana", "translation": "plátano", "vocabulary_id": vocabularies[2]["id"]},
        {"word": "dog", "translation": "perro", "vocabulary_id": vocabularies[3]["id"]},
        {"word": "cat", "translation": "gato", "vocabulary_id": vocabularies[3]["id"]},
        {"word": "water", "translation": "agua", "vocabulary_id": vocabularies[4]["id"]},
        {"word": "fire", "translation": "fuego", "vocabulary_id": vocabularies[4]["id"]},
        {"word": "sky", "translation": "cielo", "vocabulary_id": vocabularies[5]["id"]},
        {"word": "earth", "translation": "tierra", "vocabulary_id": vocabularies[5]["id"]},
        {"word": "sun", "translation": "sol", "vocabulary_id": vocabularies[6]["id"]},
        {"word": "moon", "translation": "luna", "vocabulary_id": vocabularies[6]["id"]},
        {"word": "star", "translation": "estrella", "vocabulary_id": vocabularies[7]["id"]},
        {"word": "cloud", "translation": "nube", "vocabulary_id": vocabularies[7]["id"]},
    ]

    vocabularies_by_id = {v["id"]: v for v in vocabularies}

    active_vocabularies_count = len([v for v in vocabularies if v["is_active"]])

    language_pairs_from_active_vocabularies = [
        (lp["word"], lp["translation"])
        for lp in language_pairs if vocabularies_by_id[lp["vocabulary_id"]]["is_active"]
    ]

    await session.execute(insert(VocabularySet).values(vocabularies))
    await session.execute(insert(LanguagePair).values(language_pairs))
    await session.commit()

    # Act
    random_pairs = await lp_service.get_random_lang_pair_from_every_active_vocabulary()

    # Assert
    assert len(random_pairs) == active_vocabularies_count
    for pair in random_pairs:
        assert (pair.word, pair.translation) in language_pairs_from_active_vocabularies


async def test_get_random_lang_pair_from_every_active_vocabulary_no_active_vocabularies(
    lp_service: LanguagePairService,
):
    # Act & Assert
    with pytest.raises(NoActiveVocabulariesError):
        await lp_service.get_random_lang_pair_from_every_active_vocabulary()


async def test_get_random_lang_pair_from_random_inactive_users_vocabulary(
        session: AsyncSession,
        lp_service: LanguagePairService,
        db_mock_users: list[User],
        clean_db,
    ):
    # Set up vocabularies and language pairs for specific users
    target_users_ids = [db_mock_users[0].id, db_mock_users[1].id, db_mock_users[2].id]

    # Insert inactive vocabularies for the selected users
    mock_vocabularies = [
        {"owner_id": target_users_ids[0], "name": "U1 Vocabulary 1", "is_active": False},
        {"owner_id": target_users_ids[1], "name": "U2 Vocabulary 1", "is_active": False},
        {"owner_id": target_users_ids[1], "name": "U2 Vocabulary 2", "is_active": False},
        {"owner_id": target_users_ids[2], "name": "U3 Vocabulary 1", "is_active": False},
        {"owner_id": target_users_ids[2], "name": "U3 Vocabulary 2", "is_active": False},
        {"owner_id": target_users_ids[2], "name": "U3 Vocabulary 3", "is_active": True},
    ]

    stmt = insert(VocabularySet).values(mock_vocabularies).returning(VocabularySet.id)
    vocas_ids = await session.scalars(stmt)
    await session.commit()
    vocas_ids = vocas_ids.all()

    # Insert language pairs for the vocabularies
    mock_lps = [
        # U1 Vocabulary 1
        {"vocabulary_id": vocas_ids[0], "word": "user", "translation": "користувач"},
        {"vocabulary_id": vocas_ids[0], "word": "system", "translation": "система"},

        # U2 Vocabulary 1
        {"vocabulary_id": vocas_ids[1], "word": "hello", "translation": "привіт"},
        {"vocabulary_id": vocas_ids[1], "word": "world", "translation": "світ"},

        # U2 Vocabulary 2
        {"vocabulary_id": vocas_ids[2], "word": "car", "translation": "машина"},
        {"vocabulary_id": vocas_ids[2], "word": "road", "translation": "дорога"},

        # U3 Vocabulary 1
        {"vocabulary_id": vocas_ids[3], "word": "house", "translation": "будинок"},
        {"vocabulary_id": vocas_ids[3], "word": "window", "translation": "вікно"},

        # U3 Vocabulary 2
        {"vocabulary_id": vocas_ids[4], "word": "book", "translation": "книга"},
        {"vocabulary_id": vocas_ids[4], "word": "pen", "translation": "ручка"},

        # Active vocabulary (should not be selected)
        {"vocabulary_id": vocas_ids[5], "word": "active", "translation": "активний"},
        {"vocabulary_id": vocas_ids[5], "word": "test", "translation": "тест"},
    ]

    stmt = insert(LanguagePair).values(mock_lps)
    await session.execute(stmt)
    await session.commit()

    # Call the method and verify results
    result = await lp_service.get_random_lang_pair_from_random_inactive_users_vocabulary(target_users_ids)

    # Assert we only get one random pair per user
    assert len(result) == len(set(v["owner_id"] for v in mock_vocabularies if v["is_active"] == False))  # We expect one result per inactive user