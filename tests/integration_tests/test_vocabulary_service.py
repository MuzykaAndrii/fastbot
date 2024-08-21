



from app.backend.users.models import User
from app.backend.vocabulary.services import VocabularyService
from app.shared.schemas import VocabularyCreateSchema


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