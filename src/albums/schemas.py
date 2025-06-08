from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class AlbumBase(BaseModel):
    title: str = Field(..., max_length=255)
    release_data: Optional[date] = None


class AlbumCreate(AlbumBase):
    artist_id: int = Field(..., description="ID of the artist")


class AlbumRead(AlbumBase):
    album_id: int
    artist_id: int
    created_at: datetime

    class Config:
        orm_mode = True
