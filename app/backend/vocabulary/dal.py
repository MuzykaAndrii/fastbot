from typing import Callable

from sqlalchemy import UnaryExpression, and_, func, select, update
from sqlalchemy.orm import aliased

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

    async def get_one_random_language_pair_from_each_active_vocabulary(self) -> list[LanguagePair]:
        subquery = (
            select(
                LanguagePair,
                func.row_number()
                .over(partition_by=VocabularySet.owner_id, order_by=func.random())
                .label("seed")
            )
            .join(VocabularySet, VocabularySet.id == LanguagePair.vocabulary_id)
            .where(VocabularySet.is_active == True)
            .subquery()
        )

        query = (
            select(LanguagePair)
            .from_statement(  # this needs for retrieving LanguagePair instances instead of raw fields
                select(subquery).where(subquery.c.seed == 1)
            )
        )

        res = await self.session.scalars(query)
        return res.all()
    
    async def get_one_random_language_pairs_from_random_inactive_users_vocabulary(self, users_ids: list[int]) -> list[LanguagePair]:
        vocab_subquery = aliased(VocabularySet)
        language_pair_subquery = aliased(LanguagePair)
        
        vocab_query = (
            select(
                vocab_subquery.id.label("random_vocabulary_id"),
                vocab_subquery.owner_id,
            )
            .add_columns(
                func.row_number().over(
                    partition_by=vocab_subquery.owner_id,
                    order_by=func.random()
                ).label("seed")
            )
            .where(
                vocab_subquery.is_active == False,
                vocab_subquery.owner_id.in_(users_ids)
            )
            .subquery()
        )
        
        filtered_vocab_query = (
            select(vocab_query.c.random_vocabulary_id, vocab_query.c.owner_id)
            .where(vocab_query.c.seed == 1)
            .subquery()
        )
        
        language_pair_query = (
            select(
                language_pair_subquery.id,
                language_pair_subquery.word,
                language_pair_subquery.translation,
                filtered_vocab_query.c.random_vocabulary_id.label("vocabulary_id"),
            )
            .add_columns(
                func.row_number().over(
                    partition_by=language_pair_subquery.vocabulary_id,
                    order_by=func.random()
                ).label("lp_seed")
            )
            .join(
                filtered_vocab_query,
                language_pair_subquery.vocabulary_id == filtered_vocab_query.c.random_vocabulary_id
            )
            .subquery()
        )
        
        final_query = (
            select(LanguagePair)
            .from_statement(  # this need to retrieve the LanguagePair instance
                select(language_pair_query).where(language_pair_query.c.lp_seed == 1)
            )
        )

        result = await self.session.scalars(final_query)
        return result.all()
