from aiogram import types, Router
from aiogram import F

from app.bot.vocabulary.callback_patterns import VocabularyCallbackData, VocabularyAction

router = Router()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.delete))
async def handle_vocabulary_action(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    pass