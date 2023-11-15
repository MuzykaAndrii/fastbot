import re
from app.users.dal import UserDAL
from app.words.dal import VocabularyBundleDAL, WordPairDAL

from app.words.schemas import VocabularyUnitSchema


class VocabularyParser:
    split_rule: str = r'\s*-\s*'

    @classmethod
    def parse_bulk_vocabulary(cls, raw_vocabulary: str) -> list[VocabularyUnitSchema]:
        lines = raw_vocabulary.strip().split('\n')
        result = []

        for line in lines:
            word, translation = re.split(cls.split_rule, line)
            result.append(
                VocabularyUnitSchema(
                    word=word.strip(),
                    translation=translation.strip()
                )
            )

        return result


class VocabularyService:
    @classmethod
    async def save_bulk_vocabulary(cls, vocabulary_data: dict, user_tg_id: int):
        raw_vocabulary = vocabulary_data.get("bulk_vocabulary")
        vocabulary_name = vocabulary_data.get("name")
        parsed_vocabulary = VocabularyParser.parse_bulk_vocabulary(raw_vocabulary)
        word_pairs = list()

        user = await UserDAL.get_or_create(tg_id=user_tg_id)
        vocabulary_bundle = await VocabularyBundleDAL.create(name=vocabulary_name, owner_id=user.id)

        for word_pair in parsed_vocabulary:
            word_pairs.append({
                "word": word_pair.word,
                "translation": word_pair.translation,
                "bundle_id": vocabulary_bundle.id,
            })
        
        await WordPairDAL.bulk_create(word_pairs)