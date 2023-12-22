from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from app.bot.main import bot


class UserService:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def get_user_context(self) -> FSMContext:
        user_context = FSMContext(
            storage=bot.dispatcher.storage,
            key=StorageKey(
                chat_id=self.user_id,
                user_id=self.user_id,
                bot_id=bot.bot.id,
            )
        )
        return user_context

    async def user_has_active_state(self) -> bool:
        context = self.get_user_context()
        state = await context.get_state()

        if state is None:
            return False
        return True