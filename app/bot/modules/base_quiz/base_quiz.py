from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass

from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext

from .exceptions import QuestionsIsEmptyError, QuestionsIsGoneError, QuizItemNotLoadedError


@dataclass(frozen=True, slots=True)
class QuestionItem:
    question: str
    answer: str


class QuestionManager(ABC):
    @abstractmethod
    def get_question_item(self) -> QuestionItem:
        pass


class Quiz:
    def __init__(
        self,
        question_manager: QuestionManager,
        last_question_msg: Message | None = None,
        current_question: str | None = None,
        current_answer: str | None = None,
        correct_answers_count: int = 0,
        wrong_answers_count: int = 0,
        skipped_answers_count: int = 0,
    ) -> None:
        self.question_manager = question_manager
        self.last_question_msg = last_question_msg
        self._current_question = current_question
        self._current_answer = current_answer
        self.correct_answers_count = correct_answers_count
        self.wrong_answers_count = wrong_answers_count
        self.skipped_answers_count = skipped_answers_count
        

    def load_next_quiz_item(self) -> None:
        """
        Loads the next quiz pair as question/answer that can be fetched by 
        current_question or current_answer properties of this instance.
        raises QuestionsIsGoneError if questions is empty
        """
        try:
            quiz_item = self.question_manager.get_question_item()
        except QuestionsIsGoneError as e:
            raise e

        self._current_question = quiz_item.question
        self._current_answer = quiz_item.answer
    
    @property
    def questions_count(self):
        return self.question_manager.questions_count

    @property
    def current_question(self) -> str:
        if self._current_question is None:
            raise QuizItemNotLoadedError
        else:
            return self._current_question
    
    @property
    def current_answer(self) -> str:
        if self._current_answer is None:
            raise QuizItemNotLoadedError
        else:
            return self._current_answer
    
    def increment_correct_answers_count(self) -> None:
        self.correct_answers_count += 1
    
    def increment_wrong_answers_count(self) -> None:
        self.wrong_answers_count += 1
    
    def increment_skipped_answers_count(self) -> None:
        self.skipped_answers_count += 1
    
    @property
    def answered_questions_count(self) -> int:
        return self.correct_answers_count + self.wrong_answers_count + self.skipped_answers_count + 1
    
    @property
    def success_rate(self) -> float:
        try:
            return round(self.correct_answers_count / self.questions_count * 100, 1)
        except ZeroDivisionError:
            raise QuestionsIsEmptyError
    
    @classmethod
    async def load_form_state(cls, state: FSMContext):
        state_data = await state.get_data()
        return cls(**state_data)
    
    def dump(self) -> dict[str, Any]:
        return {
            "question_manager": self.question_manager,
            "last_question_msg": self.last_question_msg,
            "current_question": self._current_question,
            "current_answer": self._current_answer,
            "correct_answers_count": self.correct_answers_count,
            "wrong_answers_count": self.wrong_answers_count,
            "skipped_answers_count": self.skipped_answers_count,
        }
    
    async def save_to_state(self, state: FSMContext) -> None:
        await state.update_data(**self.dump())