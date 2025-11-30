from typing import List
import schemas
from student_course import models


from uow import UnitOfWork
from exceptions import NotFoundError, AlreadyExistsError

class StudentService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_student(self, dto: schemas.StudentCreate) -> models.student.Student:
        existing = await self.uow.students.get_by_name(dto.name)
        if existing:
            raise AlreadyExistsError("student already exists")
        print("подготовка к созданию студента")
        student = models.student.Student(name=dto.name)
        print("объект студента", student)
        await self.uow.students.add(student)
        return student

    async def list_students(self) -> List[models.student.Student]:
        return await self.uow.students.list()

    async def enroll(self, student_id: int, course_id: int) -> models.student.Student:
        student = await self.uow.students.get_with_courses(student_id)
        course = await self.uow.courses.get(course_id)
        if not student or not course:
            raise NotFoundError("student or course not found")
        if course not in student.courses:
            student.courses.append(course)
            await self.uow.session.flush()
        return await self.uow.students.get_with_courses(student_id)

    async def unenroll(self, student_id: int, course_id: int) -> models.student.Student:
        student = await self.uow.students.get_with_courses(student_id)
        if not student:
            raise NotFoundError("student not found")
        # find course in student's courses (loaded via selectin)
        course = next((c for c in student.courses if c.id == course_id), None)
        if not course:
            raise NotFoundError("enrollment not found")
        student.courses.remove(course)
        await self.uow.session.flush()
        return await self.uow.students.get_with_courses(student_id)

    async def delete_student(self, student_id: int) -> None:
        student = await self.uow.students.get(student_id)
        if not student:
            raise NotFoundError("student not found")
        await self.uow.students.remove(student)


class CourseService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_course(self, dto: schemas.CourseCreate) -> models.course.Course:
        existing = await self.uow.courses.get_by_title(dto.title)
        if existing:
            raise AlreadyExistsError("course already exists")
        course = models.course.Course(title=dto.title)
        await self.uow.courses.add(course)
        return course

    async def list_courses(self) -> List[models.course.Course]:
        return await self.uow.courses.list()

    async def delete_course(self, course_id: int) -> None:
        course = await self.uow.courses.get(course_id)
        if not course:
            raise NotFoundError("course not found")
        await self.uow.courses.remove(course)
