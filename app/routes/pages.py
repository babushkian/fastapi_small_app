from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from app.fastapi_instance import templates

router = APIRouter()

@router.get("/abba", response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse(request, "index.html", context= {"title":"Home"})
