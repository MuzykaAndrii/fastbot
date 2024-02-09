from aiogram import types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from .actions import create_vocabulary
from . import messages
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.validators import VocabularyValidator

router = Router()


class VocabularyCreationStates(StatesGroup):
    name_specifying = State()
    lang_pairs_specifying = State()


@router.message(Command("create"))
async def handle_create_cmd(message: types.Message, state: FSMContext):
    await state.set_state(VocabularyCreationStates.name_specifying)
    await message.answer(messages.create_vocabulary_text)


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def handle_cancel_cmd(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(VocabularyMessages.cancelled_text)


@router.message(VocabularyCreationStates.name_specifying, ~F.text)
async def handle_incorrect_vocabulary_name(message: types.Message, state: FSMContext):
    await message.reply(messages.invalid_vocabulary_name_text)


@router.message(VocabularyCreationStates.name_specifying)
async def save_vocabulary_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(VocabularyCreationStates.lang_pairs_specifying)
    await message.answer(messages.vocabulary_creation_rules)


@router.message(VocabularyCreationStates.lang_pairs_specifying, F.text.func(VocabularyValidator().validate))
async def handle_lang_pairs_input(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    await create_vocabulary(message=message, vocabulary_name=state_data.get('name'))
    
    await state.clear()


@router.message(VocabularyCreationStates.lang_pairs_specifying)
async def handle_lang_pairs_invalid_input(message: types.Message, state: FSMContext):
    await message.answer(messages.invalid_vocabulary_input_text) 
