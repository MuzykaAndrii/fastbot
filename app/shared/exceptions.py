"""
Since the current architecture of app is monolithic, we emulate the http status codes by exceptions.
When service being divided to multiple apps, exceptions should be changed to http status codes.
"""


class VocabularyError(Exception):
    pass


class VocabularyDoesNotExist(VocabularyError):
    pass


class UserIsNotOwnerOfVocabulary(VocabularyError):
    pass


class VocabularyIsAlreadyActive(VocabularyError):
    pass


class NoVocabulariesFound(VocabularyError):
    pass