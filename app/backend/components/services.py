from app.backend.components.unitofwork import UnitOfWork
from app.backend.db.session import async_session_maker
from app.backend.users.services import UserService
from app.backend.vocabulary.services import VocabularyService


def users_service() -> UserService:
    uow = UnitOfWork(async_session_maker)
    return UserService(uow)


def vocabularies_service() -> VocabularyService:
    uow = UnitOfWork(async_session_maker)
    return VocabularyService(uow)