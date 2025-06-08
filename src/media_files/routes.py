from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import get_session
from src.media_files.schemas import MediaFileRead
from src.media_files.service import MediaService

router = APIRouter(prefix="/media/fies", tags=["media_files"])


async def get_media_service(
    session: AsyncSession = Depends(get_session),
) -> MediaService:
    return MediaService(session)


@router.post("/upload/{track_id}", response_model=MediaFileRead)
async def upload_file(
    track_id: int,
    file: UploadFile,
    service: MediaService = Depends(get_media_service),
):
    return await service.save_file(track_id, file)


@router.get("/file/{media_id}")
async def get_file(
    media_id: int,
    service: MediaService = Depends(get_media_service),
):
    media = await service.get_by_id(media_id)
    if not media:
        raise HTTPException(
            status_code=404,
            detail="Media file not found",
        )

    return FileResponse(
        path=media.file_path,
        media_type=media.mime_type,
        filename=media.file_path.split("/")[-1],
    )


@router.delete("/{media_id}", status_code=204)
async def delete_media(
    media_id: int,
    service: MediaService = Depends(get_media_service),
):
    await service.delete(media_id)
