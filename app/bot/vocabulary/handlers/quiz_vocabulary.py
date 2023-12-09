import random

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.vocabulary.services import VocabularyService


class QuizScene(Scene, state="quiz"):
    @on.callback_query.enter(VocabularyCallbackData.filter(F.action == VocabularyAction.quiz))
    async def on_enter(self, query: CallbackQuery, state: FSMContext, step: int | None = 0):
        print("entered "*5)
        if not step:
            await query.message.answer("Welcome to the quiz!")
            callback_data = VocabularyCallbackData.unpack(query.data)
            vocabulary = await VocabularyService.get_vocabulary(query.from_user.id, callback_data.vocabulary_id)
            random.shuffle(vocabulary.language_pairs)
            await state.update_data(step=step, language_pairs=vocabulary.language_pairs)
        
        state_data = await state.get_data()
        
        try:
            question_item = state_data.get("language_pairs")[step]
        except IndexError:
            return await self.wizard.exit()

        await state.update_data(step=step)
        await query.message.answer(question_item.translation)
    
    @on.message.enter()
    async def on_enter_msg(self, message: Message, state: FSMContext, step: int | None = 0):
        print("retaked "*10)
    
    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()
        step = state_data.get("step")
        current_pair = state_data.get("language_pairs")[step]

        if current_pair.word != message.text:
            await message.answer(f"Wrong! Correct is: \"{current_pair.word}\"")
        else:
            await message.answer("Youre damn right!")
        
        await self.wizard.retake(step=step+1)


    @on.message()
    async def unknown_message(self, message: Message) -> None:
        await message.answer("Please select an answer.")

router = Router()
router.callback_query.register(QuizScene.as_handler())