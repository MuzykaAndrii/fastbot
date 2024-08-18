from typing import Any

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.users.models import User
from app.backend.vocabulary.dal import VocabularySetDAL


@pytest.fixture(scope="function")
def vocabulary_dal(session: AsyncSession) -> VocabularySetDAL:
    return VocabularySetDAL(session)