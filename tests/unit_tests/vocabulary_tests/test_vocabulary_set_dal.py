from typing import Any

import pytest

from app.backend.vocabulary.dal import VocabularySetDAL
from app.backend.vocabulary.models import VocabularySet


@pytest.mark.asyncio
async def test_create_vocabulary(vocabulary_dal: VocabularySetDAL, create_mock_users, mock_users_list: list[dict[str, Any]]):
    owner = mock_users_list[0]
    new_vocabulary = await vocabulary_dal.create(owner_id=owner["id"], name="Test Vocabulary", is_active=True)

    assert new_vocabulary.id is not None
    assert new_vocabulary.owner_id == owner["id"]
    assert new_vocabulary.name == "Test Vocabulary"
    assert new_vocabulary.is_active is True