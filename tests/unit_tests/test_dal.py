import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import InvalidRequestError
from typing import Any
from app.backend.db.dal import BaseDAL
from app.backend.users.models import User
from app.backend.vocabulary.models import VocabularySet, LanguagePair
from app.backend.users.dal import UserDAL
from app.backend.vocabulary.dal import VocabularySetDAL, LanguagePairDAL


@pytest.fixture(scope="function")
async def session_mock_vocabularies(session: AsyncSession, session_mock_users: list[User]) -> list[VocabularySet]:
    mock_vocabularies_data = [
        {"owner_id": session_mock_users[0].id, "name": "Vocab Set 1", "is_active": True},
        {"owner_id": session_mock_users[1].id, "name": "Vocab Set 2", "is_active": False},
    ]
    stmt = insert(VocabularySet).values(mock_vocabularies_data).returning(VocabularySet)
    result = await session.scalars(stmt)
    return list(result.unique().all())


@pytest.fixture(scope="function")
async def session_mock_language_pairs(session: AsyncSession, session_mock_vocabularies: list[VocabularySet]) -> list[LanguagePair]:
    mock_language_pairs_data = [
        {"word": "word", "translation": "слово", "vocabulary_id": session_mock_vocabularies[0].id},
        {"word": "мрія", "translation": "dream", "vocabulary_id": session_mock_vocabularies[0].id},
    ]
    stmt = insert(LanguagePair).values(mock_language_pairs_data).returning(LanguagePair)
    result = await session.scalars(stmt)
    return list(result.unique().all())


@pytest.fixture(params=[UserDAL, VocabularySetDAL, LanguagePairDAL])
def dal_class(request: Any, session: AsyncSession) -> BaseDAL:
    return request.param(session)


# Fixture that returns multiple mock instances for the DAL (User, VocabularySet, LanguagePair)
@pytest.fixture
def mock_instances(
    dal_class: type[BaseDAL], session_mock_users: list[User], session_mock_vocabularies: list[VocabularySet], session_mock_language_pairs: list[LanguagePair]
) -> list[Any]:
    match dal_class:
        case UserDAL():
            return session_mock_users
        case VocabularySetDAL():
            return session_mock_vocabularies
        case LanguagePairDAL():
            return session_mock_language_pairs
        case _:
            raise ValueError(f"Unrecognized DAL class: {dal_class}")



async def test_get_random_with_criteria_no_criteria(dal_class: BaseDAL, mock_instances: list[Any]) -> None:
    # Act
    random_instance = await dal_class.get_random_with_criteria()

    # Assert
    assert random_instance is not None
    assert random_instance in mock_instances


async def test_get_random_with_criteria_no_entities(dal_class: BaseDAL) -> None:
    # Act
    random_instance = await dal_class.get_random_with_criteria()

    # Assert
    assert random_instance is None


async def test_get_random_with_criteria_no_match(dal_class: BaseDAL) -> None:
    # Act
    random_instance = await dal_class.get_random_with_criteria(id=-1)

    # Assert
    assert random_instance is None


async def test_get_random_with_invalid_field(dal_class: BaseDAL) -> None:
    # Arrange
    invalid_criteria = {"invalid_field": "some_value"}

    # Act and Assert
    with pytest.raises(InvalidRequestError):
        await dal_class.get_random_with_criteria(**invalid_criteria)
