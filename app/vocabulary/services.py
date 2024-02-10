import random

from app.shared.exceptions import (
    NoVocabulariesFound,
    UserIsNotOwnerOfVocabulary,
    VocabularyDoesNotExist,
    VocabularyIsAlreadyActive
)
from app.shared.schemas import ExtendedLanguagePairSchema, LanguagePairsAppendSchema, VocabularyCreateSchema
from app.vocabulary.dal import LanguagePairDAL, VocabularySetDAL
from app.vocabulary.models import VocabularySet, LanguagePair


class VocabularyService:
    @classmethod
    async def create_vocabulary(cls, vocabulary: VocabularyCreateSchema):
        vocabulary: dict = vocabulary.model_dump()
        lang_pairs = [LanguagePair(**lp) for lp in vocabulary.get("language_pairs")]
        vocabulary.update({"language_pairs": lang_pairs})

        await VocabularySetDAL.create(**vocabulary)


    @classmethod
    async def append_language_pairs_to_vocabulary(cls, append_lp_data: LanguagePairsAppendSchema):
        vocabulary_to_append = await VocabularySetDAL.get_by_id(append_lp_data.vocabulary_id)
        cls._validate_user_vocabulary(append_lp_data.user_id, vocabulary_to_append)

        lang_pairs_as_dicts = (lp.model_dump() for lp in append_lp_data.language_pairs)

        await LanguagePairDAL.bulk_create(lang_pairs_as_dicts)

    @classmethod
    async def get_recent_user_vocabulary(cls, user_id: int) -> VocabularySet:
        latest_vocabulary = await VocabularySetDAL.get_latest_user_vocabulary(user_id)

        if not latest_vocabulary:
            raise NoVocabulariesFound
        
        return latest_vocabulary
    
    
    @classmethod
    async def get_next_vocabulary(cls, user_id: int, vocabulary_id: int) -> VocabularySet:
        next_vocabulary = await VocabularySetDAL.get_vocabulary_that_latest_than_given(vocabulary_id)

        cls._validate_user_vocabulary(user_id, next_vocabulary)

        return next_vocabulary
    

    @classmethod
    async def get_previous_vocabulary(cls, user_id: int, vocabulary_id: int) -> VocabularySet:
        previous_vocabulary = await VocabularySetDAL.get_vocabulary_that_earliest_than_given(vocabulary_id)

        cls._validate_user_vocabulary(user_id, previous_vocabulary)

        return previous_vocabulary


    @classmethod
    async def get_all_user_vocabularies(cls, user_id: int) -> list[VocabularySet]:
        vocabularies = await VocabularySetDAL.filter_by(owner_id=user_id)

        if not vocabularies:
            raise NoVocabulariesFound
        return vocabularies

    @classmethod
    async def get_vocabulary(cls, user_id: int, vocabulary_id: int) -> VocabularySet:
        vocabulary = await VocabularySetDAL.get_by_id(vocabulary_id)

        cls._validate_user_vocabulary(user_id, vocabulary)
        return vocabulary
    

    @classmethod
    async def get_random_lang_pair_from_every_active_vocabulary(cls) -> list[ExtendedLanguagePairSchema]:
        active_vocabularies: list[VocabularySet] = await VocabularySetDAL.filter_by(is_active=True)
        random_lang_pairs: list[ExtendedLanguagePairSchema] = []

        for vocabulary in active_vocabularies:
            random_lang_pair = random.choice(vocabulary.language_pairs)
            
            random_lang_pairs.append(ExtendedLanguagePairSchema(
                word=random_lang_pair.word,
                translation=random_lang_pair.translation,
                owner_id=vocabulary.owner.id,
            ))

        return random_lang_pairs
    

    @classmethod
    async def delete_vocabulary(cls, user_id: int, vocabulary_id: int) -> VocabularySet:
        vocabulary = await VocabularySetDAL.get_by_id(vocabulary_id)

        cls._validate_user_vocabulary(user_id, vocabulary)
        
        deleted_vocabulary = await VocabularySetDAL.delete_by_id(vocabulary.id)
        return deleted_vocabulary
    

    @classmethod
    async def disable_active_vocabulary_and_enable_given(cls, user_id: int, vocabulary_id: int) -> VocabularySet:
        vocabulary_to_activate = await VocabularySetDAL.get_by_id(vocabulary_id)

        cls._validate_user_vocabulary(user_id, vocabulary_to_activate, check_active=True)            
        
        await VocabularySetDAL.disable_user_active_vocabulary(user_id)
        activated_vocabulary = await VocabularySetDAL.make_active(vocabulary_to_activate.id)

        return activated_vocabulary

    
    @classmethod
    async def disable_user_active_vocabulary(cls, user_id: int) -> None:
        await VocabularySetDAL.disable_user_active_vocabulary(user_id)
    

    @classmethod
    async def disable_vocabulary(cls, vocabulary_id: int) -> None:
        disabled_vocabulary = await VocabularySetDAL.make_inactive(vocabulary_id)
        return disabled_vocabulary


    @classmethod
    def _validate_user_vocabulary(
        cls,
        user_id: int,
        vocabulary: VocabularySet,
        check_active: bool = False,
    ):
        if not vocabulary:
            raise VocabularyDoesNotExist

        if user_id != vocabulary.owner_id:
            raise UserIsNotOwnerOfVocabulary
        
        if check_active and vocabulary.is_active:
            raise VocabularyIsAlreadyActive
