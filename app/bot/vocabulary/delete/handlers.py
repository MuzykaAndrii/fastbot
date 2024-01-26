from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.delete.actions import delete_vocabulary


router = Router()

@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.delete))
async def delete_vocabulary_handler(query: CallbackQuery, callback_data: VocabularyCallbackData):
    await delete_vocabulary(
        query.from_user.id,
        callback_data.vocabulary_id,
        query,
    )