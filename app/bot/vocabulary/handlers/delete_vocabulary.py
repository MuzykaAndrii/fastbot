from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.handlers.utils import update_vocabulary_msg
from app.bot.vocabulary.messages import VocabularyMessages
from app.shared.exceptions import NoVocabulariesFound
from app.vocabulary.services import VocabularyService


router = Router()

@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.delete))
async def delete_vocabulary(query: CallbackQuery, callback_data: VocabularyCallbackData):
    await VocabularyService.delete_vocabulary(query.from_user.id, callback_data.vocabulary_id)

    try:
        latest_vocabulary = await VocabularyService.get_recent_user_vocabulary(query.from_user.id)
    
    except NoVocabulariesFound:
        await query.message.edit_text(VocabularyMessages.user_havent_any_vocabularies)
        await query.message.edit_reply_markup(reply_markup=None)

    else:
        await update_vocabulary_msg(query, latest_vocabulary)

    finally:
        await query.answer(text=VocabularyMessages.vocabulary_deleted_successfully)