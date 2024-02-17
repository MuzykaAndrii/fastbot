from contextlib import asynccontextmanager

from aiogram import types
from fastapi import FastAPI

from app.config import settings
from app.bot.main import bot
from app.users.services import UserService
from app.vocabulary.routes import router as vocabulary_router
from app.logger import logger
from app.admin import admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    await UserService.ensure_admin_exists()

    await bot.start_bot(drop_pending_updates=settings.DEBUG)
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
    from app.db.session import async_session_maker
    from sqlalchemy import select

    async with async_session_maker() as db_session:
        await db_session.execute(select(1))
        
    return {"detail": "pong"}


app.include_router(vocabulary_router)

if settings.DEBUG:
    from app.pages.routes import router as pages_router
    app.include_router(pages_router)

admin.mount_to(app)