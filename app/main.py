from contextlib import asynccontextmanager

from aiogram import types
from fastapi import FastAPI

from app.config import settings
from app.bot.main import bot
from app.users.services.user import UserService
from app.vocabulary.routes import router as vocabulary_router
from app.logger import logger
from app.admin.admin import admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    await UserService.ensure_admin_exists()

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


@app.post(settings.WEBHOOK_PATH, include_in_schema=settings.DEBUG)
async def handle_tg_response(update: types.Update):
    await bot.handle_update(update)


@app.get("/ping", status_code=200)
async def ping():
    return {"detail": "pong"}


app.include_router(vocabulary_router)
admin.mount_to(app)