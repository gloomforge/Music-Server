from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import AuthRead as UserRead
from src.db.engine import get_session
from src.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    return UserService(session)


@router.get("/", response_model=List[UserRead])
async def get_users(
    service: UserService = Depends(get_user_service),
):
    return await service.get_users()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return await service.get_user(user_id)

@router.delete("/{user_id}")
async def delete_user(
        user_id: int,
        service: UserService = Depends(get_user_service)
):
    return await service.delete_user(user_id)