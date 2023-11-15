from aiogram import types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F
from app.bot.handlers.words.keyboards import get_select_strategy_keyboard

from app.users.services.user import UserService

router = Router()


class CreateBundleForm(StatesGroup):
    name = State()
    words_strategy = State()
    bulk_strategy = State()
    line_by_line_strategy = State()



@router.message(Command("create"))
async def command_create_bundle(message: types.Message, state: FSMContext):
    # current_user_tg_id = message.from_user.id
    # user = UserService.get_by_tg_id(current_user_tg_id)

    await state.set_state(CreateBundleForm.name)
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


@router.message(CreateBundleForm.name, ~F.text)
async def handle_incorrect_bundle_name(message: types.Message, state: FSMContext):
    await message.reply("Invalid bundle name, please try again")


@router.message(CreateBundleForm.name)
async def set_bundle_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateBundleForm.words_strategy)

    select_strategy_keyboard = get_select_strategy_keyboard()
    await message.answer("Great name! Lets select words strategy now.", reply_markup=select_strategy_keyboard)


@router.message(CreateBundleForm.words_strategy, F.text.casefold() == "bulk")
async def handle_bulk_words_strategy(message: types.Message, state: FSMContext):
    await state.set_state(CreateBundleForm.bulk_strategy)
    await message.answer(
        "Okay, send me words in following format: 'foreign word - translation', separate this pairs by new line, min pairs count: 2",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(CreateBundleForm.bulk_strategy, F.text.regexp(r"^[^- ]{2,} *- *[^- ]{2,}(?:\n[^- ]{2,} *- *[^- ]{2,})*\n*$"))
async def handle_bulk_words_input(message: types.Message, state: FSMContext):
    await message.answer("success!")


@router.message(CreateBundleForm.bulk_strategy)
async def handle_bulk_words_invalid_input(message: types.Message, state: FSMContext):
    await message.answer("Invalid vocabulary, please follow the correct format")


@router.message(CreateBundleForm.words_strategy, F.text.casefold() == "line by line")
async def handle_line_by_line_words_strategy(message: types.Message, state: FSMContext):
    pass


@router.message(CreateBundleForm.words_strategy)
async def handle_invalid_words_strategy(message: types.Message, state: FSMContext):
    await message.reply("Invalid words strategy, please use the buttons in keyboard")