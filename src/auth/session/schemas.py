from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SessionBase(BaseModel):
    user_id: Optional[int]
    expires_at: datetime


class SessionRequest(BaseModel):
    session_id: str


class SessionCreate(SessionBase):
    pass


class SessionRead(SessionBase):
    session_id: str
    created_at: datetime
