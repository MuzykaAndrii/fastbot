from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.bot.vocabulary.quiz.callback_patterns import QuizStrategy, VocabularyQuizCallbackData


def get_quiz_keyboard():
    btn_end_test = KeyboardButton(text="🚪 Leave quiz")
    btn_skip_question = KeyboardButton(text="🔁 Skip question")

    quiz_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [btn_end_test, btn_skip_question],
        ],
        resize_keyboard=True,
    )
    return quiz_keyboard


class SelectQuizTypeKeyboard:
    def __init__(self, vocabulary_id) -> None:
        self.vocabulary_id = vocabulary_id
    

    def get_markup(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [self.btn_guess_foreign],
            [self.btn_guess_native],
            [self.btn_guess_combined],
        ])

        return keyboard

    @property
    def btn_guess_foreign(self):
        return InlineKeyboardButton(
            text="Translate from Native to Foreign",
            callback_data=self._make_callback_data(QuizStrategy.guess_foreign),
        )
    
    @property
    def btn_guess_native(self):
        return InlineKeyboardButton(
            text="Translate from Foreign to Native",
            callback_data=self._make_callback_data(QuizStrategy.guess_native),
        )
    
    @property
    def btn_guess_combined(self):
        return InlineKeyboardButton(
            text="Mixed mode",
            callback_data=self._make_callback_data(QuizStrategy.combined),
        )
    
    def _make_callback_data(self, strategy: QuizStrategy):
        callback_data = VocabularyQuizCallbackData(
            quiz_strategy=strategy,
            vocabulary_id=self.vocabulary_id,
        )
        return callback_data.pack()