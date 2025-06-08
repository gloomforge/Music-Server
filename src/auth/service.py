from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.models import User
from src.auth.schemas import AuthCreate, AuthRead

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def login(self, data: AuthCreate) -> AuthRead:
        statement = select(User).where(
            User.username == data.username,
        )
        result = await self.session.execute(statement)
        user = result.scalars().first()
        if not user or not pwd_ctx.verify(data.password, user.password):
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        return AuthRead.model_validate(user)

    async def register(self, data: AuthCreate) -> AuthRead:
        statement = select(User).where(
            User.username == data.username,
        )
        result = await self.session.execute(statement)

        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="User already exists",
            )

        user = User(
            username=data.usernamae,
            password=pwd_ctx.hash(data.password),
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return AuthRead.model_validate(user)
