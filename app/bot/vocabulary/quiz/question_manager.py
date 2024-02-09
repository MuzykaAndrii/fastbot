import random

from app.bot.modules.base_quiz.base_quiz import QuestionItem, QuestionManager
from app.bot.modules.base_quiz.exceptions import QuestionsIsGoneError
from app.bot.vocabulary.quiz.callback_patterns import QuizStrategy
from app.shared.schemas import LanguagePairSchema


class VocabularyQuestionManager(QuestionManager):
    def __init__(
        self,
        language_pairs: list[LanguagePairSchema],
        quiz_strategy: QuizStrategy,
    ) -> None:
        self._language_pairs = language_pairs
        self._strategy = quiz_strategy
        self._calculate_questions_count()
        self._shuffle_questions()
    
    def _shuffle_questions(self) -> None:
        random.shuffle(self._language_pairs)
        
    def _calculate_questions_count(self):
        self.questions_count = len(self._language_pairs)
    
    def _parse_language_pair_to_question_item(self, language_pair: LanguagePairSchema) -> QuestionItem:
        match self._strategy:
            case QuizStrategy.guess_native:
                question = language_pair.word
                answer = language_pair.translation
            
            case QuizStrategy.guess_foreign:
                question = language_pair.translation
                answer = language_pair.word
            
            case QuizStrategy.combined:
                question, answer = random.sample([language_pair.word, language_pair.translation], 2)
            
            case _:
                raise ValueError
        
        return QuestionItem(question=question, answer=answer)
    
    def get_question_item(self) -> QuestionItem:
        try:
            language_pair = self._language_pairs.pop()
        except IndexError:
            raise QuestionsIsGoneError
        
        q_item = self._parse_language_pair_to_question_item(language_pair)
        return q_item