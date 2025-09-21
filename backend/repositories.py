from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import Student, Course

class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[Student]:
        return await self.session.get(Student, id)

    async def get_with_courses(self, id: int) -> Optional[Student]:
        stmt = select(Student).options(selectinload(Student.courses)).filter_by(id=id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get_by_name(self, name: str) -> Optional[Student]:
        print("Поиск студента по имени")
        stmt = select(Student).filter_by(name=name).options(selectinload(Student.courses))
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def list(self) -> List[Student]:
        stmt = select(Student).options(selectinload(Student.courses))
        res = await self.session.execute(stmt)
        return res.scalars().unique().all()

    async def add(self, student: Student) -> Student:
        self.session.add(student)
        await self.session.flush()
        return student

    async def remove(self, student: Student) -> None:
        # session.delete is synchronous API; it schedules deletion
        await self.session.delete(student)
        await self.session.flush()


class CourseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[Course]:
        return await self.session.get(Course, id)

    async def get_with_students(self, id: int) -> Optional[Course]:
        stmt = select(Course).options(selectinload(Course.students)).filter_by(id=id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get_by_title(self, title: str) -> Optional[Course]:
        stmt = select(Course).filter_by(title=title)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def list(self) -> List[Course]:
        stmt = select(Course).options(selectinload(Course.students))
        res = await self.session.execute(stmt)
        return res.scalars().unique().all()

    async def add(self, course: Course) -> Course:
        self.session.add(course)
        await self.session.flush()
        return course

    async def remove(self, course: Course) -> None:
        await self.session.delete(course)
        await self.session.flush()