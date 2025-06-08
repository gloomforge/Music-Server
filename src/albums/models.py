from datetime import date, datetime
from typing import Optional

import sqlalchemy.dialects.mysql as msql
from sqlalchemy import ForeignKey, func
from sqlmodel import Column, Field, SQLModel


class Album(SQLModel, table=True):
    __tablename__ = "albums"

    album_id: int = Field(
        sa_column=Column(
            type_=msql.INTEGER,
            primary_key=True,
            autoincrement=True,
        ),
    )

    artist_id: int = Field(
        sa_column=Column(
            ForeignKey("artists.artist_id"),
            type_=msql.INTEGER,
            nullable=False,
            index=True,
        ),
        description="ID of the artist associated with the album",
    )

    title: str = Field(
        sa_column=Column(
            type_=msql.VARCHAR(255),
            nullable=False,
            index=True,
        ),
        max_length=255,
        description="Title of the album",
    )

    release_data: Optional[date] = Field(
        sa_column=Column(
            type_=msql.DATE,
            nullable=False,
            index=True,
        ),
        description="Release date of the album",
    )

    created_at: datetime = Field(
        sa_column=Column(
            type_=msql.DATETIME,
            server_default=func.now(),
            nullable=False,
            index=True,
        ),
        description="Creation timestamp of the album",
    )

    def __repr__(self) -> str:
        return f"<Album {self.album_id}: {self.title} ({self.release_date})>"
