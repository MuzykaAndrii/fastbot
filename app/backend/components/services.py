from app.backend.components.unitofwork import UnitOfWork
from app.backend.db.session import async_session_maker
from app.backend.users.services import UserService
from app.backend.vocabulary.services import VocabularyService


users_service = UserService(UnitOfWork(async_session_maker))
vocabularies_service = VocabularyService(UnitOfWork(async_session_maker))