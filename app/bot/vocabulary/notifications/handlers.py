from aiogram import types, Router
from aiogram.filters import Command
from aiogram import F

from app.bot.vocabulary.callback_patterns import VocabularyCallbackData, VocabularyAction
from .actions import disable_user_active_vocabulary, disable_vocabulary, enable_vocabulary
from app.bot.vocabulary.show.actions import show_vocabulary_in_existing_msg

router = Router()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.enable_notification))
async def handle_enable_notification_button(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    enabled_vocabulary = await enable_vocabulary(query.message, query.from_user.id, callback_data.vocabulary_id)
    await show_vocabulary_in_existing_msg(enabled_vocabulary, query.message)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.disable_notification))
async def handle_disable_notification_btn(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    disabled_vocabulary = await disable_vocabulary(query.message, callback_data.vocabulary_id)
    await show_vocabulary_in_existing_msg(disabled_vocabulary, query.message)


@router.message(Command("disable"))
async def handle_disable_notifications_command(message: types.Message):
    await disable_user_active_vocabulary(message)