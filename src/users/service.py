from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.models import User
from src.auth.schemas import AuthRead as UserRead


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self) -> List[UserRead]:
        result = await self.session.execute(select(User))
        users = result.scalars().all()
        return [UserRead.model_validate(u) for u in users]

    async def get_user(self, user_id: int) -> UserRead:
        statement = select(User).where(user_id == User.user_id)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        return UserRead.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        statement = select(User).where(User.user_id == user_id)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        await self.session.delete(user)
        await self.session.commit()
