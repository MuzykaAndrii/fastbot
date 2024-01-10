from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.validators import VocabularyValidator


router = Router()

class AppendLanguagePairsStates(StatesGroup):
    handling_input = State()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.append_language_pairs))
async def append_language_pairs(query: CallbackQuery, callback_data: VocabularyCallbackData, state: FSMContext):
    await state.set_state(AppendLanguagePairsStates.handling_input)
    await state.update_data({"vocabulary_id": callback_data.vocabulary_id})
    await query.message.answer(VocabularyMessages.vocabulary_appending_rules)


@router.message(AppendLanguagePairsStates.handling_input, F.text.func(VocabularyValidator(1).validate))
async def save_language_pairs(message: Message, state: FSMContext):
    await message.answer("success")
    ...


@router.message(AppendLanguagePairsStates.handling_input, ~F.text)
async def handle_wrong_input_type(message: Message):
    await message.answer("Oh no! It seems what your'e sent something wrong. Try again.")


@router.message(AppendLanguagePairsStates.handling_input)
async def handle_invalid_input(message: Message):
    await message.answer("Oh no! Your'e sent word(s) in wrong format. Please send me word pairs appropriate to instructions above.")