import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI

from app.bot.middlewares.config import ConfigMiddleware
from app.bot.handlers.start import router as start_router
from app.config import settings


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    await bot.set_webhook(url=settings.WEBHOOK_URL)
    logger.info("App started")

    dp.update.outer_middleware(ConfigMiddleware(settings))

    dp.include_router(start_router)

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
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)