from aiogram import Bot, types

from app.shared.schemas import NotificationSchema, VocabularySchema

from . import messages
from app.backend.components import vocabularies_service


async def enable_vocabulary(message: types.Message, user_id: int, vocabulary_id: int) -> VocabularySchema:
    enabled_vocabulary = await vocabularies_service.disable_active_vocabulary_and_enable_given(
        user_id,
        vocabulary_id,
    )

    vocabulary_is_active_msg = await message.answer(
        messages.active_vocabulary.format(vocabulary_name=enabled_vocabulary.name)
    )
    await vocabulary_is_active_msg.pin(disable_notification=True)
    return enabled_vocabulary


async def disable_vocabulary(message: types.Message, vocabulary_id: int) -> VocabularySchema:
    disabled_vocabulary = await vocabularies_service.disable_vocabulary(vocabulary_id)

    vocabulary_disabled_message = await message.answer(messages.no_active_vocabulary)
    await vocabulary_disabled_message.pin(disable_notification=True)

    return disabled_vocabulary


async def disable_user_active_vocabulary(message: types.Message):
    await vocabularies_service.disable_user_active_vocabulary(message.from_user.id)

    vocabulary_disabled_message = await message.answer(messages.no_active_vocabulary)
    await vocabulary_disabled_message.pin(disable_notification=True)


async def send_notification(bot: Bot, language_pair: NotificationSchema) -> types.Message | None:
    notification = await bot.send_message(
        language_pair.owner_id,
        messages.get_language_pair_notification(language_pair),
    )

    return notification