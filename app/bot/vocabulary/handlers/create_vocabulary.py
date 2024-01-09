from aiogram import types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.validators import VocabularyParser, VocabularyValidator
from app.shared.schemas import VocabularyCreateSchema
from app.vocabulary.services import VocabularyService

router = Router()


class VocabularyCreationStates(StatesGroup):
    name_specifying = State()
    lang_pairs_specifying = State()


@router.message(Command("create"))
async def handle_create_cmd(message: types.Message, state: FSMContext):
    await state.set_state(VocabularyCreationStates.name_specifying)
    await message.answer(f"✨ To create a new vocabulary, specify its name")


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def handle_cancel_cmd(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Cancelled. ❌")


@router.message(VocabularyCreationStates.name_specifying, ~F.text)
async def handle_incorrect_vocabulary_name(message: types.Message, state: FSMContext):
    await message.reply("Invalid vocabulary name, please try again 🤔")


@router.message(VocabularyCreationStates.name_specifying)
async def save_vocabulary_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(VocabularyCreationStates.lang_pairs_specifying)
    await message.answer(VocabularyMessages.vocabulary_creation_rules)


@router.message(VocabularyCreationStates.lang_pairs_specifying, F.text.func(VocabularyValidator.validate))
async def handle_lang_pairs_input(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    vocabulary = VocabularyCreateSchema(
        owner_id=message.from_user.id,
        name=state_data.get('name'),
        language_pairs=VocabularyParser().parse_bulk_vocabulary(message.text),
    )

    await VocabularyService.create_vocabulary(vocabulary)
    await state.clear()
    await message.answer("Vocabulary saved successfully! 🎉 Check it out using /my command!")


@router.message(VocabularyCreationStates.lang_pairs_specifying)
async def handle_lang_pairs_invalid_input(message: types.Message, state: FSMContext):
    await message.answer("Invalid vocabulary, please follow the correct format 🚫") 
