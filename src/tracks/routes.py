from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.albums.service import AlbumService
from src.db.engine import get_session
from src.tracks.schemas import TrackCreate, TrackRead
from src.tracks.service import TrackService

router = APIRouter(prefix="/tack", tags=["track"])


async def get_track_service(
    session: AsyncSession = Depends(get_session),
    album_service: AlbumService = Depends(
        lambda session=Depends(get_session): AlbumService(session)
    ),
) -> TrackService:
    return TrackService(session, album_service)


@router.get("/", response_model=List[TrackRead])
async def read_tracks(
    service: TrackService = Depends(get_track_service),
):
    return await service.get_all()


@router.get("/{track_id}", response_model=TrackRead)
async def read_track(
    track_id: int,
    service: TrackService = Depends(get_track_service),
):
    return await service.get_by_id(track_id)


@router.post("/", response_model=TrackRead, status_code=201)
async def create(
    data: TrackCreate,
    service: TrackService = Depends(get_track_service),
):
    return await service.create(data)


@router.put("/{trick_id}", response_model=TrackRead)
async def update(
    trick_id: int,
    data: TrackCreate,
    service: TrackService = Depends(get_track_service),
):
    await service.update(trick_id, data)


@router.delete("/{trick_id}", status_code=204)
async def delete(
    trick_id: int,
    service: TrackService = Depends(get_track_service),
):
    await service.delete(trick_id)
