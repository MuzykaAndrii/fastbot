from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from .actions import append_lang_pairs_to_vocabulary
from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from . import messages
from app.bot.vocabulary.validators import VocabularyValidator


router = Router()

class AppendLanguagePairsStates(StatesGroup):
    handling_input = State()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.append_language_pairs))
async def append_language_pairs(query: CallbackQuery, callback_data: VocabularyCallbackData, state: FSMContext):
    await state.set_state(AppendLanguagePairsStates.handling_input)
    await state.update_data({"vocabulary_id": callback_data.vocabulary_id})
    await query.message.edit_text(messages.vocabulary_appending_rules_text, reply_markup=None)
    await query.message.answer(messages.waiting_text)


@router.message(AppendLanguagePairsStates.handling_input, F.text.func(VocabularyValidator(1).validate))
async def save_language_pairs(message: Message, state: FSMContext):
    state_data = await state.get_data()

    await append_lang_pairs_to_vocabulary(
        user_id=message.from_user.id,
        vocabulary_id=state_data.get("vocabulary_id"),
        raw_language_pairs=message.text,
    )

    await state.clear()
    await message.answer(messages.successful_save_text)

@router.message(AppendLanguagePairsStates.handling_input, ~F.text)
async def handle_wrong_input_type(message: Message):
    await message.answer(messages.wrong_input_text)

 
@router.message(AppendLanguagePairsStates.handling_input)
async def handle_invalid_input(message: Message):
    await message.answer(messages.invalid_input_text)