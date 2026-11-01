from collections.abc import AsyncGenerator, Callable

from app.db.database import async_session
from app.interfaces import UnitOfWork
from app.uow import SQLUnitOfWork


def create_uow[T: UnitOfWork](
    uow_class: type[T],
) -> Callable[[], AsyncGenerator[T]]:
    async def dependency() -> AsyncGenerator[T]:
        async with uow_class(async_session) as uow:
            yield uow

    return dependency


get_uow = create_uow(SQLUnitOfWork)
