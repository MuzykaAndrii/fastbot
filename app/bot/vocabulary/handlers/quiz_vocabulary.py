from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.scene import SceneRegistry

from app.bot.modules.base_quiz import Quiz
from app.bot.vocabulary.callback_patterns import StartQuizCallbackData, VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.exceptions import QuestionsIsGoneError
from app.bot.vocabulary.keyboards import QuizTypesKeyboard, get_quiz_keyboard
from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.question_manager import VocabularyQuestionManager
from app.bot.vocabulary.validators import QuizAnswerChecker
from app.vocabulary.services import VocabularyService


router = Router()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.quiz))
async def show_quiz_types(query: CallbackQuery, callback_data: VocabularyCallbackData):
    select_quiz_types_keyboard = QuizTypesKeyboard(callback_data.vocabulary_id).get_markup()
    await query.message.edit_text(VocabularyMessages.select_quiz_type_msg)
    await query.message.edit_reply_markup(reply_markup=select_quiz_types_keyboard)


class QuizScene(Scene, state="quiz"):
    @on.message.enter()
    async def ask_next_question(self, message: Message, state: FSMContext):
        await self.ask_question(message, state)


    @on.callback_query.enter(StartQuizCallbackData)
    async def start_quiz(self, query: CallbackQuery, state: FSMContext):
        callback_data = StartQuizCallbackData.unpack(query.data)
        vocabulary = await VocabularyService.get_vocabulary(query.from_user.id, callback_data.vocabulary_id)

        vocabulary_question_manager = VocabularyQuestionManager(vocabulary.language_pairs, callback_data.quiz_strategy)
        quiz = Quiz(vocabulary_question_manager)

        await quiz.save_to_state(state)

        await query.message.answer(VocabularyMessages.start_quiz_msg, reply_markup=get_quiz_keyboard())
        await self.ask_question(query.message, state)
    

    async def ask_question(self, message: Message, state: FSMContext):
        quiz = await Quiz.load_form_state(state)

        try:
            quiz.load_next_quiz_item()
        except QuestionsIsGoneError:
            return await self.wizard.exit(show_stats=True)

        question_msg = await message.answer(
            VocabularyMessages.quiz_question.format(
                question=quiz.current_question,
                current_question_num=quiz.answered_questions_count,
                total_question_count=quiz.questions_count,
            )
        )

        quiz.last_question_msg = question_msg
        await quiz.save_to_state(state)
    

    @on.message(F.text == "🚪 Leave quiz")
    async def leave_quiz(self, message: Message):
        await message.answer(VocabularyMessages.leave_quiz, reply_markup=ReplyKeyboardRemove())
        return await self.wizard.exit()
    

    @on.message(F.text == "🔁 Skip question")
    async def skip_question(self, message: Message, state: FSMContext) -> None:
        quiz = await Quiz.load_form_state(state)
        quiz.increment_skipped_answers_count()

        await quiz.last_question_msg.edit_text(VocabularyMessages.quiz_skipped_answer.format(
            word=quiz.current_question,
            translation=quiz.current_answer,
        ))
        await message.delete()

        await quiz.save_to_state(state)
        await self.wizard.retake()
    
    @on.message(F.text)
    async def handle_user_answer(self, message: Message, state: FSMContext) -> None:
        quiz = await Quiz.load_form_state(state)

        if QuizAnswerChecker(message.text, quiz.current_answer).is_match():
            answer_response_msg = VocabularyMessages.quiz_success_answer.format(
                word=quiz.current_question,
                translation=quiz.current_answer,
            )
            quiz.increment_correct_answers_count()
        else:
            answer_response_msg = VocabularyMessages.quiz_wrong_answer.format(
                word=quiz.current_question,
                translation=quiz.current_answer,
                suggestion=message.text
            )
            quiz.increment_wrong_answers_count()
                
        await quiz.last_question_msg.edit_text(answer_response_msg)
        await message.delete()

        await quiz.save_to_state(state)
        await self.wizard.retake()


    @on.message()
    async def handle_unknown_message(self, message: Message) -> None:
        await message.answer("I dont get what u mean 🤯. Please send an answer ⬇️.")
    

    @on.message.exit()
    async def exit_from_quiz(self, message: Message, state: FSMContext, show_stats=False) -> None:
        if show_stats:
            await self.show_stats(message, state)
    

    async def show_stats(self, message: Message, state: FSMContext):
        quiz = await Quiz.load_form_state(state)

        await message.answer(
            VocabularyMessages.quiz_stats.format(
                correct_guesses=quiz.correct_answers_count,
                wrong_guesses=quiz.wrong_answers_count,
                skipped_answers=quiz.skipped_answers_count,
                success_rate=quiz.success_rate,
                total_words_attempted=quiz.questions_count,
            ),
            reply_markup=ReplyKeyboardRemove(),
        )


scene_registry = SceneRegistry(router)
scene_registry.add(QuizScene)
router.callback_query.register(QuizScene.as_handler())
