from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.albums.service import AlbumService
from src.genres.models import Genre
from src.tracks.models import Track
from src.tracks.schemas import TrackCreate, TrackRead


class TrackService:
    def __init__(
        self,
        session: AsyncSession,
        album_service: AlbumService,
    ) -> None:
        self.session = session
        self.album_service = album_service

    async def get_all(self) -> List[TrackRead]:
        statement = select(Track)
        result = await self.session.execute(statement)
        tracks = result.scalars().all()

        reads: List[TrackRead] = []
        for track in tracks:
            read = TrackRead.from_orm(track)
            read.genre_ids = [g.genre_id for g in track.genres]
            reads.append(read)

        return reads

    async def get_by_id(self, track_id: int) -> TrackRead:
        statement = select(Track).where(Track.track_id == track_id)
        result = await self.session.execute(statement)

        track: Optional[Track] = await result.scalar_one_or_none()
        if not track:
            raise HTTPException(
                status_code=404,
                detail="Track not found",
            )

        read = TrackRead.from_orm(track)
        read.genre_ids = [g.genre_id for g in track.genres]

        return read

    async def create(self, data: TrackCreate) -> TrackRead:
        await self.album_service.get_by_id(data.album_id)
        statement = select(Track).where(
            Track.album_id == data.album_id,
            Track.position == data.position,
        )

        if (await self.session.execute(statement)).scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Track position already taken in this album",
            )

        track = Track.from_orm(data)
        if data.genre_ids:
            genres = (
                (
                    await self.session.execute(
                        select(Genre).where(Genre.genre_id.in_(data.genre_ids))
                    )
                )
                .scalars()
                .all()
            )
            track.genres = genres

        self.session.add(track)

        await self.session.commit()
        await self.session.refresh(track)
        return await self.get_by_id(track.track_id)

    async def update(self, track_id: int, data: TrackCreate) -> TrackRead:
        track: TrackRead = await self.get_by_id(track_id)
        await self.album_service.get_by_id(data.album_id)

        statement = select(Track).where(
            Track.album_id == data.album_id,
            Track.position == data.position,
            Track.track_id != track_id,
        )
        if (await self.session.execute(statement)).scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Track position already taken in  this album",
            )

        for field, val in data.dict(exclude_unset=True).items():
            if field != "genre_ids":
                setattr(track, field, val)

        if data.genre_ids is not None:
            genres = (
                (
                    await self.session.execute(
                        select(Genre).where(Genre.genre_id.in_(data.genre_ids))
                    )
                )
                .scalars()
                .all()
            )
            track.genre_ids = genres

        self.session.add(track)
        await self.session.commit()
        await self.session.refresh(track)
        return await self.get_by_id(track.track_id)

    async def delete(self, track_id: int) -> None:
        track: TrackRead = await self.get_by_id(track_id)
        await self.session.delete(track)
        await self.session.commit()
