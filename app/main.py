import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI

from app.bot.main.handlers.start import router as start_router
from app.bot.vocabulary.router import vocabulary_router
from app.config import settings


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)

bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
fsm_storage = MemoryStorage()
dp = Dispatcher(storage=fsm_storage)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    await bot.set_webhook(url=settings.WEBHOOK_URL)
    logger.info("App started")

    dp.include_router(start_router)
    dp.include_router(vocabulary_router)

    yield
    # on shutdown
    await bot.session.close()
    logger.info("App stopped")

app = FastAPI(
    title='Language bot',
    debug=settings.DEBUG,
    lifespan=lifespan,
)

@app.post(settings.WEBHOOK_PATH)
async def handle_tg_response(update: types.Update):
    await dp.feed_update(bot=bot, update=update)