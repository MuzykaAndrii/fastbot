__all__ = ("router",)

from aiogram import Router

from .create.handlers import router as create_vocabulary_router
from .show.handlers import router as show_vocabulary_router
from .notifications.handlers import router as notifications_vocabulary_router
from .quiz.handlers import router as quiz_vocabulary_router
from .delete.handlers import router as delete_vocabulary_router
from .gen_text.handlers import router as gen_text_router
from .append.handlers import router as append_lang_pairs_router
from .exceptions_handlers import errors_handler_router


router = Router(name=__name__)

router.include_routers(
    create_vocabulary_router,
    show_vocabulary_router,
    notifications_vocabulary_router,
    delete_vocabulary_router,
    gen_text_router,
    append_lang_pairs_router,
    quiz_vocabulary_router,

    errors_handler_router,
)