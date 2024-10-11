import logging

from app.backend.components.unitofwork import UnitOfWork
from app.backend.vocabulary.exceptions import NoActiveVocabulariesError
from app.shared.exceptions import (
    NoVocabulariesFound,
    UserIsNotOwnerOfVocabulary,
    VocabularyDoesNotExist,
    VocabularyIsAlreadyActive
)
from app.shared.schemas import NotificationSchema, LanguagePairsAppendSchema, VocabularyCreateSchema
from app.backend.vocabulary.models import VocabularySet, LanguagePair


log = logging.getLogger("backend.vocabulary")


class VocabularyService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow
    
    async def create_vocabulary(self, vocabulary: VocabularyCreateSchema) -> VocabularySet:
        vocabulary_as_dict: dict = vocabulary.model_dump()
        lang_pairs = [LanguagePair(**lp) for lp in vocabulary_as_dict.get("language_pairs")]
        vocabulary_as_dict.update({"language_pairs": lang_pairs})

        async with self._uow as uow:
            return await uow.vocabularies.create(**vocabulary_as_dict)

    
    async def append_language_pairs_to_vocabulary(self, append_lp_data: LanguagePairsAppendSchema) -> None:
        async with self._uow as uow:
            vocabulary_to_append = await uow.vocabularies.get_by_id(append_lp_data.vocabulary_id)
            self._validate_user_vocabulary(append_lp_data.user_id, vocabulary_to_append)

            lang_pairs_as_dicts = (lp.model_dump() for lp in append_lp_data.language_pairs)

            await uow.language_pairs.bulk_create(lang_pairs_as_dicts)

    
    async def get_recent_user_vocabulary(self, user_id: int) -> VocabularySet:
        async with self._uow(persistent=False) as uow:
            latest_vocabulary = await uow.vocabularies.get_latest_user_vocabulary(user_id)

        if not latest_vocabulary:
            raise NoVocabulariesFound
        
        return latest_vocabulary
    
    
    async def get_next_vocabulary(self, user_id: int, vocabulary_id: int) -> VocabularySet:
        async with self._uow(persistent=False) as uow:
            next_vocabulary = await uow.vocabularies.get_vocabulary_that_latest_than_given(user_id, vocabulary_id)

        self._validate_user_vocabulary(user_id, next_vocabulary)
        return next_vocabulary
    
    
    async def get_previous_vocabulary(self, user_id: int, vocabulary_id: int) -> VocabularySet | None:
        async with self._uow(persistent=False) as uow:
            previous_vocabulary = await uow.vocabularies.get_vocabulary_that_earliest_than_given(user_id, vocabulary_id)

        self._validate_user_vocabulary(user_id, previous_vocabulary)
        return previous_vocabulary

    
    async def get_all_user_vocabularies(self, user_id: int) -> list[VocabularySet]:
        async with self._uow(persistent=False) as uow:
            vocabularies = await uow.vocabularies.filter_by(owner_id=user_id)

        if not vocabularies:
            raise NoVocabulariesFound
        return vocabularies

    
    async def get_vocabulary(self, user_id: int, vocabulary_id: int) -> VocabularySet:
        async with self._uow(persistent=False) as uow:
            vocabulary = await uow.vocabularies.get_by_id(vocabulary_id)

        self._validate_user_vocabulary(user_id, vocabulary)
        return vocabulary


    async def get_random_lang_pair_from_every_active_vocabulary(self) -> list[NotificationSchema]:
        async with self._uow(persistent=False) as uow:
            random_lang_pairs = await uow.language_pairs.get_one_random_language_pair_from_each_active_vocabulary()

        if not random_lang_pairs:
            raise NoActiveVocabulariesError

        res = []
        for random_lp in random_lang_pairs:
            res.append(NotificationSchema(
                word=random_lp.word,
                translation=random_lp.translation,
                owner_id=random_lp.vocabulary.owner_id,
            ))

        return res
    
    async def get_random_lang_pair_from_random_inactive_users_vocabulary(self, users_ids: list[int]):
        async with self._uow(persistent=False) as uow:
            random_lang_pairs = await uow.language_pairs.get_one_random_language_pairs_from_random_inactive_users_vocabulary(users_ids)

        result = []
        for rand_lp in random_lang_pairs:
            result.append(NotificationSchema(
                word=rand_lp.word,
                translation=rand_lp.translation,
                owner_id=rand_lp.vocabulary.owner_id,
            ))

        return result
            

    
    async def delete_vocabulary(self, user_id: int, vocabulary_id: int) -> VocabularySet:
        async with self._uow as uow:
            vocabulary = await uow.vocabularies.get_by_id(vocabulary_id)
            self._validate_user_vocabulary(user_id, vocabulary)
            
            deleted_vocabulary = await uow.vocabularies.delete_by_id(vocabulary.id)

        return deleted_vocabulary

    
    async def disable_active_vocabulary_and_enable_given(self, user_id: int, vocabulary_id: int) -> VocabularySet:
        async with self._uow as uow:
            vocabulary_to_activate = await uow.vocabularies.get_by_id(vocabulary_id)

            self._validate_user_vocabulary(user_id, vocabulary_to_activate, check_active=True)            
            
            await uow.vocabularies.disable_user_active_vocabulary(user_id)
            activated_vocabulary = await uow.vocabularies.make_active(vocabulary_to_activate.id)

        return activated_vocabulary

    
    async def disable_user_active_vocabulary(self, user_id: int) -> None:
        async with self._uow as uow:
            await uow.vocabularies.disable_user_active_vocabulary(user_id)
    
    
    async def disable_vocabulary(self, vocabulary_id: int) -> VocabularySet:
        # TODO: add user check
        async with self._uow as uow:
            return await uow.vocabularies.make_inactive(vocabulary_id)

    
    def _validate_user_vocabulary(
        self,
        user_id: int,
        vocabulary: VocabularySet,
        check_active: bool = False,
    ):
        if not vocabulary:
            log.info("Attempt to access non-existent vocabulary")
            raise VocabularyDoesNotExist

        if user_id != vocabulary.owner_id:
            log.warning(f"Attempt to access to not own vocabulary, user id: {user_id}")
            raise UserIsNotOwnerOfVocabulary
        
        if check_active and vocabulary.is_active:
            raise VocabularyIsAlreadyActive
