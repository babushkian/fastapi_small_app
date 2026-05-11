from .courses import router as course_router
from .students import router as student_router
from .pages import router as pages_router
__all__ = ["course_router", "student_router", "pages_router"]