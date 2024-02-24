from typing import Callable

from sqlalchemy import UnaryExpression, and_, select, update

from app.backend.db.dal import BaseDAL
from app.backend.vocabulary.models import VocabularySet, LanguagePair


class VocabularySetDAL(BaseDAL[VocabularySet]):
    model = VocabularySet

    async def disable_user_active_vocabulary(self, user_id: int) -> None:
        stmt = (
            update(VocabularySet)
            .where(and_(VocabularySet.owner_id == user_id, VocabularySet.is_active == True))
            .values(is_active=False)
        )
        await self.session.execute(stmt)

    
    async def make_active(self, vocabulary_id: int) -> VocabularySet:
        return await self._change_status(vocabulary_id, active=True)

    
    async def make_inactive(self, vocabulary_id: int) -> VocabularySet:
        return await self._change_status(vocabulary_id, active=False)

    
    async def _change_status(self, vocabulary_id: int, active: bool) -> VocabularySet:
        stmt = (
            update(VocabularySet)
            .where(VocabularySet.id == vocabulary_id)
            .values(is_active=active)
            .returning(VocabularySet)
        )

        vocabulary = await self.session.execute(stmt)
        return vocabulary.unique().scalar_one()
    
    
    async def get_latest_user_vocabulary(self, user_id: int) -> VocabularySet | None:
        query = (
            select(VocabularySet)
            .where(VocabularySet.owner_id == user_id)
            .order_by(VocabularySet.created_at.desc())
            .limit(1)
        )

        latest_vocabulary = await self.session.execute(query)
        return latest_vocabulary.unique().scalar_one_or_none()
    
    
    async def _get_vocabulary_by_condition(
        self,
        user_id: int,
        vocabulary_id: int,
        order_by: UnaryExpression,
        comparison_op: Callable
    ) -> VocabularySet | None:
        # TODO: refactor to receive created_at as param

        query_1 = select(VocabularySet.created_at).filter_by(id=vocabulary_id)
        given_vocabulary_created_at = await self.session.scalar(query_1)

        query_2 = (
            select(VocabularySet)
            .order_by(order_by)
            .limit(1)
            .where(
                VocabularySet.owner_id == user_id,
                comparison_op(VocabularySet.created_at, given_vocabulary_created_at)
            )
        )
        result_vocabulary = await self.session.execute(query_2)
        return result_vocabulary.unique().scalar_one_or_none()

    
    async def get_vocabulary_that_latest_than_given(self, user_id: int,  vocabulary_id: int) -> VocabularySet | None:
        return await self._get_vocabulary_by_condition(user_id, vocabulary_id, VocabularySet.created_at.desc(), lambda x, y: x < y)

    
    async def get_vocabulary_that_earliest_than_given(self, user_id: int,  vocabulary_id: int) -> VocabularySet | None:
        return await self._get_vocabulary_by_condition(user_id, vocabulary_id, VocabularySet.created_at.asc(), lambda x, y: x > y)



class LanguagePairDAL(BaseDAL[LanguagePair]):
    model = LanguagePair