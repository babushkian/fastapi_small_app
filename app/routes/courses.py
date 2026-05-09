import logging
from fastapi import Depends, status, APIRouter
from fastapi.responses import JSONResponse, Response

from app.dependencies import get_uow
from app.uow import UnitOfWork
from app import schemas
from app import services


router =  APIRouter()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("app")

@router.get("/courses/", response_model=list[schemas.Course])
async def list_courses(uow: UnitOfWork = Depends(get_uow)):
    svc = services.CourseService(uow)
    return await svc.list_courses()


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, uow: UnitOfWork = Depends(get_uow)):
    svc = services.CourseService(uow)
    await svc.delete_course(course_id)
    logger.info("Deleted course id=%s", course_id)
    return Response(status_code=204)
