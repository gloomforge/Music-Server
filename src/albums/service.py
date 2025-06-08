from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select

from src.albums.models import Album
from src.albums.schemas import AlbumCreate, AlbumRead
from src.artists.service import ArtistService


class AlbumService:
    def __init__(
        self,
        session: AsyncSession,
        artist_service: ArtistService,
    ) -> None:
        self.session = session
        self.artist_service = artist_service

    async def get_all(self) -> List[AlbumRead]:
        statement = select(Album).order_by(desc(Album.title))
        result = await self.session.execute(statement)
        albums = result.scalars().all()

        return [AlbumRead.model_validate(album) for album in albums]

    async def get_by_id(self, album_id: int) -> AlbumRead:
        statement = select(Album).where(Album.album_id == album_id)
        result = await self.session.execute(statement)
        album = result.scalar_one_or_none()

        if not album:
            raise HTTPException(
                status_code=404,
                detail="Album not found",
            )

        return AlbumRead.model_validate(album)

    async def create(self, data: AlbumCreate) -> AlbumRead:
        await self.artist_service.get_by_id(data.artist_id)
        statement = select(Album).where(
            Album.artist_id == data.artist_id, Album.title == data.title
        )

        if (await self.session.execute(statement)).scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Album title already exists for this artist",
            )

        album = Album.from_orm(data)
        self.session.add(album)

        await self.session.commit()
        await self.session.refresh(album)
        return AlbumRead.model_validate(album)

    async def update(self, album_id: int, data: AlbumCreate) -> AlbumRead:
        album = self.get_by_id(album_id)
        await self.artist_service.get_by_id(data.artist_id)

        statement = select(Album).wher(
            Album.artist_id == data.artist_id,
            Album.title == data.title,
            Album.album_id != album_id,
        )
        if (await self.session.execute(statement)).scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Album title already exists for this artist",
            )

        for field, value in data.dict(exclude_unset=True).items():
            setattr(album, field, value)
        self.session.add(album)

        await self.session.commit()
        await self.session.refresh()
        return AlbumRead.model_validate(album)

    async def delete(self, album_id: int) -> None:
        album = await self.get_by_id(album_id)

        await self.session.delete(album)
        await self.session.commit()
