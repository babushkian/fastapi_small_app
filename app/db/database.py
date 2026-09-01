from typing import Final
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.settings import settings


engine = create_async_engine(settings.database_url, echo=False, future=True)
async_session = async_sessionmaker[AsyncSession](
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


