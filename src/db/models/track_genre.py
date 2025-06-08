from typing import Optional

import sqlalchemy.dialects.mysql as msql
from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, SQLModel


class TrackGenre(SQLModel, table=True):
    __tablename__ = "track_genres"

    track_id: Optional[int] = Field(
        sa_column=Column(
            msql.INTEGER,
            ForeignKey(
                "tracks.track_id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        )
    )

    genre_id: Optional[int] = Field(
        sa_column=Column(
            msql.INTEGER,
            ForeignKey(
                "genres.genre_id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        )
    )
