from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.genres.models import Genre
from src.genres.schemas import GenreCreate, GenreRead


class GenreService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> List[GenreRead]:
        result = await self.session.execute(select(Genre))
        genres = result.scalars().all()
        return [GenreRead.from_orm(g) for g in genres]

    async def get_by_id(self, genre_id: int) -> GenreRead:
        result = await self.session.execute(
            select(Genre).where(Genre.genre_id == genre_id)
        )
        genre = result.scalar_one_or_none()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        return GenreRead.from_orm(genre)

    async def create(self, data: GenreCreate) -> GenreRead:
        result = await self.session.execute(
            select(Genre).where(Genre.genre_name == data.genre_name)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"Genre '{data.genre_name}' already exists",
            )

        genre = Genre(genre_name=data.genre_name)
        self.session.add(genre)
        await self.session.commit()
        await self.session.refresh(genre)
        return GenreRead.from_orm(genre)

    async def update(self, genre_id: int, data: GenreCreate) -> GenreRead:
        result = await self.session.execute(
            select(Genre).where(Genre.genre_id == genre_id)
        )
        genre = result.scalar_one_or_none()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")

        result = await self.session.execute(
            select(Genre).where(
                Genre.genre_name == data.genre_name, Genre.genre_id != genre_id
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400, detail="Genre name already used by another"
            )

        genre.genre_name = data.genre_name
        self.session.add(genre)
        await self.session.commit()
        await self.session.refresh(genre)
        return GenreRead.from_orm(genre)

    async def delete(self, genre_id: int) -> None:
        result = await self.session.execute(
            select(Genre).where(Genre.genre_id == genre_id)
        )

        genre = result.scalar_one_or_none()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        await self.session.delete(genre)
        await self.session.commit()
