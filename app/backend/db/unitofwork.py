from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.backend.users.dal import UserDAL

from app.backend.vocabulary.dal import LanguagePairDAL, VocabularySetDAL

from .dal import BaseDAL


class UnitOfWorkInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, type, value, traceback):
        pass

    @abstractmethod
    async def save(self):
        pass

    @abstractmethod
    async def undo(self):
        pass

T = TypeVar("T", bound=BaseDAL)

class AbstractUnitOfWork(UnitOfWorkInterface):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self._session_factory()
        self._init_repos()

        return self

    @abstractmethod
    def _init_repos(self) -> None:
        pass

    def _register_repo(self, repo: type[BaseDAL]) -> BaseDAL:
        return repo(self.session)
        
    async def __aexit__(self, type, value, traceback):
        if type is None:
            self.session.commit()
        else:
            self.session.rollback()

        self.session.close()

    async def save(self):
        await self.session.commit()

    async def undo(self):
        await self.session.rollback()


class UnitOfWork(AbstractUnitOfWork):
    def _init_repos(self) -> None:
        self.users = self._register_repo(UserDAL)
        self.vocabularies = self._register_repo(VocabularySetDAL)
        self.language_pairs = self._register_repo(LanguagePairDAL)


if __name__ == '__main__':
    from .session import async_session_maker

    uow = UnitOfWork(async_session_maker)
    uow.users.get_all()