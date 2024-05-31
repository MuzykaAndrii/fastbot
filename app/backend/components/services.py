from app.backend.components.unitofwork import UnitOfWork
from app.backend.components.db import database
from app.backend.users.services import UserService
from app.backend.vocabulary.services import VocabularyService


def users_service():
    return UserService(UnitOfWork(database.session_maker))

def vocabularies_service():
    return VocabularyService(UnitOfWork(database.session_maker))