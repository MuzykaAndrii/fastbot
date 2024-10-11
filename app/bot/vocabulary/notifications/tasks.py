import logging

from app.bot.user.services import UserService
from app.bot.main import bot
from app.bot.vocabulary.notifications.actions import send_notification
from app.shared.schemas import NotificationSchema

logger = logging.getLogger(__name__)


async def send_notifications(notifications: list[NotificationSchema]) -> None:
    for notification in notifications:
        us = UserService(notification.receiver_id)
        state = await us.user_has_active_state()

        if state:
            logger.info(f"Notification to {notification.receiver_id} skipped, user busy")
            continue
        
        message = await send_notification(bot.bot, notification)
        
        if message:
            logger.info(f"Sended notification to {notification.receiver_id}")
        else:
            logger.warning(f"Sending notification to {notification.receiver_id} failed")