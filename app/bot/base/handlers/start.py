from aiogram import types, Router
from aiogram.filters import CommandStart, Command

from app.bot.base.messages import BaseMessages
from app.backend.components import users_service


router = Router()


@router.message(CommandStart())
@router.message(Command("about"))
async def start_handler(message: types.Message):
    await users_service.get_or_create_by_id(message.from_user.id)

    await message.answer(BaseMessages.about)


# @router.message()
# async def unknown_command_handler(message: types.Message):
#     await message.answer(BaseMessages.unknown_command_msg)