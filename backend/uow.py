from typing import Optional
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from repositories import StudentRepository, CourseRepository
from auth.repository import UserRepository

class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory
        self.session: Optional[AsyncSession] = None
        self.students: Optional[StudentRepository] = None
        self.courses: Optional[CourseRepository] = None
        # self.users: Optional[UserRepository] = None

    async def __aenter__(self):
        self.session = self._session_factory()
        self.students = StudentRepository(self.session)
        self.courses = CourseRepository(self.session)
        # self.users = UserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()