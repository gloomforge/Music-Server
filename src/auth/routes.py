from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import AuthCreate, AuthRead
from src.auth.service import AuthService
from src.auth.session.manager import SessionManager, get_session_manager
from src.auth.session.schemas import SessionRead
from src.db.engine import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


async def get_auth_service(
    session: AsyncSession = Depends(get_session),
    manager: SessionManager = Depends(get_session_manager),
) -> AuthService:
    return AuthService(session, manager)


@router.post("/login", response_model=tuple[AuthRead, SessionRead])
async def login(
    data: AuthCreate,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(data)


@router.post("/register", response_model=tuple[AuthRead, SessionRead])
async def register(
    data: AuthCreate,
    service: AuthService = Depends(get_auth_service),
):
    return await service.register(data)


@router.post("/logout")
async def logout(
    session_id: str = Header(alias="X-Session-Id"),
    service: AuthService = Depends(get_auth_service),
):
    await service.logout(session_id)


@router.post("/refresh", response_model=SessionRead)
async def refresh_session(
    session_id: str = Header(alias="X-Session-Id"),
    service: AuthService = Depends(get_auth_service),
):
    return await service.refresh_session(session_id)
