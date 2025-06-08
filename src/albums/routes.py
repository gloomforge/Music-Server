from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.albums.schemas import AlbumCreate, AlbumRead
from src.albums.service import AlbumService
from src.artists.service import ArtistService
from src.db.engine import get_session

router = APIRouter(prefix="/album", tags=["album"])


async def get_album_service(
    session: AsyncSession = Depends(get_session),
    artist_service: ArtistService = Depends(
        lambda session=Depends(get_session): ArtistService(session)
    ),
) -> AlbumService:
    return AlbumService(session, artist_service)


@router.get("/", response_model=List[AlbumRead])
async def read_albums(
    service: AlbumService = Depends(get_album_service),
):
    return await service.get_all()


@router.get("/{album_id}", response_model=AlbumRead)
async def read_album(
    album_id: int,
    service: AlbumService = Depends(get_album_service),
):
    return await service.get_by_id(album_id)


@router.post("/", response_model=AlbumRead, status_code=201)
async def create(
    data: AlbumCreate,
    service: AlbumService = Depends(get_album_service),
):
    return await service.create(data)


@router.put("/{album_id}", response_model=AlbumRead)
async def update(
    album_id: int,
    data: AlbumCreate,
    service: AlbumService = Depends(get_album_service),
):
    return await service.update(album_id, data)


@router.delete("/{album_id}", response_model=None, status_code=204)
async def delete(
    album_id: int,
    service: AlbumService = Depends(get_album_service),
):
    await service.delete(album_id)
