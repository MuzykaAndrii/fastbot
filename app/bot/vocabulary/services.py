import random

from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.schemas import VocabularySetSchema
from app.bot.main import bot
from app.logger import logger


async def send_notifications(vocabularies: list[VocabularySetSchema]) -> None:
    for vocabulary in vocabularies:
        random_lang_pair = random.choice(vocabulary.language_pairs)
        
        sended_notification = await bot.bot.send_message(
            vocabulary.owner.tg_id,
            VocabularyMessages.language_pair_notification.format(
                word=random_lang_pair.word,
                translation=random_lang_pair.translation
            ),
        )
        
        if sended_notification:
            logger.info(f"Sended notification to {vocabulary.owner.tg_id}")
        else:
            logger.warn(f"Sending notification to {vocabulary.owner.tg_id} failed")