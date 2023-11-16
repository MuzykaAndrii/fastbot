from aiogram import Router

from app.bot.vocabulary.handlers.create_vocabulary import router as create_vocabulary_router
from app.bot.vocabulary.handlers.show_vocabulary import router as show_vocabulary_router


vocabulary_router = Router()
vocabulary_router.include_routers(
    create_vocabulary_router,
    show_vocabulary_router,
)