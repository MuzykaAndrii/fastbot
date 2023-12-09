from aiogram import types, Router
from aiogram.filters import CommandStart
from app.bot.base.messages import BaseMessages

from app.users.services.user import UserService


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await UserService.get_or_create_by_tg_id(message.from_user.id)

    await message.answer(BaseMessages.start_msg.format(username=message.from_user.username))


@router.message()
async def unknown_command_handler(message: types.Message):
    await message.answer(BaseMessages.unknown_command_msg)