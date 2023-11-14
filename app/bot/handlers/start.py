from aiogram import types, Router
from aiogram.filters import Command


router = Router()


@router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer(f"Hey {message.from_user.first_name}")


@router.message()
async def echo_handler(message: types.Message):
    await message.answer(message.text)