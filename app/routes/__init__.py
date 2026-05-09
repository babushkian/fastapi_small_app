from .courses import router as course_router
from .students import router as student_router

__all__ = ["course_router", "student_router"]