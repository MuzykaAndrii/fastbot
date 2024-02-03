from aiogram import types

from app.bot.vocabulary.keyboards import ActionsKeyboard
from app.vocabulary.services import VocabularyService
from app.shared.schemas import VocabularySchema

from . import messages



async def update_vocabulary_msg(message: types.Message, vocabulary: VocabularySchema) -> None:
    vocabulary_set_msg = messages.get_full_vocabulary_entity_msg(vocabulary)
    vocabulary_actions_keyboard = ActionsKeyboard(vocabulary).get_markup()

    await message.edit_text(vocabulary_set_msg)
    await message.edit_reply_markup(reply_markup=vocabulary_actions_keyboard)


async def show_recent_vocabulary(message: types.Message):
    recent_vocabulary = await VocabularyService.get_recent_user_vocabulary(message.from_user.id)
    
    vocabulary_set_msg = messages.get_full_vocabulary_entity_msg(recent_vocabulary)
    vocabulary_actions_keyboard = ActionsKeyboard(recent_vocabulary).get_markup()

    await message.answer(vocabulary_set_msg, reply_markup=vocabulary_actions_keyboard)


async def show_next_vocabulary(message: types.Message, user_id: int, vocabulary_id: int):
    next_vocabulary = await VocabularyService.get_next_vocabulary(user_id, vocabulary_id)
    await update_vocabulary_msg(message, next_vocabulary)


async def show_previous_vocabulary(message: types.Message, user_id: int, vocabulary_id: int):
    previous_vocabulary = await VocabularyService.get_previous_vocabulary(user_id, vocabulary_id)
    await update_vocabulary_msg(message, previous_vocabulary)