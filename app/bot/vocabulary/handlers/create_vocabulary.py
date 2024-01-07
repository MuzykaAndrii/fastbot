from aiogram import types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.bot.vocabulary.keyboards import get_select_strategy_keyboard
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.validators import VocabularyValidator
from app.vocabulary.services import VocabularyService

router = Router()


class VocabularyCreationStates(StatesGroup):
    name = State()
    words_strategy = State()
    bulk_strategy = State()
    line_by_line_strategy = State()


@router.message(Command("create"))
async def command_create_bundle(message: types.Message, state: FSMContext):
    await state.set_state(VocabularyCreationStates.name)
    await message.answer(f"Hey {message.from_user.first_name}, to create words bundle, specify the bundle name")


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(VocabularyCreationStates.name, ~F.text)
async def handle_incorrect_bundle_name(message: types.Message, state: FSMContext):
    await message.reply("Invalid bundle name, please try again")


@router.message(VocabularyCreationStates.name)
async def set_bundle_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(VocabularyCreationStates.words_strategy)

    select_strategy_keyboard = get_select_strategy_keyboard()
    await message.answer("Great name! Lets select words strategy now.", reply_markup=select_strategy_keyboard)


@router.message(VocabularyCreationStates.words_strategy, F.text.casefold() == "bulk")
async def handle_bulk_words_strategy(message: types.Message, state: FSMContext):
    await state.set_state(VocabularyCreationStates.bulk_strategy)
    await message.answer(
        VocabularyMessages.bulk_vocabulary_creation_rules,
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(VocabularyCreationStates.bulk_strategy, F.text.func(VocabularyValidator.validate_bulk))
async def handle_bulk_words_input(message: types.Message, state: FSMContext):
    await state.update_data(bulk_vocabulary=message.text)
    vocabulary_data = await state.get_data()

    await VocabularyService.save_bulk_vocabulary(vocabulary_data, message.from_user.id)
    await state.clear()
    await message.answer("Vocabulary saved successfully! Check it out")


@router.message(VocabularyCreationStates.bulk_strategy)
async def handle_bulk_words_invalid_input(message: types.Message, state: FSMContext):
    await message.answer("Invalid vocabulary, please follow the correct format")


@router.message(VocabularyCreationStates.words_strategy, F.text.casefold() == "line by line")
async def handle_line_by_line_words_strategy(message: types.Message, state: FSMContext):
    pass


@router.message(VocabularyCreationStates.words_strategy)
async def handle_invalid_words_strategy(message: types.Message, state: FSMContext):
    await message.reply("Invalid words strategy, please use the buttons in keyboard")