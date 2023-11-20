from aiogram import types, Router
from aiogram import F

from app.bot.vocabulary.callback_patterns import VocabularyCallbackData, VocabularyAction
from app.bot.vocabulary.messages import VocabularyMessages
from app.shared.exceptions import UserIsNotOwnerOfVocabulary, VocabularyDoesNotExist
from app.users.services.user import UserService
from app.vocabulary.dal import VocabularySetDAL
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


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.set_notification))
async def handle_set_notification_vocabulary_action(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    user = await UserService.get_by_tg_id(query.from_user.id)
    vocabulary = await VocabularySetDAL.get_by_id(callback_data.vocabulary_id)

    if not vocabulary:
        await query.answer(text=VocabularyMessages.vocabulary_dont_exists)
        return

    if user.id != vocabulary.owner_id:
        await query.answer(text=VocabularyMessages.user_is_not_owner_of_vocabulary)
        return
    
    if vocabulary.is_active:
        await query.answer(text=VocabularyMessages.vocabulary_already_active)
        return
    
    await VocabularySetDAL.disable_user_active_vocabulary(user.id)
    await VocabularySetDAL.make_active(vocabulary.id)

    vocabulary_is_active_msg = await query.message.answer(
        text=VocabularyMessages.active_vocabulary.format(vocabulary_name=vocabulary.name)
    )
    await vocabulary_is_active_msg.pin(disable_notification=True)