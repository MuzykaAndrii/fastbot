from sqlalchemy import and_, select, update

from app.db.dal import BaseDAL
from app.vocabulary.models import VocabularySet, LanguagePair


class VocabularySetDAL(BaseDAL):
    model = VocabularySet

    @classmethod
    async def disable_user_active_vocabulary(cls, user_id: int):
        async with cls.make_session() as session:
            query = (
                update(VocabularySet)
                .where(and_(VocabularySet.owner_id == user_id, VocabularySet.is_active == True))
                .values(is_active=False)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def make_active(cls, vocabulary_id: int):
        async with cls.make_session() as session:
            query = (
                update(VocabularySet)
                .where(VocabularySet.id == vocabulary_id)
                .values(is_active=True)
            )
            await session.execute(query)
            await session.commit()
    
    @classmethod
    async def get_latest_user_vocabulary(cls, user_id: int) -> VocabularySet | None:
        async with cls.make_session() as session:
            stmt = (
                select(VocabularySet)
                .where(VocabularySet.owner_id == user_id)
                .order_by(VocabularySet.created_at.desc())
                .limit(1)
            )

            latest_vocabulary = await session.execute(stmt)
            return latest_vocabulary.unique().scalar_one_or_none()
    
    @classmethod
    async def get_vocabulary_that_latest_than_given(cls, vocabulary_id: int) -> VocabularySet | None:
        async with cls.make_session() as session:
            given_vocabulary_stmt = (
                select(VocabularySet)
                .where(VocabularySet.id == vocabulary_id)
            )
            given_vocabulary = await session.execute(given_vocabulary_stmt)
            given_vocabulary = given_vocabulary.unique().scalar_one_or_none()

            stmt = (
                select(VocabularySet)
                .order_by(VocabularySet.created_at)
                .limit(1)
                .where(VocabularySet.owner_id == given_vocabulary.owner_id, VocabularySet.created_at < given_vocabulary.created_at)
            )
            result_vocabulary = await session.execute(stmt)
            return result_vocabulary.unique().scalar_one_or_none()
    
    @classmethod
    async def get_vocabulary_that_earliest_than_given(cls, vocabulary_id: int) -> VocabularySet | None:
        async with cls.make_session() as session:
            given_vocabulary_stmt = (
                select(VocabularySet)
                .where(VocabularySet.id == vocabulary_id)
            )
            given_vocabulary = await session.execute(given_vocabulary_stmt)
            given_vocabulary = given_vocabulary.unique().scalar_one_or_none()

            stmt = (
                select(VocabularySet)
                .order_by(VocabularySet.created_at)
                .limit(1)
                .where(VocabularySet.owner_id == given_vocabulary.owner_id, VocabularySet.created_at > given_vocabulary.created_at)
            )
            result_vocabulary = await session.execute(stmt)
            return result_vocabulary.unique().scalar_one_or_none()



class LanguagePairDAL(BaseDAL):
    model = LanguagePair