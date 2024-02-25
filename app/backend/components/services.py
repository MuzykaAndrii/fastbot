from app.backend.components.unitofwork import UnitOfWork
from app.backend.db.session import async_session_maker
from app.backend.users.services import UserService
from app.backend.vocabulary.services import VocabularyService


def users_service():
    return UserService(UnitOfWork(async_session_maker))

def vocabularies_service():
    return VocabularyService(UnitOfWork(async_session_maker))