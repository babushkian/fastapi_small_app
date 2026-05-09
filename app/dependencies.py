from app.db.database import async_session
from app.uow import UnitOfWork


async def get_uow():
    async with UnitOfWork(async_session) as uow:
        yield uow
