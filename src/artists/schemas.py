from pydantic import BaseModel, Field


class ArtistBase(BaseModel):
    name: str = Field(..., max_length=255, description="Artist name")


class ArtistCreate(ArtistBase):
    pass


class ArtistRead(ArtistBase):
    artist_id: int

    class Config:
        orm_mode = True
