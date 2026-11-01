from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.student_course.models import Course, Student


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Student | None:
        return await self.session.get(Student, id)

    async def get_with_courses(self, id: int) -> Student | None:
        stmt = select(Student).options(selectinload(Student.courses)).filter_by(id=id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get_by_name(self, name: str) -> Student | None:
        print("Поиск студента по имени")
        stmt = select(Student).filter_by(name=name).options(selectinload(Student.courses))
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def list(self) -> Sequence[Student]:
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

    async def get(self, id: int) -> Course | None:
        return await self.session.get(Course, id)

    async def get_with_students(self, id: int) -> Course | None:
        stmt = select(Course).options(selectinload(Course.students)).filter_by(id=id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get_by_title(self, title: str) -> Course | None:
        stmt = select(Course).filter_by(title=title)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def list(self) -> Sequence[Course]:
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