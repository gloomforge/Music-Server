from typing import List, Optional

import sqlalchemy.dialects.mysql as msql
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel

from src.db.models.track_genre import TrackGenre


class Genre(SQLModel, table=True):
    __tablename__ = "genres"

    genre_id: Optional[int] = Field(
        sa_column=Column(
            msql.INTEGER,
            primary_key=True,
            autoincrement=True,
        )
    )

    genre_name: str = Field(
        sa_column=Column(
            msql.VARCHAR(100),
            nullable=False,
            unique=True,
            index=True,
        ),
        max_length=100,
        description="Name of the genre",
    )

    tracks: List["Track"] = Relationship(
        back_populates="genres",
        link_model=TrackGenre,
    )
