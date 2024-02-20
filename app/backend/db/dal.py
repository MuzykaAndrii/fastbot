from abc import ABC
from typing import (
    Any,
    Generic,
    Iterable,
    Mapping,
    TypeVar,
)

from sqlalchemy import (
    delete,
    select,
)

from .session import async_session_maker
from .base import Base


T = TypeVar("T", bound=Base)


class BaseDAL(Generic[T], ABC):
    model: type[T]
    make_session = async_session_maker

    @classmethod
    async def get_by_id(cls, id: int) -> T | None:
        async with cls.make_session() as session:
            result = await session.get(cls.model, id)

            if not result:
                return None
            return result

    @classmethod
    async def create(cls, **fields: Mapping) -> T:
        async with cls.make_session() as session:
            instance = cls.model(**fields)

            session.add(instance)
            await session.commit()
            await session.refresh(instance)

            return instance
    
    @classmethod
    async def bulk_create(cls, instances: list[Mapping[str, Any]]) -> None:
        async with cls.make_session() as session:
            for fields in instances:
                instance = cls.model(**fields)
                session.add(instance)
            
            await session.commit()

    @classmethod
    async def delete_by_id(cls, id: int) -> T:
        async with cls.make_session() as session:
            stmt = delete(cls.model).where(cls.model.id == id).returning(cls.model)

            deleted_instance = await session.execute(stmt)
            await session.commit()
            return deleted_instance.unique().scalar_one()

    @classmethod
    async def get_all(cls, offset: int = 0, limit: int = 50) -> Iterable[T] | None:
        async with cls.make_session() as session:
            stmt = select(cls.model).offset(offset).limit(limit)

            instances = await session.execute(stmt)
            return instances.scalars().all()

    @classmethod
    async def filter_by(cls, **filter_criteria: Mapping) -> Iterable[T] | None:
        async with cls.make_session() as session:
            stmt = select(cls.model).filter_by(**filter_criteria)

            filter_result = await session.scalars(stmt)
            return filter_result.unique().all()
    
    @classmethod
    async def get_one(cls, **filter_criteria: Mapping) -> T | None:
        # TODO: refactor with previous method to reduce duplication
        async with cls.make_session() as session:
            stmt = select(cls.model).filter_by(**filter_criteria)
            
            filter_result = await session.execute(stmt)
            return filter_result.unique().scalar_one_or_none()
    
    @classmethod
    async def get_or_create(cls, **filter_criteria: Mapping) -> T:
        instance = await cls.get_one(**filter_criteria)

        if not instance:
            instance = await cls.create(**filter_criteria)
        
        return instance