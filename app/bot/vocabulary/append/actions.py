from app.bot.vocabulary.validators import VocabularyParser
from app.shared.schemas import LanguagePairsAppendSchema
from app.vocabulary.services import VocabularyService


async def append_lang_pairs_to_vocabulary(user_id: int, vocabulary_id: int, raw_language_pairs: str) -> None:
    language_pairs = VocabularyParser().parse_bulk_vocabulary(raw_language_pairs)

    append_lp_data = LanguagePairsAppendSchema(
        user_id=user_id,
        vocabulary_id=vocabulary_id,
        language_pairs=language_pairs,
    )
    await VocabularyService.append_language_pairs_to_vocabulary(append_lp_data)