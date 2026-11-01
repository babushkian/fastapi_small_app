from collections.abc import AsyncGenerator

from app.db.database import async_session
from app.interfaces import UnitOfWork
from app.uow import SQLUnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork]:
    async with SQLUnitOfWork(async_session) as uow:
        yield uow
