from aiogram import types, Router
from aiogram import F

from app.bot.vocabulary.callback_patterns import VocabularyCallbackData, VocabularyAction
from app.bot.vocabulary.messages import VocabularyMessages
from app.users.services.user import UserService
from app.vocabulary.dal import VocabularySetDAL

router = Router()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.delete))
async def handle_delete_vocabulary_action(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    user = await UserService.get_by_tg_id(query.from_user.id)
    vocabulary = await VocabularySetDAL.get_by_id(callback_data.vocabulary_id)

    if user.id != vocabulary.owner_id:
        await query.answer(text=VocabularyMessages.user_is_not_owner_of_vocabulary)
        return
    
    await VocabularySetDAL.delete_by_id(vocabulary.id)
    await query.answer(text=VocabularyMessages.vocabulary_deleted_successfully)