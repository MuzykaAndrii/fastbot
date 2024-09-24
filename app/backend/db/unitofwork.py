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
        log.debug("UOW initialized")

    async def __aenter__(self) -> Self:
        log.debug("UOW transaction begin")
        self.session = self._session_factory()
        self._init_repos()

        return self

    @abstractmethod
    def _init_repos(self) -> None:
        """
        Usage:
            - Inherit BaseUnitOfWork and define this method
            - use method _register_repo to attach db session to you're repositories
        Example:
            from your_repositories import User, Profile

            class MyUnitOfWork(BaseUnitOfWork):
                def _init_repos(self):
                    self.users = self._register_repo(UserRepository)
                    self.profiles = self._register_repo(ProfileRepository)
        """
        pass

    def _register_repo(self, repo: type[R]) -> R:
        log.debug(f"Repo: {repo.__name__} initialized")
        return repo(self.session)
        
    async def __aexit__(
        self,
        exception: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exception:
            await self.session.rollback()
            log.warning("UOW transaction failed")
        else:
            await self.session.commit()
            log.debug("UOW transaction end")

        await asyncio.shield(self.session.close())

    async def save(self):
        await self.session.commit()

    async def undo(self):
        await self.session.rollback()