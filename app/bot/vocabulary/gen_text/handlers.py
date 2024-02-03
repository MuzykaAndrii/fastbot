from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.gen_text.actions import gen_text_from_vocabulary


router = Router()

@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.gen_text))
async def gen_text_button_handler(query: CallbackQuery, callback_data: VocabularyCallbackData):
    async with ChatActionSender.typing(bot=query.bot, chat_id=query.message.chat.id):
        await gen_text_from_vocabulary(query.message, query.from_user.id, callback_data.vocabulary_id)