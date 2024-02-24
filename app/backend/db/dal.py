from abc import ABC
from typing import (
    Any,
    Generic,
    Iterable,
    Mapping,
    TypeVar,
)

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


from .base import Base


T = TypeVar("T", bound=Base)


class BaseDAL(Generic[T], ABC):
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_by_id(self, id: int) -> T | None:
        return await self.session.get(self.model, id)

    
    async def create(self, **fields: Any) -> T:
        instance = self.model(**fields)

        self.session.add(instance)
        await self.session.flush()

        return instance
    
    
    async def bulk_create(self, instances: list[Mapping[str, Any]]) -> None:
        self.session.add_all((self.model(**fields) for fields in instances))

    
    async def delete_by_id(self, id: int) -> T:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)

        deleted_instance = await self.session.execute(stmt)
        return deleted_instance.unique().scalar_one()

    
    async def get_all(self) -> Iterable[T] | None:
        stmt = select(self.model)

        instances = await self.session.scalars(stmt)
        return instances.unique().all()

    
    async def filter_by(self, **filter_criteria: Any) -> Iterable[T] | None:
        stmt = select(self.model).filter_by(**filter_criteria)

        filter_result = await self.session.scalars(stmt)
        return filter_result.unique().all()
    
    
    async def get_one(self, **filter_criteria: Any) -> T | None:
        # TODO: refactor with previous method to reduce duplication
        stmt = select(self.model).filter_by(**filter_criteria)
        
        filter_result = await self.session.execute(stmt)
        return filter_result.unique().scalar_one_or_none()
    
    
    async def get_or_create(self, **filter_criteria: Any) -> T:
        instance = await self.get_one(**filter_criteria)

        if not instance:
            instance = await self.create(**filter_criteria)
        
        return instance