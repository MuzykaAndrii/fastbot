from typing import Awaitable

import asyncio

from app.backend.text_generator.text_generator import generate_sentence_from_two_words, generate_sentence_from_word
from app.backend.vocabulary.services.lp_service import LanguagePairService
from app.shared.schemas import LanguagePairSchema, NotificationSchema


class NotificationService:
    def __init__(self, lp_service: LanguagePairService):  # TODO: change type hint to protocol
        self.lp_service = lp_service
    
    async def get_notifications(self) -> list[NotificationSchema]:
        """
        1. fetch primary language pairs
        2. fetch secondary language pairs
        3. generate sentences
        """

        primary_lps, secondary_lps = await self.lp_service.get_language_pairs_for_notifications()
        
        owners_notifications: dict[int, NotificationSchema] = {}
        
        for primary_lp in primary_lps:
            owner_id = primary_lp.vocabulary.owner_id
            owners_notifications[owner_id] = NotificationSchema(
                primary_lp={"word": primary_lp.word, "translation": primary_lp.translation},
                receiver_id=owner_id,
            )
        
        for secondary_lp in secondary_lps:
            owners_notifications[secondary_lp.vocabulary.owner_id].secondary_lp = LanguagePairSchema(
                word=secondary_lp.word,
                translation=secondary_lp.translation,
            )
        
        notifications = owners_notifications.values()
        calls: list[Awaitable] = []

        for notification in notifications:
            if notification.secondary_lp:
                calls.append(generate_sentence_from_two_words(notification.primary_lp.word, notification.secondary_lp.word))
            else:
                calls.append(generate_sentence_from_word(notification.primary_lp.word))
        
        sentences = await asyncio.gather(*calls)

        for notification, sentence in zip(notifications, sentences):
            notification.sentence_example = sentence

        return notifications