import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Callable, Self, TypeVar

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from .dal import BaseDAL


log = logging.getLogger("backend.db.uow")


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

R = TypeVar("R", bound=BaseDAL)

class BaseUnitOfWork(UnitOfWorkInterface):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._repos_initialized = False
        self.persistent = True

        log.debug("UOW initialized")

    async def __aenter__(self) -> Self:
        log.debug("UOW transaction begin")

        if self.session is None:
            self.session = self._session_factory()

        if not self._repos_initialized:
            self.init_repos()
            self._repos_initialized = True

        return self
    
    def __call__(self, persistent: bool) -> Self:
        self.persistent = persistent
        return self

    @abstractmethod
    def init_repos(self) -> None:
        """
        Usage:
            - Inherit BaseUnitOfWork and define this method
            - use method register_repo to attach db session to you're repositories
        Example:
            from your_repositories import User, Profile

            class MyUnitOfWork(BaseUnitOfWork):
                def init_repos(self):
                    self.users = self.register_repo(UserRepository)
                    self.profiles = self.register_repo(ProfileRepository)
        """
        pass

    def register_repo(self, repo: type[R]) -> R:
        log.debug(f"Repo: {repo.__name__} initialized")
        return repo(self.session)
        
    async def __aexit__(
        self,
        exception: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.persistent:
            if exception:
                await self.undo()
                log.warning("UOW transaction failed")
            else:
                await self.save()
                log.debug("UOW transaction succeed")

        self.persistent = True
        await asyncio.shield(self.session.close())
        log.debug("UOW transaction end")

    async def save(self):
        await self.session.commit()

    async def undo(self):
        await self.session.rollback()