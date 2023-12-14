class VocabularyError(Exception):
    pass


class QuizError(VocabularyError):
    pass


class LanguagePairsForQuestionsIsEmptyError(QuizError):
    pass


class QuizItemNotLoadedError(QuizError):
    pass


class QuestionsIsGoneError(QuizError):
    pass