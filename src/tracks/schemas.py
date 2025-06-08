from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TrackBase(BaseModel):
    title: str
    position: Optional[int]


class TrackCreate(TrackBase):
    album_id: int
    genre_ids: List[int] = []


class TrackRead(TrackBase):
    track_id: int
    album_id: int
    created_at: datetime
    genre_ids: List[int] = []

    class Config:
        orm_mode = True
