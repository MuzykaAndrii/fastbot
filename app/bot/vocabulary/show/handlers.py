from aiogram.filters import Command
from aiogram import F, Router, types, flags

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData

from .actions import show_previous_vocabulary, show_recent_vocabulary, show_next_vocabulary


router = Router()


@router.message(Command("my"))
@flags.chat_action("typing")
async def handle_show_vocabularies_command(message: types.Message):
    await show_recent_vocabulary(message)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.move_forward))
async def handle_show_next_vocabulary_button(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    await show_next_vocabulary(query.message, query.from_user.id, callback_data.vocabulary_id)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.move_backward))
async def handle_show_previous_vocabulary_button(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    await show_previous_vocabulary(query.message, query.from_user.id, callback_data.vocabulary_id)