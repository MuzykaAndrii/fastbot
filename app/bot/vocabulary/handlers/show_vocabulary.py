from aiogram.filters import Command
from aiogram import F, Router, types
from aiogram.utils.chat_action import ChatActionSender
from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData

from app.bot.vocabulary.keyboards import get_vocabulary_actions_keyboard
from app.bot.vocabulary.messages import VocabularyMessages
from app.vocabulary.services import VocabularyService


router = Router()


@router.message(Command("my"))
async def show_vocabularies(message: types.Message):
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
        vocabulary_sets = await VocabularyService.get_all_user_vocabularies(message.from_user.id)

        if not vocabulary_sets:
            await message.answer(VocabularyMessages.user_havent_any_vocabularies)
            return
        
        for vocabulary_set in vocabulary_sets:  # type: VocabularySetSchema
            vocabulary_set_msg = VocabularyMessages.short_vocabulary_entity_msg.format(vocabulary_name=vocabulary_set.name)
            vocabulary_actions_keyboard = get_vocabulary_actions_keyboard(vocabulary_set.id)

            await message.answer(vocabulary_set_msg, reply_markup=vocabulary_actions_keyboard)