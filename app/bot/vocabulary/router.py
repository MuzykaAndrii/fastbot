from aiogram import Router

from app.bot.vocabulary.handlers.create_vocabulary import router as create_vocabulary_router
from app.bot.vocabulary.handlers.show_vocabulary import router as show_vocabulary_router
from app.bot.vocabulary.handlers.action_vocabulary import router as action_vocabulary_router
from app.bot.vocabulary.exceptions_handlers import errors_handler_router


vocabulary_router = Router()
vocabulary_router.include_routers(
    create_vocabulary_router,
    show_vocabulary_router,
    action_vocabulary_router,
    errors_handler_router,
)