
from fastapi import FastAPI

from starlette.templating import Jinja2Templates

from contextlib import asynccontextmanager
import logging

from app.db.database import engine
from app.db.base import Base
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