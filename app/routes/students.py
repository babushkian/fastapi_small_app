
import logging
from fastapi import  Depends, status, APIRouter
from fastapi.responses import Response

from app.dependencies import get_uow
from app.uow import UnitOfWork
from app import schemas
from app import services


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("app")

router =  APIRouter()


@router.post("/", response_model=schemas.StudentNew, status_code=status.HTTP_201_CREATED)
async def create_student(student_in: schemas.StudentCreate, uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    student = await svc.create_student(student_in)
    logger.info("Created student id=%s name=%s", student.id, student.name)
    return student


@router.get("/", response_model=list[schemas.Student])
async def list_students(uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    return await svc.list_students()


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    await svc.delete_student(student_id)
    logger.info("Deleted student id=%s", student_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/enroll/{student_id}/{course_id}", response_model=schemas.Student)
async def enroll(student_id: int, course_id: int, uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    student = await svc.enroll(student_id, course_id)
    logger.info("Enrolled student=%s to course=%s", student_id, course_id)
    return student


@router.delete("/{student_id}/courses/{course_id}", response_model=schemas.Student)
async def unenroll(student_id: int, course_id: int, uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    student = await svc.unenroll(student_id, course_id)
    logger.info("Unenrolled student=%s from course=%s", student_id, course_id)
    return student
