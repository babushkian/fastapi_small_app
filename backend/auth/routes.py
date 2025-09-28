from fastapi import Query, Depends, APIRouter, status
from dependencies import get_uow
from uow import UnitOfWork
from auth.schemas import UserCreate, UserRead
from auth.services import UserService
router = APIRouter()

@router.get("/current_user")
async def get_current_user(uow: UnitOfWork = Depends(get_uow)):
    return {"user": "Dima"}


@router.post("/users/", response_model= UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate , uow: UnitOfWork = Depends(get_uow)):
    svc = UserService(uow)
    result_user = await svc.create_user(user)
    return result_user


@router.get("/users/", response_model= list[UserRead], status_code=status.HTTP_200_OK)
async def create_user(uow: UnitOfWork = Depends(get_uow)):
    svc = UserService(uow)
    users = await svc.list()
    return users

