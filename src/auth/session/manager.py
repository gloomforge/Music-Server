from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.session.models import Session
from src.auth.session.schemas import SessionCreate, SessionRead
from src.db.engine import get_session


async def get_session_manager(
    session: AsyncSession = Depends(get_session),
) -> "SessionManager":
    return SessionManager(session)


class SessionManager:
    def __init__(
        self,
        session: AsyncSession,
        default_expiry: timedelta = timedelta(hours=1),
    ) -> None:
        self.db = session
        self.default_expiry = default_expiry

    async def create_session(self, data: SessionCreate) -> SessionRead:
        session = Session(
            user_id=data.user_id,
            expires_at=data.expires_at,
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return SessionRead(
            session_id=session.session_id,
            user_id=session.user_id,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )

    async def get_session(self, session_id: str) -> Optional[SessionRead]:
        statement = select(Session).where(Session.session_id == session_id)
        result = await self.db.execute(statement)
        session = result.scalars().first()

        if not session:
            return None
        if session.expires_at < datetime.utcnow():
            await self.db.delete(session)
            await self.db.commit()
            return None

        return SessionRead(
            session_id=session.session_id,
            user_id=session.user_id,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )

    async def delete_session(self, session_id: str) -> None:
        statement = select(Session).where(Session.session_id == session_id)
        result = await self.db.execute(statement)
        session = result.scalars().first()

        if session:
            await self.db.delete(session)
            await self.db.commit()

    async def refresh_session(
        self, session_id: str, new_expiry: datetime
    ) -> Optional[SessionRead]:
        statement = select(Session).where(Session.session_id == session_id)
        result = await self.db.execute(statement)
        session = result.scalars().first()

        if not session or session.expires_at < datetime.utcnow():
            return None

        session.expires_at = new_expiry
        await self.db.commit()
        await self.db.refresh(session)

        return SessionRead(
            session_id=session.session_id,
            user_id=session.user_id,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )
