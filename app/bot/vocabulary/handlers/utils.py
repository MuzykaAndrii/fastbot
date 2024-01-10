from aiogram.types import CallbackQuery

from app.bot.vocabulary.keyboards import ActionsKeyboard
from app.bot.vocabulary.messages import VocabularyMessages
from app.shared.schemas import VocabularySchema


async def update_vocabulary_msg(query: CallbackQuery, vocabulary: VocabularySchema) -> None:
    vocabulary_set_msg = VocabularyMessages.get_full_vocabulary_entity_msg(vocabulary)
    vocabulary_actions_keyboard = ActionsKeyboard(vocabulary).get_markup()

    await query.message.edit_text(vocabulary_set_msg)
    await query.message.edit_reply_markup(reply_markup=vocabulary_actions_keyboard)