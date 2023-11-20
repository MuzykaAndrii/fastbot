from sqlalchemy import and_, update

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
        


class LanguagePairDAL(BaseDAL):
    model = LanguagePair