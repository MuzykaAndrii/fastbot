from aiogram import types, Router
from aiogram.filters import Command
from aiogram import F

from app.bot.vocabulary.callback_patterns import VocabularyCallbackData, VocabularyAction
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.show.actions import update_vocabulary_msg
from app.vocabulary.services import VocabularyService

router = Router()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.enable_notification))
async def handle_enable_notification_vocabulary_action(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    enabled_vocabulary = await VocabularyService.disable_active_vocabulary_and_enable_given(
        query.from_user.id,
        callback_data.vocabulary_id
    )

    vocabulary_is_active_msg = await query.message.answer(
        text=VocabularyMessages.active_vocabulary.format(vocabulary_name=enabled_vocabulary.name)
    )
    await vocabulary_is_active_msg.pin(disable_notification=True)
    await update_vocabulary_msg(query, enabled_vocabulary)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.disable_notification))
async def handle_disable_notification_btn(query: types.CallbackQuery):
    await VocabularyService.disable_user_active_vocabulary(query.from_user.id)

    vocabulary_disabled_message = await query.message.answer(text=VocabularyMessages.no_active_vocabulary)
    await vocabulary_disabled_message.pin(disable_notification=True)

    latest_vocabulary = await VocabularyService.get_recent_user_vocabulary(query.from_user.id)
    
    await update_vocabulary_msg(query, latest_vocabulary)

    


@router.message(Command("disable"))
async def handle_disable_notifications_command(message: types.Message):
    await VocabularyService.disable_user_active_vocabulary(message.from_user.id)

    vocabulary_disabled_message = await message.answer(text=VocabularyMessages.no_active_vocabulary)
    await vocabulary_disabled_message.pin(disable_notification=True)