from aiogram import types, Router
from aiogram.filters import Command
from aiogram import F

from app.bot.vocabulary.callback_patterns import VocabularyCallbackData, VocabularyAction
from app.bot.vocabulary.messages import VocabularyMessages
from app.shared.exceptions import UserIsNotOwnerOfVocabulary, VocabularyDoesNotExist, VocabularyIsAlreadyActive
from app.vocabulary.services import VocabularyService

router = Router()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.delete))
async def handle_delete_vocabulary_action(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    try:
        await VocabularyService.delete_vocabulary(query.from_user.id, callback_data.vocabulary_id)

    except VocabularyDoesNotExist:
        await query.answer(text=VocabularyMessages.vocabulary_dont_exists)

    except UserIsNotOwnerOfVocabulary:
        await query.answer(text=VocabularyMessages.user_is_not_owner_of_vocabulary)

    else:
        await query.message.delete()
        await query.answer(text=VocabularyMessages.vocabulary_deleted_successfully)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.enable_notification))
async def handle_enable_notification_vocabulary_action(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    try:
        vocabulary = await VocabularyService.disable_active_vocabulary_and_enable_given(
            query.from_user.id,
            callback_data.vocabulary_id
        )

    except VocabularyDoesNotExist:
        await query.answer(text=VocabularyMessages.vocabulary_dont_exists)

    except UserIsNotOwnerOfVocabulary:
        await query.answer(text=VocabularyMessages.user_is_not_owner_of_vocabulary)
    
    except VocabularyIsAlreadyActive:
        await query.answer(text=VocabularyMessages.vocabulary_already_active)

    else:
        vocabulary_is_active_msg = await query.message.answer(
            text=VocabularyMessages.active_vocabulary.format(vocabulary_name=vocabulary.name)
        )
        await vocabulary_is_active_msg.pin(disable_notification=True)


@router.message(Command("disable"))
async def handle_disable_notifications_command(message: types.Message):
    await VocabularyService.disable_user_vocabulary(message.from_user.id)

    vocabulary_disabled_message = await message.answer(text=VocabularyMessages.no_active_vocabulary)
    await vocabulary_disabled_message.pin(disable_notification=True)