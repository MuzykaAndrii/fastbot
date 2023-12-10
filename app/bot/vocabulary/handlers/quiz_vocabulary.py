import random

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.schemas import LanguagePairSchema
from app.bot.vocabulary.validators import QuizAnswerChecker
from app.vocabulary.services import VocabularyService


class QuizScene(Scene, state="quiz"):
    @on.message.enter()
    async def on_enter_msg(self, message: Message, state: FSMContext):
        await self.ask(message, state)


    @on.callback_query.enter(VocabularyCallbackData.filter(F.action == VocabularyAction.quiz))
    async def on_enter_btn(self, query: CallbackQuery, state: FSMContext):
        await query.message.answer(VocabularyMessages.start_quiz_msg)
        callback_data = VocabularyCallbackData.unpack(query.data)
        vocabulary = await VocabularyService.get_vocabulary(query.from_user.id, callback_data.vocabulary_id)
        random.shuffle(vocabulary.language_pairs)
        await state.update_data(
            step=0,
            language_pairs=vocabulary.language_pairs,
            correct_answers_count=0,
            wrong_answers_count=0
        )

        await self.ask(query.message, state)
    

    async def ask(self, message: Message, state: FSMContext):
        state_data = await state.get_data()
        step = state_data.get("step")
        language_pairs = state_data.get("language_pairs")

        try:
            question_item = language_pairs[step]
        except (IndexError, TypeError):
            return await self.wizard.exit()

        last_question_msg = await message.answer(VocabularyMessages.quiz_question.format(word=question_item.translation))
        await state.update_data(step=step, last_question_msg=last_question_msg)
        
    
    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()
        step = state_data.get("step")
        correct_answers_count = state_data.get("correct_answers_count")
        wrong_answers_count = state_data.get("wrong_answers_count")
        last_question_msg: Message = state_data.get("last_question_msg")
        current_pair: LanguagePairSchema = state_data.get("language_pairs")[step]

        answer_checker = QuizAnswerChecker(message.text, current_pair.word)
        if answer_checker.check_correctness():
            answer_response_msg = VocabularyMessages.quiz_success_answer.format(
                word=message.text,
                translation=current_pair.translation,
            )
            correct_answers_count += 1
        else:
            answer_response_msg = VocabularyMessages.quiz_wrong_answer.format(
                word=current_pair.word,
                translation=current_pair.translation,
                suggestion=message.text
            )
            wrong_answers_count += 1
        
        await message.delete()
        await last_question_msg.edit_text(answer_response_msg)
        await state.update_data(
            step=step+1,
            correct_answers_count=correct_answers_count,
            wrong_answers_count=wrong_answers_count
        )
        await self.wizard.retake()


    @on.message()
    async def unknown_message(self, message: Message) -> None:
        await message.answer("I dont get what u mean 🤯. Please send an answer ⬇️.")
    
    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()

        correct_answers_count = state_data.get("correct_answers_count")
        wrong_answers_count = state_data.get("wrong_answers_count")
        pairs: list[LanguagePairSchema] = state_data.get("language_pairs")

        questions_count = len(pairs)
        success_rate = round(correct_answers_count / questions_count * 100, 1)

        await message.answer(VocabularyMessages.quiz_stats.format(
            correct_guesses=correct_answers_count,
            wrong_guesses=wrong_answers_count,
            success_rate=success_rate,
            total_words_attempted=questions_count,
        ))


router = Router()
router.callback_query.register(QuizScene.as_handler())