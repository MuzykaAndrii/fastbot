import re
from app.users.dal import UserDAL
from app.words.dal import VocabularyBundleDAL, WordPairDAL

from app.words.schemas import LanguagePairSchema


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
            bundle_id=self.vocabulary_id,
        )


class VocabularyService:
    @classmethod
    async def save_bulk_vocabulary(cls, vocabulary_data: dict, user_tg_id: int):
        raw_vocabulary = vocabulary_data.get("bulk_vocabulary")
        vocabulary_name = vocabulary_data.get("name")

        user = await UserDAL.get_or_create(tg_id=user_tg_id)
        vocabulary_bundle = await VocabularyBundleDAL.create(name=vocabulary_name, owner_id=user.id)

        vocabulary_parser = VocabularyParser(vocabulary_id=vocabulary_bundle.id)
        parsed_vocabulary = await vocabulary_parser.parse_bulk_vocabulary(raw_vocabulary)

        await WordPairDAL.bulk_create(parsed_vocabulary)
