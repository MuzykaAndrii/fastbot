from contextlib import suppress
from itertools import chain
from random import sample

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.scene import SceneRegistry
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from app.bot.modules.base_quiz.base_quiz import Quiz

from app.bot.modules.base_quiz.exceptions import QuestionsIsGoneError
from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from .callback_patterns import QuizStrategy, VocabularyQuizCallbackData
from .keyboards import SelectQuizTypeKeyboard, get_quiz_keyboard
from . import messages
from app.bot.vocabulary.quiz.question_manager import VocabularyQuestionManager
from app.shared.schemas import LanguagePairSchema
from app.bot.vocabulary.validators import QuizAnswerChecker
from app.vocabulary.services import VocabularyService


router = Router()


@router.callback_query(VocabularyCallbackData.filter(F.action == VocabularyAction.quiz))
async def show_quiz_types(query: CallbackQuery, callback_data: VocabularyCallbackData):
    select_quiz_types_keyboard = SelectQuizTypeKeyboard(callback_data.vocabulary_id).get_markup()
    await query.message.edit_text(messages.select_quiz_type_msg)
    await query.message.edit_reply_markup(reply_markup=select_quiz_types_keyboard)


class QuizScene(Scene, state="quiz"):
    @on.message.enter()
    async def init_global_quiz(self, message: Message, state: FSMContext):
        vocabularies = await VocabularyService.get_all_user_vocabularies(message.from_user.id)

        language_pairs: list[LanguagePairSchema] = list(chain(*(v.language_pairs for v in vocabularies)))
        language_pairs: list[LanguagePairSchema] = sample(language_pairs, len(language_pairs) // len(vocabularies))


        vocabulary_question_manager = VocabularyQuestionManager(language_pairs, QuizStrategy.guess_foreign)
        quiz = Quiz(vocabulary_question_manager)

        await quiz.save_to_state(state)

        await message.answer(messages.start_quiz_msg, reply_markup=get_quiz_keyboard())
        await self.ask_question(message, state)


    @on.callback_query.enter(VocabularyQuizCallbackData)
    async def init_vocabulary_quiz(self, query: CallbackQuery, state: FSMContext):
        callback_data = VocabularyQuizCallbackData.unpack(query.data)
        vocabulary = await VocabularyService.get_vocabulary(query.from_user.id, callback_data.vocabulary_id)

        vocabulary_question_manager = VocabularyQuestionManager(vocabulary.language_pairs, callback_data.quiz_strategy)
        quiz = Quiz(vocabulary_question_manager)

        await quiz.save_to_state(state)

        await query.message.answer(messages.start_quiz_msg, reply_markup=get_quiz_keyboard())
        await self.ask_question(query.message, state)
    

    async def ask_question(self, message: Message, state: FSMContext):
        quiz = await Quiz.load_form_state(state)

        try:
            quiz.load_next_quiz_item()
        except QuestionsIsGoneError:
            return await self.wizard.exit(show_stats=True)

        question_msg = await message.answer(
            messages.quiz_question.format(
                question=quiz.current_question,
                current_question_num=quiz.answered_questions_count,
                total_question_count=quiz.questions_count,
            )
        )

        quiz.last_question_msg = question_msg
        await quiz.save_to_state(state)
    

    @on.message(F.text == "🚪 Leave quiz")
    async def leave_quiz(self, message: Message):
        await message.answer(messages.leave_quiz, reply_markup=ReplyKeyboardRemove())
        return await self.wizard.exit()
    

    @on.message(F.text == "🔁 Skip question")
    async def skip_question(self, message: Message, state: FSMContext) -> None:
        quiz = await Quiz.load_form_state(state)
        quiz.increment_skipped_answers_count()
        
        with suppress(TelegramBadRequest):
            await quiz.last_question_msg.edit_text(messages.quiz_skipped_answer.format(
                word=quiz.current_question,
                translation=quiz.current_answer,
            ))
            await message.delete()

        await quiz.save_to_state(state)
        await self.ask_question(message, state)
    
    @on.message(F.text)
    async def handle_user_answer(self, message: Message, state: FSMContext) -> None:
        quiz = await Quiz.load_form_state(state)

        if QuizAnswerChecker(message.text, quiz.current_answer).is_match():
            answer_response_msg = messages.quiz_success_answer.format(
                word=quiz.current_question,
                translation=quiz.current_answer,
            )
            quiz.increment_correct_answers_count()
        else:
            answer_response_msg = messages.quiz_wrong_answer.format(
                word=quiz.current_question,
                translation=quiz.current_answer,
                suggestion=message.text
            )
            quiz.increment_wrong_answers_count()
        
        with suppress(TelegramBadRequest):
            await quiz.last_question_msg.edit_text(answer_response_msg)
            await message.delete()

        await quiz.save_to_state(state)
        await self.ask_question(message, state)


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
            messages.quiz_stats.format(
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
router.message.register(QuizScene.as_handler(), Command("quiz"))
