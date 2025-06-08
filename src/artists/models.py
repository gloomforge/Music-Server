from typing import Optional

import sqlalchemy.dialects.mysql as msql
from sqlmodel import Column, Field, SQLModel


class Artist(SQLModel, table=True):
    __tablename__ = "artists"

    artist_id: Optional[int] = Field(
        sa_column=Column(
            type_=msql.INTEGER,
            primary_key=True,
            autoincrement=True,
        ),
    )

    name: str = Field(
        sa_column=Column(
            type_=msql.VARCHAR(255),
            nullable=False,
            index=True,
            unique=True,
        ),
        description="Name of the artist",
        max_length=255,
    )

    def __repr__(self) -> str:
        return f"<Artist {self.artist_id}: {self.artist_name}>"
