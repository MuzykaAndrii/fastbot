from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.keyboards import get_quiz_keyboard
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.schemas import LanguagePairSchema
from app.bot.vocabulary.validators import QuizAnswerChecker
from app.vocabulary.services import VocabularyService
from app.bot.vocabulary.schemas import VocabularyQuiz

class QuizScene(Scene, state="quiz"):
    @on.message.enter()
    async def on_enter_msg(self, message: Message, state: FSMContext):
        await self.ask_question(message, state)


    @on.callback_query.enter(VocabularyCallbackData.filter(F.action == VocabularyAction.quiz))
    async def on_enter_btn(self, query: CallbackQuery, state: FSMContext):
        callback_data = VocabularyCallbackData.unpack(query.data)
        vocabulary = await VocabularyService.get_vocabulary(query.from_user.id, callback_data.vocabulary_id)

        quiz = VocabularyQuiz(initial=True, language_pairs=vocabulary.language_pairs)
        await quiz.save_to_state(state)

        await query.message.answer(VocabularyMessages.start_quiz_msg, reply_markup=get_quiz_keyboard())
        await self.ask_question(query.message, state)
    

    async def ask_question(self, message: Message, state: FSMContext):
        state_data = await state.get_data()
        language_pairs = state_data.get("language_pairs")
        questions__count = state_data.get("questions_count")
        correct_answers_count = state_data.get("correct_answers_count")
        wrong_answers_count = state_data.get("wrong_answers_count")

        answered_questions_count = correct_answers_count + wrong_answers_count + 1

        try:
            question_item = language_pairs.pop()
        except IndexError:
            return await self.wizard.exit(show_stats=True)

        last_question_msg = await message.answer(
            VocabularyMessages.quiz_question.format(
                answered=answered_questions_count,
                total=questions__count,
                word=question_item.translation,
            )
        )
        await state.update_data(last_question_msg=last_question_msg, current_language_pair=question_item)
    

    @on.message(F.text == "🚪 Leave quiz")
    async def leave_quiz(self, message: Message):
        await message.answer(VocabularyMessages.leave_quiz, reply_markup=ReplyKeyboardRemove())
        return await self.wizard.exit()
        
    
    @on.message(F.text)
    async def handle_user_answer(self, message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()
        correct_answers_count = state_data.get("correct_answers_count")
        wrong_answers_count = state_data.get("wrong_answers_count")
        last_question_msg: Message = state_data.get("last_question_msg")
        current_language_pair: LanguagePairSchema = state_data.get("current_language_pair")

        answer_checker = QuizAnswerChecker(message.text, current_language_pair.word)
        if answer_checker.check_correctness():
            answer_response_msg = VocabularyMessages.quiz_success_answer.format(
                word=message.text,
                translation=current_language_pair.translation,
            )
            correct_answers_count += 1
        else:
            answer_response_msg = VocabularyMessages.quiz_wrong_answer.format(
                word=current_language_pair.word,
                translation=current_language_pair.translation,
                suggestion=message.text
            )
            wrong_answers_count += 1
        
        await last_question_msg.edit_text(answer_response_msg)
        await message.delete()
        await state.update_data(
            correct_answers_count=correct_answers_count,
            wrong_answers_count=wrong_answers_count
        )
        await self.wizard.retake()


    @on.message()
    async def unknown_message(self, message: Message) -> None:
        await message.answer("I dont get what u mean 🤯. Please send an answer ⬇️.")
    

    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext, show_stats=False) -> None:
        if show_stats:
            await self.show_stats(message, state)
    

    async def show_stats(self, message: Message, state: FSMContext):
        state_data = await state.get_data()

        correct_answers_count = state_data.get("correct_answers_count")
        wrong_answers_count = state_data.get("wrong_answers_count")
        questions_count = state_data.get("questions_count")

        success_rate = round(correct_answers_count / questions_count * 100, 1)

        await message.answer(
            VocabularyMessages.quiz_stats.format(
                correct_guesses=correct_answers_count,
                wrong_guesses=wrong_answers_count,
                success_rate=success_rate,
                total_words_attempted=questions_count,
            ),
            reply_markup=ReplyKeyboardRemove(),
        )


router = Router()
router.callback_query.register(QuizScene.as_handler())