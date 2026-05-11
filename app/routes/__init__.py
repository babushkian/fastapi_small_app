from fastapi import APIRouter




from .courses import router as course_router
from .students import router as student_router
from .pages import router as pages_router

api_router=APIRouter()
api_router.include_router(student_router, prefix="/students", tags=["students"])
api_router.include_router(course_router, prefix="/courses", tags=["courses"])


__all__ = ["api_router", "pages_router"]