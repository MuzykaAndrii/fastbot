import pytest

from app.backend.components.unitofwork import UnitOfWork
from app.backend.users.dal import UserDAL
from app.backend.vocabulary.dal import LanguagePairDAL, VocabularySetDAL


@pytest.mark.asyncio
async def test_uow_initialization(uow: UnitOfWork):    
    async with uow:
        assert isinstance(uow.users, UserDAL)
        assert isinstance(uow.vocabularies, VocabularySetDAL)
        assert isinstance(uow.language_pairs, LanguagePairDAL)