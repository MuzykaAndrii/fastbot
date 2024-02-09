from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.validators import VocabularyParser, VocabularyValidator
from app.shared.schemas import LanguagePairsAppendSchema
from app.vocabulary.services import VocabularyService


router = Router()

class AppendLanguagePairsStates(StatesGroup):
    handling_input = State()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.append_language_pairs))
async def append_language_pairs(query: CallbackQuery, callback_data: VocabularyCallbackData, state: FSMContext):
    await state.set_state(AppendLanguagePairsStates.handling_input)
    await state.update_data({"vocabulary_id": callback_data.vocabulary_id})
    await query.message.edit_text(VocabularyMessages.vocabulary_appending_rules, reply_markup=None)
    await query.message.answer("Okay, send me new words! I am waiting)")


@router.message(AppendLanguagePairsStates.handling_input, F.text.func(VocabularyValidator(1).validate))
async def save_language_pairs(message: Message, state: FSMContext):
    state_data = await state.get_data()

    user_id = message.from_user.id
    vocabulary_id = state_data.get("vocabulary_id")
    language_pairs = VocabularyParser().parse_bulk_vocabulary(message.text)

    append_lp_data = LanguagePairsAppendSchema(
        user_id=user_id,
        vocabulary_id=vocabulary_id,
        language_pairs=language_pairs,
    )
    await VocabularyService.append_language_pairs_to_vocabulary(append_lp_data)

    # TODO: show edited vocabulary
    await message.answer("New words saved successfully, check it out by /my")

@router.message(AppendLanguagePairsStates.handling_input, ~F.text)
async def handle_wrong_input_type(message: Message):
    await message.answer("Oh no! It seems what your'e sent something wrong. Try again.")

 
@router.message(AppendLanguagePairsStates.handling_input)
async def handle_invalid_input(message: Message):
    await message.answer("Oh no! Your'e sent word(s) in wrong format. Please send me word pairs appropriate to instructions above.")