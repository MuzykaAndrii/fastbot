from aiogram.filters import Command
from aiogram import Router, types
from app.bot.vocabulary.keyboards import get_vocabulary_actions_keyboard

from app.bot.vocabulary.messages import VocabularyMessages
from app.vocabulary.services import VocabularyService


router = Router()


@router.message(Command("my"))
async def show_vocabularies(message: types.Message):
    vocabulary_sets = await VocabularyService.get_user_vocabularies(message.from_user.id)

    if not vocabulary_sets:
        await message.answer(VocabularyMessages.user_havent_any_vocabularies)
        return

    for vocabulary_set in vocabulary_sets:
        vocabulary_set_msg = VocabularyMessages.get_vocabulary_entity_msg(
            vocabulary_set.name,
            vocabulary_set.language_pairs,
            vocabulary_set.is_active,
        )

        vocabulary_actions_keyboard = get_vocabulary_actions_keyboard(vocabulary_set.id)
        await message.answer(vocabulary_set_msg, reply_markup=vocabulary_actions_keyboard)