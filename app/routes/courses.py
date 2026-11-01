import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response

from app import schemas, services
from app.dependencies import get_uow
from app.interfaces import UnitOfWork

router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("app")


@router.get("/", response_model=list[schemas.Course])
async def list_courses(uow: Annotated[UnitOfWork, Depends(get_uow)]):
    svc = services.CourseService(uow)
    return await svc.list_courses()


@router.post("/", response_model=schemas.Course, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: schemas.CourseCreate, uow: Annotated[UnitOfWork, Depends(get_uow)]
):
    svc = services.CourseService(uow)
    course = await svc.create_course(course_in)
    logger.info("Created course id=%s title=%s", course.id, course.title)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, uow: Annotated[UnitOfWork, Depends(get_uow)]):
    svc = services.CourseService(uow)
    await svc.delete_course(course_id)
    logger.info("Deleted course id=%s", course_id)
    return Response(status_code=204)
