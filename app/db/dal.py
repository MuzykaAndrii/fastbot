from typing import (
    Any,
    Iterable,
    Mapping,
)

from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.exc import NoResultFound

from app.db.session import async_session_maker


class BaseDAL:
    model = None

    @classmethod
    async def get_by_id(cls, id: int) -> Any | None:
        async with async_session_maker() as session:
            result = await session.get(cls.model, id)

            if not result:
                return None
            return result

    @classmethod
    async def create(cls, **fields: Mapping):
        async with async_session_maker() as session:
            instance = cls.model(**fields)

            session.add(instance)
            await session.commit()
            await session.refresh(instance)

            return instance
    
    @classmethod
    async def bulk_create(cls, instances: list[Mapping[str, Any]]) -> None:
        async with async_session_maker() as session:
            for fields in instances:
                instance = cls.model(**fields)
                session.add(instance)
            
            await session.commit()

    @classmethod
    async def delete_by_id(cls, id: int) -> Any | NoResultFound:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id == id).returning(cls.model)

            deleted_instance = await session.execute(stmt)
            return deleted_instance.scalar_one()

    @classmethod
    async def get_all(cls, offset: int = 0, limit: int = 50) -> Iterable[Any] | None:
        async with async_session_maker() as session:
            stmt = select(cls.model).offset(offset).limit(limit)

            instances = await session.execute(stmt)
            return instances.scalars().all()

    @classmethod
    async def filter_by(cls, **filter_criteria: Mapping) -> Iterable[Any] | None:
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_criteria)

            filter_result = await session.scalars(stmt)
            return filter_result.unique().all()
    
    @classmethod
    async def get_one(cls, **filter_criteria: Mapping) -> Any | None:
        # TODO: refactor with previous method to reduce duplication
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_criteria)
            
            filter_result = await session.execute(stmt)
            return filter_result.unique().scalar_one_or_none()
    
    @classmethod
    async def get_or_create(cls, **filter_criteria: Mapping) -> Any:
        instance = await cls.get_one(**filter_criteria)

        if not instance:
            instance = await cls.create(**filter_criteria)
        
        return instance