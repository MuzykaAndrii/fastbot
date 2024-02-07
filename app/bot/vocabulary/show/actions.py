from aiogram import types
from aiogram.methods.send_message import SendMessage

from app.bot.vocabulary.keyboards import ActionsKeyboard
from app.vocabulary.services import VocabularyService
from app.shared.schemas import VocabularySchema

from . import messages


async def show_vocabulary(vocabulary: VocabularySchema, edit_existing: types.Message | bool = False):
    vocabulary_set_msg = messages.get_full_vocabulary_entity_msg(vocabulary)
    vocabulary_actions_keyboard = ActionsKeyboard(vocabulary).get_markup()

    if edit_existing:
        await edit_existing.edit_text(vocabulary_set_msg)
        await edit_existing.edit_reply_markup(reply_markup=vocabulary_actions_keyboard)
    else:
        await SendMessage(
            chat_id=vocabulary.owner_id,
            text=vocabulary_set_msg,
            reply_markup=vocabulary_actions_keyboard,
        )


async def show_recent_vocabulary(message: types.Message):
    recent_vocabulary = await VocabularyService.get_recent_user_vocabulary(message.from_user.id)
    await show_vocabulary(recent_vocabulary)


async def show_next_vocabulary(message: types.Message, user_id: int, vocabulary_id: int):
    next_vocabulary = await VocabularyService.get_next_vocabulary(user_id, vocabulary_id)
    await show_vocabulary(next_vocabulary, edit_existing=message)


async def show_previous_vocabulary(message: types.Message, user_id: int, vocabulary_id: int):
    previous_vocabulary = await VocabularyService.get_previous_vocabulary(user_id, vocabulary_id)
    await show_vocabulary(previous_vocabulary, edit_existing=message)