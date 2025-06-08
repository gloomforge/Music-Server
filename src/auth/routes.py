from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import AuthCreate, AuthRead
from src.auth.service import AuthService
from src.db.engine import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


async def get_auth_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(session)


@router.post("/register", response_model=AuthRead, status_code=201)
async def register(
    data: AuthCreate,
    service: AuthService = Depends(get_auth_service),
):
    return await service.register(data)


@router.post("/login", response_model=AuthRead)
async def login(
    data: AuthCreate,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(data)
