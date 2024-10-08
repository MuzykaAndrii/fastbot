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
        self._repos_registry: list[R] = []
        self._persistent = True

        log.debug("UOW initialized")

    async def __aenter__(self) -> Self:
        log.debug("UOW transaction begin")

        if not self.session:
            self.session = self._session_factory()
            self.init_repos()
        else:
            self._renew_repos()

        return self
    
    def __call__(self, persistent: bool) -> Self:
        self._persistent = persistent
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
        repo_instance = repo(self.session)
        log.debug(f"Repo: {repo.__name__} initialized")
        self._repos_registry.append(repo_instance)
        return repo_instance

    def _renew_repos(self) -> None:
        if self.session.is_active:
            return
        
        self.session = self._session_factory()
        for repo in self._repos_registry:
            repo.session = self.session

        
    async def __aexit__(
        self,
        exception: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._persistent:
            if exception:
                await self.undo()
                log.warning("UOW transaction failed")
            else:
                await self.save()
                log.debug("UOW transaction succeed")

        self._persistent = True
        await asyncio.shield(self.session.close())
        log.debug("UOW transaction end")

    async def save(self) -> None:
        if self._persistent:
            await self.session.commit()
        else:
            log.warning("Intercepted 'save()' operation during non-persistent transaction")

    async def undo(self) -> None:
        await self.session.rollback()
