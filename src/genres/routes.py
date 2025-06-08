from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.engine import get_session
from src.genres.schemas import GenreCreate, GenreRead
from src.genres.service import GenreService

router = APIRouter(prefix="/genre", tags=["genre"])


async def get_genre_service(
    session: AsyncSession = Depends(get_session),
) -> GenreService:
    return GenreService(session)


@router.get("/", response_model=List[GenreRead])
async def read_genres(
    service: GenreService = Depends(get_genre_service),
):
    return await service.get_all()


@router.get("/{genre_id}", response_model=GenreRead)
async def read_genre(
    genre_id: int,
    service: GenreService = Depends(get_genre_service),
):
    return await service.get_by_id(genre_id)


@router.post(path="/", response_model=GenreRead, status_code=201)
async def create_genre(
    data: GenreCreate,
    service: GenreService = Depends(get_genre_service),
):
    return await service.create(data)


@router.put("/{genre_id}", response_model=GenreRead)
async def update_genre(
    genre_id: int,
    data: GenreCreate,
    service: GenreService = Depends(get_genre_service),
):
    return await service.update(genre_id, data)


@router.delete("/{genre_id}", status_code=204)
async def delete_genre(
    genre_id: int,
    service: GenreService = Depends(get_genre_service),
):
    await service.delete(genre_id)
