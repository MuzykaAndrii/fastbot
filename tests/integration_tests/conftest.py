import pytest

from app.backend.auth.protocols import PasswordServiceProtocol
from app.backend.components.db import database
from app.backend.components import UnitOfWork
from app.backend.users.services import UserService



@pytest.fixture(scope="session")
async def uow() -> UnitOfWork:
    return UnitOfWork(database.session_maker)


class MockPasswordService(PasswordServiceProtocol):
    def get_hash(self, password: str) -> bytes:
        return password.encode('utf-8')
    
    def verify(self, raw_password: str, hashed_password: bytes) -> bool:
        return raw_password.encode('utf-8') == hashed_password


@pytest.fixture(scope="function")
def user_service(uow: UnitOfWork):
    pwd_service = MockPasswordService()
    return UserService(uow=uow, pwd_service=pwd_service)