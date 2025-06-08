from pydantic import BaseModel


class AuthBase(BaseModel):
    username: str


class AuthCreate(AuthBase):
    password: str


class AuthRead(AuthBase):
    user_id: int

    class Config:
        orm_model = True
