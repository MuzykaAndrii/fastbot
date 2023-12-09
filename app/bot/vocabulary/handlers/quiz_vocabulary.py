from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, SceneRegistry, ScenesManager, on

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.vocabulary.services import VocabularyService


class QuizScene(Scene, state="quiz"):
    @on.callback_query.enter(VocabularyCallbackData.filter(F.action == VocabularyAction.quiz))
    async def on_enter(self, query: CallbackQuery, callback_data: VocabularyCallbackData, state: FSMContext, step: int | None = 0):
        if not step:
            await query.message.answer("Welcome to the quiz!")
        
        print(query)
        
        # questions = await VocabularyService.get_vocabulary()


router = Router()
router.callback_query.register(QuizScene.as_handler())
scene_registry = SceneRegistry(router)
scene_registry.add(QuizScene)