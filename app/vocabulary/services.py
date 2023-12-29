import random
import re

from app.shared.exceptions import (
    NoVocabulariesFound,
    UserIsNotOwnerOfVocabulary,
    VocabularyDoesNotExist,
    VocabularyIsAlreadyActive
)
from app.shared.schemas import ExtendedLanguagePairSchema
from app.vocabulary.dal import VocabularySetDAL, LanguagePairDAL
from app.vocabulary.models import VocabularySet
from app.vocabulary.schemas import LanguagePairSchema


class VocabularyParser:
    split_rule: str = r'\s*-\s*'

    def __init__(self, vocabulary_id: int):
        self.vocabulary_id = vocabulary_id

    def parse_bulk_vocabulary(self, raw_bulk_vocabulary: str) -> list[LanguagePairSchema]:
        lines = raw_bulk_vocabulary.split('\n')
        result: list[LanguagePairSchema] = []

        for line in lines:
            result.append(self.parse_line_vocabulary(line))

        return result
    
    def parse_line_vocabulary(self, raw_line_vocabulary: str) -> LanguagePairSchema:
        word, translation = re.split(self.split_rule, raw_line_vocabulary)

        return LanguagePairSchema(
            word=word.strip(),
            translation=translation.strip(),
            vocabulary_id=self.vocabulary_id,
        )


class VocabularyService:
    @classmethod
    async def save_bulk_vocabulary(cls, vocabulary_data: dict, user_id: int):
        raw_vocabulary = vocabulary_data.get("bulk_vocabulary")
        vocabulary_name = vocabulary_data.get("name")

        vocabulary_set = await VocabularySetDAL.create(name=vocabulary_name, owner_id=user_id)

        vocabulary_parser = VocabularyParser(vocabulary_id=vocabulary_set.id)
        parsed_vocabulary = vocabulary_parser.parse_bulk_vocabulary(raw_vocabulary)

        await LanguagePairDAL.bulk_create([word_pair.model_dump() for word_pair in parsed_vocabulary])
    

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
        vocabulary_sets = await VocabularySetDAL.filter_by(owner_id=user_id)

        if vocabulary_sets:
            return vocabulary_sets
        return None


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
