from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MediaFileBase(BaseModel):
    id: int
    track_id: int
    file_path: str
    file_size: Optional[int]
    mime_type: Optional[str]
    checksum: Optional[str]
    created_at: datetime


class MediaFileRead(MediaFileBase):
    pass
