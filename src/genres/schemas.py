from pydantic import BaseModel, Field


class GenreBase(BaseModel):
    genre_name: str = Field(..., max_length=100)


class GenreCreate(GenreBase):
    pass


class GenreRead(GenreBase):
    genre_id: int

    model_config = {
        "from_attributes": True,
    }
