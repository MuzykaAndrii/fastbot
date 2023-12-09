from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.vocabulary.services import VocabularyService


class QuizScene(Scene, state="quiz"):
    @on.callback_query.enter(VocabularyCallbackData.filter(F.action == VocabularyAction.quiz))
    async def on_enter(self, query: CallbackQuery, state: FSMContext, step: int | None = 0):
        print(query, state, step, sep="\n\n")


router = Router()
router.callback_query.register(QuizScene.as_handler())