from app.bot.user.services import UserService
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.main import bot
from app.logger import logger
from app.shared.schemas import ExtendedLanguagePairSchema


async def send_notifications(language_pairs: list[ExtendedLanguagePairSchema]) -> None:
    for lang_pair in language_pairs:
        us = UserService(lang_pair.owner_id)
        state = await us.user_has_active_state()

        if state:
            logger.info(f"Notification to {lang_pair.owner_id} skipped")
            continue
        
        sended_notification = await bot.bot.send_message(
            lang_pair.owner_id,
            VocabularyMessages.get_language_pair_notification(lang_pair),
        )
        
        if sended_notification:
            logger.info(f"Sended notification to {lang_pair.owner_id}")
        else:
            logger.warn(f"Sending notification to {lang_pair.owner_id} failed")