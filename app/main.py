import logging
from contextlib import asynccontextmanager
import random

from aiogram import types
from fastapi import FastAPI, HTTPException

from app.bot.vocabulary.messages import VocabularyMessages
from app.config import settings
from app.vocabulary.schemas import AuthorizationSchema
from app.vocabulary.services import VocabularyService
from app.bot.main import bot


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


@app.post("/send_notifications", status_code=200)
async def send_notifications(auth: AuthorizationSchema):
    if auth.api_key != settings.API_KEY:
        raise HTTPException(403, detail="Invalid API key")
    
    active_vocabularies = await VocabularyService.get_active_vocabularies()

    if not active_vocabularies:
        raise HTTPException(204, detail="No active vocabularies")

    for vocabulary in active_vocabularies:
        random_lang_pair = random.choice(vocabulary.language_pairs)
        await bot.send_message(
            vocabulary.owner.tg_id,
            VocabularyMessages.language_pair_notification.format(
                word=random_lang_pair.word,
                translation=random_lang_pair.translation
            ),
        )
    
    return {"detail": "success"}