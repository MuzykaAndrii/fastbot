from aiogram import types, Router
from aiogram import F

from app.bot.vocabulary.callback_patterns import VocabularyCallbackData, VocabularyAction
from app.bot.vocabulary.messages import VocabularyMessages
from app.shared.exceptions import UserIsNotOwnerOfVocabulary, VocabularyDoesNotExist
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
        await query.bot.delete_message(query.message.chat.id, query.message.message_id)
        await query.answer(text=VocabularyMessages.vocabulary_deleted_successfully)