from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.messages import VocabularyMessages
from app.text_generator.text_generator import generate_text_from_words
from app.vocabulary.services import VocabularyService


router = Router()

@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.gen_text))
async def generate_text_from_vocabulary(query: CallbackQuery, callback_data: VocabularyCallbackData):
    async with ChatActionSender.typing(bot=query.bot, chat_id=query.message.chat.id):
        vocabulary = await VocabularyService.get_vocabulary(query.from_user.id, callback_data.vocabulary_id)
        text = await generate_text_from_words(lang_pair.word for lang_pair in vocabulary.language_pairs)

        if text:
            response_msg = VocabularyMessages.generated_text.format(
                vocabulary_name=vocabulary.name,
                text=text,
            )
        else:
            response_msg = VocabularyMessages.text_generator_not_available
        
        await query.message.answer(response_msg)
