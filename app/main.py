from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.bot.router import router as bot_router
from app.bot.services.webhook import BotWebhookService
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup

    bot_webhook_service = BotWebhookService(
        bot_token=settings.BOT_TOKEN,
        webhook_url=settings.WEBHOOK_URL,
        webhook_prefix=bot_router.prefix,
    )
    bot_webhook_service.set_webhook_if_current_unmatched()

    yield

    # on shutdown

app = FastAPI(
    title='Language bot',
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(bot_router)