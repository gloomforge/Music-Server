import sqlalchemy.dialects.mysql as msql
from sqlalchemy import Column
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(
        sa_column=Column(
            msql.INTEGER,
            primary_key=True,
            autoincrement=True,
        )
    )

    username: str = Field(
        sa_column=Column(
            msql.VARCHAR(255),
            nullable=False,
            unique=True,
        )
    )

    password: str = Field(
        sa_column=Column(
            msql.VARCHAR(255),
            nullable=False,
        )
    )
