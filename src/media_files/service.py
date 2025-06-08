import hashlib
import os
from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.media_files.models import MediaFile
from src.media_files.schemas import MediaFileRead

MEDIA_DIR = "media"


class MediaService:
    def __init__(self, session: AsyncSession):
        self.session = session
        os.makedirs(MEDIA_DIR, exist_ok=True)

    async def save_file(
        self,
        track_id: int,
        file: UploadFile,
    ) -> MediaFileRead:
        file_bytes = await file.read()
        checksum = hashlib.sha256(file_bytes).hexdigest()
        file_path = os.path.join(MEDIA_DIR, f"{checksum}_{file.filename}")

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        media = MediaFile(
            track_id=track_id,
            file_path=file_path,
            file_size=len(file_bytes),
            mime_type=file.content_type,
            checksum=checksum,
        )
        self.session.add(media)
        await self.session.commit()
        await self.session.refresh(media)
        return MediaFileRead.model_validate(media)

    async def get_by_id(self, media_id: int) -> Optional[MediaFileRead]:
        result = await self.session.execute(
            select(MediaFile).where(MediaFile.id == media_id)
        )

        return MediaFileRead.model_validate(result.scalar_one_or_none())

    async def delete(self, media_id: int) -> None:
        media = await self.get_by_id(media_id)
        if not media:
            raise HTTPException(
                status_code=404,
                detail="Media not found",
            )

        try:
            os.remove(media.file_path)
        except FileNotFoundError:
            pass

        await self.session.delete(media)
        await self.session.commit()
