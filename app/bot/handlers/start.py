from aiogram import types, Router
from aiogram.filters import CommandStart

from app.users.services.user import UserService


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    current_user_tg_id = message.from_user.id
    user = await UserService.get_or_create_from_tg_id(current_user_tg_id)

    await message.answer(f"Hey {message.from_user.first_name}")


@router.message()
async def echo_handler(message: types.Message):
    await message.answer(message.text)