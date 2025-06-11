from datetime import datetime, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.models import User
from src.auth.schemas import AuthCreate, AuthRead
from src.auth.session.manager import SessionManager
from src.auth.session.schemas import SessionCreate, SessionRead

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, session: AsyncSession, manager: SessionManager) -> None:
        self.session = session
        self.manager = manager

    async def login(self, data: AuthCreate) -> tuple[AuthRead, SessionRead]:
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

        session_data = SessionCreate(
            user_id=user.user_id,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
        session = await self.manager.create_session(session_data)

        return AuthRead.model_validate(user), session

    async def register(self, data: AuthCreate) -> tuple[AuthRead, SessionRead]:
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
            username=data.username,
            password=pwd_ctx.hash(data.password),
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        session_data = SessionCreate(
            user_id=user.user_id,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
        session = await self.manager.create_session(session_data)

        return AuthRead.model_validate(user), session

    async def logout(self, session_id: str) -> None:
        await self.manager.delete_session(session_id)

    async def refresh_session(self, session_id: str) -> SessionRead:
        session = await self.manager.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=401,
                detail="Invalid session",
            )

        new_expiry = datetime.utcnow() + timedelta(days=7)
        refreshed_session = await self.manager.refresh_session(
            session_id,
            new_expiry,
        )
        if not refreshed_session:
            raise HTTPException(
                status_code=401,
                detail="Failed to refresh session",
            )

        return refreshed_session
