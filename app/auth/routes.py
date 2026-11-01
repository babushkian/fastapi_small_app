from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.auth.schemas import UserCreate, UserRead
from app.auth.services import UserService
from app.dependencies import get_uow
from app.uow import SQLUnitOfWork

router = APIRouter()

@router.get("/current_user")
async def get_current_user(uow: Annotated[SQLUnitOfWork, Depends(get_uow)]):
    return {"user": "Dima"}


@router.post("/users/", response_model= UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, uow: Annotated[SQLUnitOfWork, Depends(get_uow)]):
    svc = UserService(uow)
    result_user = await svc.create_user(user)
    return result_user


@router.get("/users/", response_model= list[UserRead], status_code=status.HTTP_200_OK)
async def users_list(uow: Annotated[SQLUnitOfWork, Depends(get_uow)]):
    svc = UserService(uow)
    users = await svc.list()
    return users

