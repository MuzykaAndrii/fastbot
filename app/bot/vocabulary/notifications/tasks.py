import logging

from app.bot.user.services import UserService
from app.bot.main import bot
from app.bot.vocabulary.notifications.actions import send_notification
from app.shared.schemas import NotificationSchema

logger = logging.getLogger(__name__)


async def send_notifications(language_pairs: list[NotificationSchema]) -> None:
    for lang_pair in language_pairs:
        us = UserService(lang_pair.owner_id)
        state = await us.user_has_active_state()

        if state:
            logger.info(f"Notification to {lang_pair.owner_id} skipped")
            continue
        
        notification = await send_notification(bot.bot, lang_pair)
        
        if notification:
            logger.info(f"Sended notification to {lang_pair.owner_id}")
        else:
            logger.warn(f"Sending notification to {lang_pair.owner_id} failed")