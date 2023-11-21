import logging
from contextlib import asynccontextmanager

from aiogram import types
from fastapi import FastAPI

from app.config import settings
from app.bot.main import bot
from app.vocabulary.routes import router as vocabulary_router


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    await bot.start_bot()
    logger.info("App started")

    yield
    # on shutdown
    await bot.stop_bot()
    logger.info("App stopped")

app = FastAPI(
    title='Language bot',
    debug=settings.DEBUG,
    lifespan=lifespan,
)


@app.post(settings.WEBHOOK_PATH)
async def handle_tg_response(update: types.Update):
    await bot.handle_update(update)

app.include_router(vocabulary_router)