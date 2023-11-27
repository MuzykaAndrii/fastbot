from aiogram.filters import Command
from aiogram import F, Router, types
from aiogram.utils.chat_action import ChatActionSender
from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData

from app.bot.vocabulary.keyboards import ActionsKeyboard
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.schemas import VocabularySetSchema
from app.shared.exceptions import UserIsNotOwnerOfVocabulary, VocabularyDoesNotExist, VocabularyIsAlreadyActive
from app.vocabulary.services import VocabularyService


router = Router()


@router.message(Command("my"))
async def handle_show_vocabularies(message: types.Message):
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
        latest_vocabulary = await VocabularyService.get_recent_user_vocabulary(message.from_user.id)

        if not latest_vocabulary:
            await message.answer(VocabularyMessages.user_havent_any_vocabularies)
            return
        
        vocabulary_set_msg = VocabularyMessages.get_full_vocabulary_entity_msg(latest_vocabulary)
        vocabulary_actions_keyboard = ActionsKeyboard(latest_vocabulary.id).get_markup()

        await message.answer(vocabulary_set_msg, reply_markup=vocabulary_actions_keyboard)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.move_forward))
async def handle_show_next_vocabulary(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    try:
        next_vocabulary = await VocabularyService.get_next_vocabulary(query.from_user.id, callback_data.vocabulary_id)

    except VocabularyDoesNotExist:
        await query.answer(text=VocabularyMessages.vocabulary_dont_exists)

    except UserIsNotOwnerOfVocabulary:
        await query.answer(text=VocabularyMessages.user_is_not_owner_of_vocabulary)
    
    else:
        vocabulary_set_msg = VocabularyMessages.get_full_vocabulary_entity_msg(next_vocabulary)
        vocabulary_actions_keyboard = ActionsKeyboard(next_vocabulary.id).get_markup()

        await query.message.edit_text(vocabulary_set_msg)
        await query.message.edit_reply_markup(reply_markup=vocabulary_actions_keyboard)


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.move_backward))
async def handle_show_previous_vocabulary(query: types.CallbackQuery, callback_data: VocabularyCallbackData):
    try:
        previous_vocabulary = await VocabularyService.get_previous_vocabulary(query.from_user.id, callback_data.vocabulary_id)

    except VocabularyDoesNotExist:
        await query.answer(text=VocabularyMessages.vocabulary_dont_exists)

    except UserIsNotOwnerOfVocabulary:
        await query.answer(text=VocabularyMessages.user_is_not_owner_of_vocabulary)
    
    else:
        vocabulary_set_msg = VocabularyMessages.get_full_vocabulary_entity_msg(previous_vocabulary)
        vocabulary_actions_keyboard = ActionsKeyboard(previous_vocabulary.id).get_markup()

        await query.message.edit_text(vocabulary_set_msg)
        await query.message.edit_reply_markup(reply_markup=vocabulary_actions_keyboard)