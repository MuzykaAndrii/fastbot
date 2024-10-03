from contextlib import asynccontextmanager
import logging

from aiogram import types
from fastapi import FastAPI

from app.backend.logger import init_logger
from app.backend.components.config import app_settings, sentry_settings, bot_settings
from app.bot.main import bot
from app.backend.components.db import database
from app.backend.components import users_service
from app.backend.vocabulary.routes import router as vocabulary_router
from app.backend.components.admin import admin


log = logging.getLogger("backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    init_logger()
    await users_service.ensure_admin_exists()
    await bot.start_bot(drop_pending_updates=app_settings.DEBUG)
    log.info("App started")

    yield
    # on shutdown
    await bot.stop_bot()
    log.info("App stopped")


if not app_settings.DEBUG:
    from app.backend.sentry.setup import setup_sentry
    setup_sentry(sentry_settings.dsn)


app = FastAPI(
    title='Language bot',
    debug=app_settings.DEBUG,
    lifespan=lifespan,
)


@app.post(bot_settings.WEBHOOK_PATH, include_in_schema=app_settings.DEBUG)
async def handle_tg_response(update: types.Update):
    await bot.handle_update(update)


@app.get("/ping", status_code=200)
async def ping():
    await database.ping()
    return {"detail": "pong"}


app.include_router(vocabulary_router)

if app_settings.DEBUG:
    from app.backend.pages.routes import router as pages_router
    app.include_router(pages_router)

admin.mount_to(app)