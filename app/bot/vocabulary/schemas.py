from datetime import datetime
from typing import Any
import random

from pydantic import BaseModel, ConfigDict, Field
from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext

from app.bot.vocabulary.exceptions import LanguagePairsForQuestionsIsEmptyError, QuestionsIsGoneError, QuizItemNotLoadedError


class LanguagePairSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    word: str
    translation: str


class VocabularySetSchema(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime
    language_pairs: list[LanguagePairSchema]


class VocabularyQuiz(BaseModel):
    language_pairs: list[LanguagePairSchema]
    last_question_msg: Message | None = None

    current_question: Any | None = None
    current_answer: Any | None = None

    questions_count: int = 0
    correct_answers_count: int = 0
    wrong_answers_count: int = 0

    def __init__(self, initial: bool, **data) -> None:
        super().__init__(**data)
        
        if initial:
            self._calculate_questions_count()
            self._shuffle_questions()
    
    def _calculate_questions_count(self) -> None:
        self.questions_count = len(self.language_pairs)
    
    def _shuffle_questions(self) -> None:
        random.shuffle(self.language_pairs)
    
    def load_next_quiz_item(self) -> None:
        """
        Loads the next quiz pair as question/answer that can be fetched by 
        current_question or current_answer properties of this instance
        """
        try:
            language_pair = self.language_pairs.pop()
        except IndexError:
            raise QuestionsIsGoneError

        self.current_question = language_pair.translation
        self.current_answer = language_pair.word

    @property
    def current_question(self) -> str:
        if self.current_question is None:
            raise QuizItemNotLoadedError
        else:
            return self.current_question
    
    @property
    def current_answer(self) -> str:
        if self.current_answer is None:
            raise QuizItemNotLoadedError
        else:
            return self.current_answer
    
    def increment_correct_answers_count(self) -> None:
        self.correct_answers_count += 1
    
    def increment_wrong_answers_count(self) -> None:
        self.wrong_answers_count += 1
    
    @property
    def answered_questions_count(self) -> int:
        return self.correct_answers_count + self.wrong_answers_count + 1
    
    @property
    def success_rate(self) -> float:
        try:
            return round(self.correct_answers_count / self.questions_count * 100, 1)
        except ZeroDivisionError:
            raise LanguagePairsForQuestionsIsEmptyError
    
    @classmethod
    async def load_form_state(cls, state: FSMContext):
        state_data = await state.get_data()
        return cls(initial=False, **state_data)
    
    async def save_to_state(self, state: FSMContext) -> None:
        self_as_dict = self.model_dump()
        await state.update_data(**self_as_dict)