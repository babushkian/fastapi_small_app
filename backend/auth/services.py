

from uow import UnitOfWork
from exceptions import NotFoundError, AlreadyExistsError
from auth import models
from auth.schemas import UserCreate, UserRead
class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, dto: UserCreate) -> models.User:
        user = models.User(username=dto.username,
                           hashed_password=dto.password,
                           is_active=True,
                           token_version=1
                           )
        await self.uow.users.add(user)
        return user


    async def list(self) -> list[models.User]:
        return await self.uow.users.list()

