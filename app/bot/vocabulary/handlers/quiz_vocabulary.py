import random

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.vocabulary.services import VocabularyService


class QuizScene(Scene, state="quiz"):
    @on.message.enter()
    async def on_enter_msg(self, message: Message, state: FSMContext):
        await self.ask(message, state)


    @on.callback_query.enter(VocabularyCallbackData.filter(F.action == VocabularyAction.quiz))
    async def on_enter_btn(self, query: CallbackQuery, state: FSMContext):
        await query.message.answer("Welcome to the quiz!")
        callback_data = VocabularyCallbackData.unpack(query.data)
        vocabulary = await VocabularyService.get_vocabulary(query.from_user.id, callback_data.vocabulary_id)
        random.shuffle(vocabulary.language_pairs)
        await state.update_data(step=0, language_pairs=vocabulary.language_pairs)

        await self.ask(query.message, state)
    

    async def ask(self, message: Message, state: FSMContext):
        state_data = await state.get_data()
        step = state_data.get("step")
        language_pairs = state_data.get("language_pairs")

        try:
            question_item = language_pairs[step]
        except (IndexError, TypeError):
            return await self.wizard.exit()

        await state.update_data(step=step)
        await message.answer(question_item.translation)
        
    
    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()
        step = state_data.get("step")
        current_pair = state_data.get("language_pairs")[step]

        if current_pair.word != message.text:
            await message.answer(f"Wrong! Correct is: \"{current_pair.word}\"")
        else:
            await message.answer("Youre damn right!")
        
        await state.update_data(step=step+1)
        await self.wizard.retake()


    @on.message()
    async def unknown_message(self, message: Message) -> None:
        await message.answer("Please select an answer.")
    
    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:
        await message.answer("Bye bye!")


router = Router()
router.callback_query.register(QuizScene.as_handler())