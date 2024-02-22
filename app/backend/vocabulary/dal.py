from typing import Any, Callable

from sqlalchemy import UnaryExpression, and_, select, update
from sqlalchemy.orm import selectinload

from app.backend.db.dal import BaseDAL
from app.backend.vocabulary.models import VocabularySet, LanguagePair


class VocabularySetDAL(BaseDAL[VocabularySet]):
    model = VocabularySet

    @classmethod
    async def disable_user_active_vocabulary(cls, user_id: int):
        async with cls.make_session() as session:
            stmt = (
                update(VocabularySet)
                .where(and_(VocabularySet.owner_id == user_id, VocabularySet.is_active == True))
                .values(is_active=False)
            )
            await session.execute(stmt)
            await session.commit()
    

    @classmethod
    async def make_active(cls, vocabulary_id: int) -> VocabularySet:
        return await cls._change_status(vocabulary_id, active=True)

    @classmethod
    async def make_inactive(cls, vocabulary_id: int) -> VocabularySet:
        return await cls._change_status(vocabulary_id, active=False)

    @classmethod
    async def _change_status(cls, vocabulary_id: int, active: bool) -> VocabularySet:
        async with cls.make_session() as session:
            stmt = (
                update(VocabularySet)
                .where(VocabularySet.id == vocabulary_id)
                .values(is_active=active)
                .returning(VocabularySet)
            )

            vocabulary = await session.execute(stmt)
            await session.commit()

            return vocabulary.unique().scalar_one()
    
    @classmethod
    async def get_latest_user_vocabulary(cls, user_id: int) -> VocabularySet | None:
        async with cls.make_session() as session:
            query = (
                select(VocabularySet)
                .where(VocabularySet.owner_id == user_id)
                .order_by(VocabularySet.created_at.desc())
                .limit(1)
            )

            latest_vocabulary = await session.execute(query)
            return latest_vocabulary.unique().scalar_one_or_none()
    
    @classmethod
    async def _get_vocabulary_by_condition(cls, user_id: int, vocabulary_id: int, order_by: UnaryExpression, comparison_op: Callable) -> VocabularySet | None:
        async with cls.make_session() as session:
            query = select(VocabularySet.created_at).filter_by(id=vocabulary_id)
            given_vocabulary_created_at = await session.scalar(query)

            query = (
                select(VocabularySet)
                .order_by(order_by)
                .limit(1)
                .where(
                    VocabularySet.owner_id == user_id,
                    comparison_op(VocabularySet.created_at, given_vocabulary_created_at)
                )
            )
            result_vocabulary = await session.execute(query)
            return result_vocabulary.unique().scalar_one_or_none()

    @classmethod
    async def get_vocabulary_that_latest_than_given(cls, user_id: int,  vocabulary_id: int) -> VocabularySet | None:
        return await cls._get_vocabulary_by_condition(user_id, vocabulary_id, VocabularySet.created_at.desc(), lambda x, y: x < y)

    @classmethod
    async def get_vocabulary_that_earliest_than_given(cls, user_id: int,  vocabulary_id: int) -> VocabularySet | None:
        return await cls._get_vocabulary_by_condition(user_id, vocabulary_id, VocabularySet.created_at.asc(), lambda x, y: x > y)



class LanguagePairDAL(BaseDAL[LanguagePair]):
    model = LanguagePair