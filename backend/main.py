import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from db.base import Base
from dependencies import get_uow
from uow import UnitOfWork
import schemas, services, exceptions
from auth.routes import router as auth_router


# logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting app — creating DB schema if needed")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(Base.metadata)
    try:
        yield
    finally:
        logger.info("Shutting down — disposing engine")
        await engine.dispose()

app = FastAPI(title="Async FastAPI + SQLAlchemy (UoW/Repo/Service)", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # любой домен
    allow_credentials=False,  # без cookies
    allow_methods=["*"],      # все методы (GET, POST и т.д.)
    allow_headers=["*"],      # все заголовки
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])

# custom exception handlers
@app.exception_handler(exceptions.NotFoundError)
async def not_found_handler(request, exc: exceptions.NotFoundError):
    return JSONResponse({"detail": str(exc)}, status_code=404)

@app.exception_handler(exceptions.AlreadyExistsError)
async def conflict_handler(request, exc: exceptions.AlreadyExistsError):
    return JSONResponse({"detail": str(exc)}, status_code=400)

@app.exception_handler(exceptions.BusinessError)
async def business_handler(request, exc: exceptions.BusinessError):
    return JSONResponse({"detail": str(exc)}, status_code=400)



@app.post("/students/", response_model=schemas.StudentNew, status_code=201)
async def create_student(student_in: schemas.StudentCreate, uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    student = await svc.create_student(student_in)
    logger.info("Created student id=%s name=%s", student.id, student.name)
    return student


@app.get("/students/", response_model=list[schemas.Student])
async def list_students(uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    return await svc.list_students()


@app.delete("/students/{student_id}", status_code=204)
async def delete_student(student_id: int, uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    await svc.delete_student(student_id)
    logger.info("Deleted student id=%s", student_id)
    return Response(status_code=204)


@app.post("/courses/", response_model=schemas.Course, status_code=201)
async def create_course(course_in: schemas.CourseCreate, uow: UnitOfWork = Depends(get_uow)):
    svc = services.CourseService(uow)
    course = await svc.create_course(course_in)
    logger.info("Created course id=%s title=%s", course.id, course.title)
    return course


@app.get("/courses/", response_model=list[schemas.Course])
async def list_courses(uow: UnitOfWork = Depends(get_uow)):
    svc = services.CourseService(uow)
    return await svc.list_courses()


@app.delete("/courses/{course_id}", status_code=204)
async def delete_course(course_id: int, uow: UnitOfWork = Depends(get_uow)):
    svc = services.CourseService(uow)
    await svc.delete_course(course_id)
    logger.info("Deleted course id=%s", course_id)
    return Response(status_code=204)


@app.post("/enroll/{student_id}/{course_id}", response_model=schemas.Student)
async def enroll(student_id: int, course_id: int, uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    student = await svc.enroll(student_id, course_id)
    logger.info("Enrolled student=%s to course=%s", student_id, course_id)
    return student


@app.delete("/students/{student_id}/courses/{course_id}", response_model=schemas.Student)
async def unenroll(student_id: int, course_id: int, uow: UnitOfWork = Depends(get_uow)):
    svc = services.StudentService(uow)
    student = await svc.unenroll(student_id, course_id)
    logger.info("Unenrolled student=%s from course=%s", student_id, course_id)
    return student
