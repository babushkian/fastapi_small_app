from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.auth.repository import UserRepository
from app.interfaces import CourseRepositoryInterface, StudentRepositoryInterface
from app.repositories import CourseRepository, StudentRepository


class SQLUnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()
        self.students = StudentRepository(self.session)
        self.courses = CourseRepository(self.session)
        self.users = UserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                await self.rollback()
        finally:
            if self.session is not None:
                await self.session.close()

    async def commit(self):
        if self.session is not None:
            await self.session.commit()

    async def rollback(self):
        if self.session is not None:
            await self.session.rollback()
    
