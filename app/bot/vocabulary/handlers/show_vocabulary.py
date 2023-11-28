from aiogram.filters import Command
from aiogram import F, Router, types
from aiogram.utils.chat_action import ChatActionSender
from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.handlers.utils import update_vocabulary_msg

from app.bot.vocabulary.keyboards import ActionsKeyboard
from app.bot.vocabulary.messages import VocabularyMessages
from app.shared.exceptions import NoVocabulariesFound, UserIsNotOwnerOfVocabulary, VocabularyDoesNotExist, VocabularyIsAlreadyActive
from app.vocabulary.services import VocabularyService


router = Router()

@router.message(Command("my"))
async def handle_show_vocabularies(message: types.Message):
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
        try:
            latest_vocabulary = await VocabularyService.get_recent_user_vocabulary(message.from_user.id)
        
        except NoVocabulariesFound:
            await message.answer(VocabularyMessages.user_havent_any_vocabularies)

        else:
            vocabulary_set_msg = VocabularyMessages.get_full_vocabulary_entity_msg(latest_vocabulary)
            vocabulary_actions_keyboard = ActionsKeyboard(latest_vocabulary).get_markup()

            await message.answer(vocabulary_set_msg, reply_markup=vocabulary_actions_keyboard)


async def _show_vocabulary(
    query: types.CallbackQuery,
    vocabulary_id: int,
    get_vocabulary_func: callable,
):
    try:
        vocabulary = await get_vocabulary_func(query.from_user.id, vocabulary_id)

    except VocabularyDoesNotExist:
        await query.answer(text=VocabularyMessages.vocabulary_dont_exists)

    except UserIsNotOwnerOfVocabulary:
        await query.answer(text=VocabularyMessages.user_is_not_owner_of_vocabulary)
    
    else:
        await update_vocabulary_msg(query, vocabulary)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.move_forward))
async def handle_show_next_vocabulary(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    await _show_vocabulary(
        query,
        callback_data.vocabulary_id,
        VocabularyService.get_next_vocabulary,
    )


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.move_backward))
async def handle_show_previous_vocabulary(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    await _show_vocabulary(
        query,
        callback_data.vocabulary_id,
        VocabularyService.get_previous_vocabulary,
    )