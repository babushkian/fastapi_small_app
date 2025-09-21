from fastapi import Query, Depends, APIRouter
from dependencies import get_uow
from uow import UnitOfWork
router = APIRouter()

@router.get("/current_user")
async def get_current_user(uow: UnitOfWork = Depends(get_uow)):
    return {"user": "Dima"}


