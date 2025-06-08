from datetime import datetime
from typing import List, Optional

import sqlalchemy.dialects.mysql as msql
from sqlalchemy import Column, ForeignKey, func
from sqlmodel import Field, Relationship, SQLModel

from src.db.models.track_genre import TrackGenre


class Track(SQLModel, table=True):
    __tablename__ = "tracks"

    track_id: Optional[int] = Field(
        sa_column=Column(
            msql.INTEGER,
            primary_key=True,
            autoincrement=True,
        )
    )

    album_id: int = Field(
        sa_column=Column(
            msql.INTEGER,
            ForeignKey(
                "albums.album_id",
                ondelete="CASCADE",
            ),
            nullable=False,
        )
    )

    title: str = Field(
        sa_column=Column(
            msql.VARCHAR(255),
            nullable=False,
        ),
        description="Track title",
    )

    position: Optional[int] = Field(
        default=None,
        description="Track position in album",
    )

    created_at: datetime = Field(
        sa_column=Column(
            msql.TIMESTAMP,
            server_default=func.now(),
            nullable=False,
            index=True,
        ),
        description="Creation timestamp of the track",
    )

    genres: List["Genre"] = Relationship(
        back_populates="tracks",
        link_model=TrackGenre,
    )
