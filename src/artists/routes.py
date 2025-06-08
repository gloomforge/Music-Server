from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.artists.schemas import ArtistCreate, ArtistRead
from src.artists.service import ArtistService
from src.db.engine import get_session

router = APIRouter(prefix="/artist", tags=["artist"])


async def get_artist_service(
    session: AsyncSession = Depends(get_session),
) -> ArtistService:
    return ArtistService(session)


@router.get("/", response_model=List[ArtistRead])
async def read_artists(
    service: ArtistService = Depends(get_artist_service),
):
    return await service.get_all()


@router.get("/{artist_id}", response_model=ArtistRead)
async def read_artist(
    artist_id: int, service: ArtistService = Depends(get_artist_service)
):
    return await service.get_by_id(artist_id)


@router.post("/", response_model=ArtistRead, status_code=201)
async def create_artist(
    data: ArtistCreate, service: ArtistService = Depends(get_artist_service)
):
    return await service.create(data)


@router.put("/{artist_id}", response_model=ArtistRead)
async def update_artist(
    artist_id: int,
    data: ArtistCreate,
    service: ArtistService = Depends(get_artist_service),
):
    return await service.update(artist_id, data)


@router.delete("/{artist_id}", status_code=204)
async def delete_artist(
    artist_id: int,
    service: ArtistService = Depends(get_artist_service),
):
    await service.delete(artist_id)
