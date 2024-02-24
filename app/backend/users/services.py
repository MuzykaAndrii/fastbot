from app.backend.components.unitofwork import UnitOfWork
from app.backend.pwd import PWDService
from app.config import settings
from app.backend.users.models import User


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_or_create_by_id(self, id: int) -> User:
        async with self._uow as uow:
            user = await uow.users.get_or_create(id=id)

        return user
    
    async def get_by_id(self, id: int) -> User | None:
        async with self._uow as uow:
            user = await uow.users.get_one(id=id)

        return user
    
    async def get_by_email(self, email: str) -> User | None:
        async with self._uow as uow:
            return await uow.users.get_one(email=email)

    async def ensure_admin_exists(self) -> None:
        """Ensures the existence of at least one admin user in the system.
        If no admin users are found, creates a base admin user
        """
        async with self._uow as uow:
            admin_users = await uow.users.get_admin_users()

            if not admin_users:
                await self._create_base_admin_user(uow)
    
    @staticmethod
    def user_is_admin(user: User) -> bool:
        return user.is_superuser
    
    async def _create_base_admin_user(self, uow: UnitOfWork) -> None:
        await uow.users.create(
            email=settings.BASE_ADMIN_EMAIL,
            password_hash=PWDService.get_password_hash(settings.BASE_ADMIN_PASS),
            is_superuser=True,
        )