from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.bot.vocabulary.callback_patterns import QuizStrategy, StartQuizCallbackData, VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.schemas import VocabularySetSchema


def get_select_strategy_keyboard():
    btn_bulk = KeyboardButton(text="Bulk")
    btn_line_by_line = KeyboardButton(text="Line by line")
    btn_cancel = KeyboardButton(text="Cancel")

    select_strategy_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [btn_bulk, btn_line_by_line],
            [btn_cancel],
        ],
        resize_keyboard=True,
    )

    return select_strategy_keyboard

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


class ActionsKeyboard:
    def __init__(self, vocabulary: VocabularySetSchema) -> None:
        self.vocabulary = vocabulary
    
    def get_markup(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [self.delete_btn, self.quiz_btn],
            [self.notification_btn],
            [self.move_backward_btn, self.move_forward_btn],
        ])

        return keyboard

    @property
    def quiz_btn(self):
        return InlineKeyboardButton(
            text="📝 Start quiz",
            callback_data=self._make_callback_data(VocabularyAction.quiz)
        )
    
    @property
    def move_forward_btn(self):
        return InlineKeyboardButton(
            text="Next ⏩",
            callback_data=self._make_callback_data(VocabularyAction.move_forward),
        )
    
    @property
    def move_backward_btn(self):
        return InlineKeyboardButton(
            text="⏪ Prev",
            callback_data=self._make_callback_data(VocabularyAction.move_backward),
        )
    
    @property
    def delete_btn(self):
        return InlineKeyboardButton(
            text="❌ Delete",
            callback_data=self._make_callback_data(VocabularyAction.delete),
        )
    
    @property
    def enable_notification_btn(self):
        return InlineKeyboardButton(
            text="🕝 Enable alerts",
            callback_data=self._make_callback_data(VocabularyAction.enable_notification),
        )

    @property
    def disable_notification_btn(self):
        return InlineKeyboardButton(
            text="📵 Disable alerts",
            callback_data=self._make_callback_data(VocabularyAction.disable_notification),
        )
    
    @property
    def notification_btn(self):
        if self.vocabulary.is_active:
            return self.disable_notification_btn
        else:
            return self.enable_notification_btn
    
    def _make_callback_data(self, action: VocabularyAction):
        callback_data = VocabularyCallbackData(
            action=action,
            vocabulary_id=self.vocabulary.id,
        )
        return callback_data.pack()


class QuizTypesKeyboard:
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
        callback_data = StartQuizCallbackData(
            quiz_strategy=strategy,
            vocabulary_id=self.vocabulary_id,
        )
        return callback_data.pack()