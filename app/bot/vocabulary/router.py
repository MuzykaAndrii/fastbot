from aiogram import Router

from app.bot.vocabulary.handlers.create_vocabulary import router as create_vocabulary_router
from app.bot.vocabulary.show.handlers import router as show_vocabulary_router
from app.bot.vocabulary.notifications.handlers import router as notifications_vocabulary_router
from app.bot.vocabulary.handlers.quiz_vocabulary import router as quiz_vocabulary_router
from app.bot.vocabulary.delete.handlers import router as delete_vocabulary_router
from app.bot.vocabulary.gen_text.handlers import router as gen_text_router
from app.bot.vocabulary.handlers.append_lang_pairs import router as append_lang_pairs_router
from app.bot.vocabulary.exceptions_handlers import errors_handler_router


vocabulary_router = Router()
vocabulary_router.include_routers(
    create_vocabulary_router,
    show_vocabulary_router,
    notifications_vocabulary_router,
    delete_vocabulary_router,
    gen_text_router,
    append_lang_pairs_router,
    quiz_vocabulary_router,

    errors_handler_router,
)