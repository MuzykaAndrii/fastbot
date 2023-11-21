import random

from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.schemas import VocabularySetSchema
from app.bot.main import bot



async def send_notifications(vocabularies: list[VocabularySetSchema]) -> None:
    for vocabulary in vocabularies:
        random_lang_pair = random.choice(vocabulary.language_pairs)
        
        await bot.bot.send_message(
            vocabulary.owner.tg_id,
            VocabularyMessages.language_pair_notification.format(
                word=random_lang_pair.word,
                translation=random_lang_pair.translation
            ),
        )