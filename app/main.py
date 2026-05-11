import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from  starlette.responses import HTMLResponse
from pathlib import Path

from app.db.database import engine
from app.db.base import Base

from app import exceptions
from app.auth.routes import router as auth_router
from app.routes import course_router, student_router


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
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # любой домен
    allow_credentials=False,  # без cookies
    allow_methods=["*"],      # все методы (GET, POST и т.д.)
    allow_headers=["*"],      # все заголовки
)
from app.routes import  pages_router
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(student_router, prefix="/students", tags=["students"])
app.include_router(course_router, prefix="/courses", tags=["courses"])

app.include_router(pages_router)

# @app.get("/abba", response_class=HTMLResponse)
# async def index(request: Request):
#     return templates.TemplateResponse(request, "base.html", context= {"title":"Home"})
#

# custom exception handlers
@app.exception_handler(exceptions.NotFoundError)
async def not_found_handler(request, exc: exceptions.NotFoundError):
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_404_NOT_FOUND)

@app.exception_handler(exceptions.AlreadyExistsError)
async def conflict_handler(request, exc: exceptions.AlreadyExistsError):
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)

@app.exception_handler(exceptions.BusinessError)
async def business_handler(request, exc: exceptions.BusinessError):
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)


