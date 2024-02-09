class QuizError(Exception):
    pass


class QuestionsIsEmptyError(QuizError):
    pass


class QuizItemNotLoadedError(QuizError):
    pass


class QuestionsIsGoneError(QuizError):
    pass