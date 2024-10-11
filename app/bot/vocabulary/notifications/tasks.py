import asyncio
import logging
from typing import Awaitable

from app.bot.main import bot
from app.bot.vocabulary.notifications.actions import send_notification
from app.shared.schemas import NotificationSchema
from app.bot.user.services import UserService


log = logging.getLogger(__name__)


async def send_notifications(notifications: list[NotificationSchema]) -> None:
    calls: list[Awaitable] = []
    for notification in notifications:
        us = UserService(notification.receiver_id)
        state = await us.user_has_active_state()

        if state:
            log.info(f"Notification to {notification.receiver_id} skipped, user busy")
            return
        
        calls.append(send_notification(bot.bot, notification))
    
    await asyncio.gather(*calls)
        
