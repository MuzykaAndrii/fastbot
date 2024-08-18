import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.vocabulary.dal import VocabularySetDAL


@pytest.fixture(scope="function")
def vocabulary_dal(session: AsyncSession) -> VocabularySetDAL:
    return VocabularySetDAL(session)