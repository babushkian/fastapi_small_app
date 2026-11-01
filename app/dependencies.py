from collections.abc import AsyncGenerator

from app.db.database import async_session
from app.uow import SQLUnitOfWork
from app.interfaces import UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork]:
    async with SQLUnitOfWork(async_session) as uow:
        yield uow
