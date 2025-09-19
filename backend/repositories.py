from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import models

class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[models.Student]:
        return await self.session.get(models.Student, id)

    async def get_with_courses(self, id: int) -> Optional[models.Student]:
        stmt = select(models.Student).options(selectinload(models.Student.courses)).filter_by(id=id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get_by_name(self, name: str) -> Optional[models.Student]:
        print("Поиск студента по имени")
        stmt = select(models.Student).filter_by(name=name).options(selectinload(models.Student.courses))
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def list(self) -> List[models.Student]:
        stmt = select(models.Student).options(selectinload(models.Student.courses))
        res = await self.session.execute(stmt)
        return res.scalars().unique().all()

    async def add(self, student: models.Student) -> models.Student:
        self.session.add(student)
        await self.session.flush()
        return student

    async def remove(self, student: models.Student) -> None:
        # session.delete is synchronous API; it schedules deletion
        await self.session.delete(student)
        await self.session.flush()


class CourseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[models.Course]:
        return await self.session.get(models.Course, id)

    async def get_with_students(self, id: int) -> Optional[models.Course]:
        stmt = select(models.Course).options(selectinload(models.Course.students)).filter_by(id=id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get_by_title(self, title: str) -> Optional[models.Course]:
        stmt = select(models.Course).filter_by(title=title)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def list(self) -> List[models.Course]:
        stmt = select(models.Course).options(selectinload(models.Course.students))
        res = await self.session.execute(stmt)
        return res.scalars().unique().all()

    async def add(self, course: models.Course) -> models.Course:
        self.session.add(course)
        await self.session.flush()
        return course

    async def remove(self, course: models.Course) -> None:
        await self.session.delete(course)
        await self.session.flush()