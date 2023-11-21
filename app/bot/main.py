from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings
from app.bot.base.handlers.start import router as start_router
from app.bot.vocabulary.router import vocabulary_router



class TelegramBot:
    def __init__(self, token: str, webhook_url: str, parse_mode=ParseMode.HTML) -> None:
        self._bot = Bot(token=token, parse_mode=parse_mode)
        fsm_storage = MemoryStorage()
        self._dp = Dispatcher(storage=fsm_storage)
        self._webhook_url = webhook_url
    
    @property
    def bot(self):
        return self._bot
    
    @property
    def dispatcher(self):
        return self._dp
    
    def include_routes(self, routes: list[Router]) -> None:
        for router in routes:
            self._dp.include_router(router)
    
    async def handle_update(self, update: types.Update):
        await self._dp.feed_update(bot=self._bot, update=update)
    
    async def start_bot(self):
        await self._bot.set_webhook(self._webhook_url)
    
    async def stop_bot(self):
        await self._bot.session.close()


bot = TelegramBot(token=settings.BOT_TOKEN, webhook_url=settings.WEBHOOK_URL)
bot.include_routes([
    start_router,
    vocabulary_router,
])