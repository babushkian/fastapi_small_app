from sqlalchemy import select
from typing import Optional
from auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession



class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[User]:
        return await self.session.get(User, id)

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).filter_by(username=username)
        res = await self.session.execute(stmt)
        return res.scalars().first()


    async def add(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user


    async def list(self) -> list[User]:
        stmt = select(User)
        result = await self.session.execute(stmt)
        return  result.scalars().all()

    async def increment_token_version(self, user: User) -> None:
        user.token_version += 1
        await self.session.flush()
