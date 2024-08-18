import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.vocabulary.dal import LanguagePairDAL



@pytest.fixture(scope="function")
def lp_dal(session: AsyncSession) -> LanguagePairDAL:
    return LanguagePairDAL(session)