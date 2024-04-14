from abc import ABC, abstractmethod
import asyncio
from types import TracebackType
from typing import Callable, Self, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

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

R = TypeVar("R", bound=BaseDAL)

class BaseUnitOfWork(UnitOfWorkInterface):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> Self:
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
        return repo(self.session)
        
    async def __aexit__(
        self,
        exception: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exception:
            await self.session.rollback()
        else:
            await self.session.commit()

        await asyncio.shield(self.session.close())

    async def save(self):
        await self.session.commit()

    async def undo(self):
        await self.session.rollback()