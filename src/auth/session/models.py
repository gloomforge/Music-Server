from datetime import datetime
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlmodel import Field, SQLModel


class Session(SQLModel, table=True):
    __tablename__ = "sessions"  # type: ignore

    session_id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
    )
    user_id: int = Field(ForeignKey("users.user_id"))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
