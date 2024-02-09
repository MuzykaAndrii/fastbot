import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.fsm.storage.memory import SimpleEventIsolation

from app.config import settings
from app.bot.base.handlers.start import router as start_router
from app.bot.vocabulary import router as vocabulary_router


logging.basicConfig(level=logging.INFO)


class TelegramBot:
    def __init__(self, token: str, webhook_url: str, parse_mode=ParseMode.HTML) -> None:
        self._bot = Bot(token=token, parse_mode=parse_mode)
        self._webhook_url = webhook_url
        self._init_dispatcher()
    
    def _init_dispatcher(self) -> None:
        fsm_storage = MemoryStorage()
        self._dp = Dispatcher(
            storage=fsm_storage,
            events_isolation=SimpleEventIsolation(),
        )

    @property
    def bot(self) -> Bot:
        return self._bot
    
    @property
    def dispatcher(self) -> Dispatcher:
        return self._dp
    
    def include_routes(self, routes: list[Router]) -> None:
        for router in routes:
            self._dp.include_router(router)
    
    async def handle_update(self, update: types.Update) -> None:
        await self._dp.feed_update(bot=self._bot, update=update)
    
    async def start_bot(self, drop_pending_updates: bool = False) -> None:
        await self._bot.set_webhook(self._webhook_url, drop_pending_updates=drop_pending_updates)
    
    async def stop_bot(self) -> None:
        await self._bot.session.close()


bot = TelegramBot(token=settings.BOT_TOKEN, webhook_url=settings.WEBHOOK_URL)

bot.dispatcher.message.middleware(ChatActionMiddleware())
bot.dispatcher.callback_query.middleware(ChatActionMiddleware())

bot.include_routes([
    vocabulary_router,
    start_router,
])