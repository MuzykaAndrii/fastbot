import logging

from app.backend.auth.protocols import PasswordServiceProtocol
from app.backend.components.unitofwork import UnitOfWork
from app.backend.components.config import app_settings
from app.backend.users.models import User


log = logging.getLogger("backend.users")


class UserService:
    def __init__(self, uow: UnitOfWork, pwd_service: PasswordServiceProtocol) -> None:
        self._uow = uow
        self._pwd_service = pwd_service

    async def get_or_create_by_id(self, id: int) -> User:
        async with self._uow as uow:
            user = await uow.users.get_or_create(id=id)

        return user
    
    async def get_by_id(self, id: int) -> User | None:
        async with self._uow(persistent=False) as uow:
            user = await uow.users.get_by_id(id)

        return user
    
    async def get_by_email(self, email: str) -> User | None:
        async with self._uow(persistent=False) as uow:
            return await uow.users.get_one(email=email)

    async def ensure_admin_exists(self) -> None:
        """Ensures the existence of at least one admin user in the system.
        If no admin users are found, creates a base admin user
        """
        async with self._uow as uow:
            admin_users = await uow.users.get_admin_users()

            if not admin_users:
                await self._create_base_admin_user(uow)
                log.info("Base admin user created")
            else:
                log.info("Admin user found, base admin creating skipped")
    
    @staticmethod
    def user_is_admin(user: User) -> bool:
        return user.is_superuser
    
    async def _create_base_admin_user(self, uow: UnitOfWork) -> None:
        await uow.users.create(
            email=app_settings.BASE_ADMIN_EMAIL,
            password_hash=self._pwd_service.get_hash(app_settings.BASE_ADMIN_PASS),
            is_superuser=True,
        )