from typing import Final
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.settings import settings
DATABASE_URL: Final[str] = f"sqlite+aiosqlite:///{settings.DATABASE_PATH}"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


