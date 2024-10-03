from aiogram import types
from aiogram import Bot

from app.bot.vocabulary.keyboards import ActionsKeyboard
from app.backend.components import vocabularies_service
from app.shared.schemas import VocabularySchema

from . import messages


async def show_vocabulary(vocabulary: VocabularySchema, bot: Bot):
    vocabulary_msg = messages.get_full_vocabulary_entity_msg(vocabulary)
    vocabulary_actions_keyboard = ActionsKeyboard(vocabulary).get_markup()

    await bot.send_message(
        chat_id=vocabulary.owner_id,
        text=vocabulary_msg,
        reply_markup=vocabulary_actions_keyboard,
    )


async def show_vocabulary_in_existing_msg(vocabulary: VocabularySchema, message: types.Message) -> None:
    vocabulary_set_msg = messages.get_full_vocabulary_entity_msg(vocabulary)
    vocabulary_actions_keyboard = ActionsKeyboard(vocabulary).get_markup()

    await message.edit_text(vocabulary_set_msg)
    await message.edit_reply_markup(reply_markup=vocabulary_actions_keyboard)


async def show_recent_vocabulary(message: types.Message):
    recent_vocabulary = await vocabularies_service.get_recent_user_vocabulary(message.from_user.id)
    await show_vocabulary(recent_vocabulary, message.bot)


async def show_next_vocabulary(message: types.Message, user_id: int, vocabulary_id: int):
    next_vocabulary = await vocabularies_service.get_next_vocabulary(user_id, vocabulary_id)
    await show_vocabulary_in_existing_msg(next_vocabulary, message)


async def show_previous_vocabulary(message: types.Message, user_id: int, vocabulary_id: int):
    previous_vocabulary = await vocabularies_service.get_previous_vocabulary(user_id, vocabulary_id)
    await show_vocabulary_in_existing_msg(previous_vocabulary, message)