from datetime import datetime
from typing import Optional

import sqlalchemy.dialects.mysql as msql
from sqlalchemy import ForeignKey
from sqlmodel import Column, Field, SQLModel


class MediaFile(SQLModel, table=True):
    __tablename__ = "media_files"

    media_id: int = Field(
        sa_column=Column(
            type_=msql.INTEGER,
            primary_key=True,
            autoincrement=True,
        )
    )

    track_id: int = Field(
        sa_column=Column(
            ForeignKey("tracks.track_id"), type_=msql.INTEGER, nullable=False
        )
    )

    file_path: str = Field(nullable=False)
    file_size: Optional[int] = None
    mime_type: Optional[str] = Field(default=None, max_length=50)
    checksum: Optional[str] = Field(default=None, max_length=64)
    created_at: datetime = Field(default_factory=datetime.utcnow)
