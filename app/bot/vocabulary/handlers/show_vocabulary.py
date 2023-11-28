from aiogram.filters import Command
from aiogram import F, Router, types, flags

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.handlers.utils import update_vocabulary_msg
from app.bot.vocabulary.keyboards import ActionsKeyboard
from app.bot.vocabulary.messages import VocabularyMessages
from app.shared.exceptions import NoVocabulariesFound
from app.vocabulary.services import VocabularyService


router = Router()


@router.message(Command("my"))
@flags.chat_action("typing")
async def handle_show_vocabularies(message: types.Message):
    try:
        latest_vocabulary = await VocabularyService.get_recent_user_vocabulary(message.from_user.id)
    
    except NoVocabulariesFound:
        await message.answer(VocabularyMessages.user_havent_any_vocabularies)

    else:
        vocabulary_set_msg = VocabularyMessages.get_full_vocabulary_entity_msg(latest_vocabulary)
        vocabulary_actions_keyboard = ActionsKeyboard(latest_vocabulary).get_markup()

        await message.answer(vocabulary_set_msg, reply_markup=vocabulary_actions_keyboard)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.move_forward))
async def handle_show_next_vocabulary(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    next_vocabulary = await VocabularyService.get_next_vocabulary(query.from_user.id, callback_data.vocabulary_id)
    await update_vocabulary_msg(query, next_vocabulary)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.move_backward))
async def handle_show_previous_vocabulary(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    previous_vocabulary = await VocabularyService.get_previous_vocabulary(query.from_user.id, callback_data.vocabulary_id)
    await update_vocabulary_msg(query, previous_vocabulary)