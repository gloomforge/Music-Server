from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select

from src.artists.models import Artist
from src.artists.schemas import ArtistCreate, ArtistRead


class ArtistService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> List[ArtistRead]:
        statement = select(Artist).order_by(desc(Artist.name))
        result = await self.session.execute(statement)
        artists = result.scalars().all()

        return [ArtistRead.model_validate(artist) for artist in artists]

    async def get_by_id(self, artist_id: int) -> ArtistRead:
        statement = select(Artist).where(Artist.artist_id == artist_id)
        result = await self.session.execute(statement)

        artist = result.scalar_one_or_none()
        if not artist:
            raise HTTPException(
                status_code=404,
                detail="Artist not found",
            )

        return ArtistRead.model_validate(artist)

    async def create(self, data: ArtistCreate) -> ArtistRead:
        statement = select(Artist).where(Artist.name == data.artist_name)
        if (await self.session.execute(statement)).scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Artist already exists",
            )

        artist = Artist.from_orm(data)
        self.session.add(artist)
        await self.session.commit()
        await self.session.refresh(artist)
        return ArtistRead.model_validate(artist)

    async def update(self, artist_id: int, data: ArtistCreate) -> ArtistRead:
        statement = select(Artist).where(
            Artist.name == data.name,
            Artist.artist_id != artist_id,
        )
        if (await self.session.execute(statement)).scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Artist name already used",
            )

        artist = await self.get_by_id(artist_id)
        for field, value in data.dict(exclude_unset=True).items():
            setattr(artist, field, value)
        self.session.add(artist)

        await self.session.commit()
        await self.session.refresh(artist)
        return ArtistRead.model_validate(artist)

    async def delete(self, artist_id: int) -> None:
        artist = await self.get_by_id(artist_id)
        await self.session.delete(artist)
        await self.session.commit()
