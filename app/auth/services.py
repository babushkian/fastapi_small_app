from collections.abc import Sequence

from app.auth import models
from app.auth.schemas import UserCreate, UserRead
from app.exceptions import AlreadyExistsError, NotFoundError
from app.interfaces import UnitOfWork


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, dto: UserCreate) -> models.User:
        user = models.User(
            username=dto.username,
            hashed_password=dto.password,
            is_active=True,
            token_version=1,
        )
        await self.uow.users.add(user)
        await self.uow.commit()
        return user

    async def list(self) -> Sequence[models.User]:
        return await self.uow.users.list()
