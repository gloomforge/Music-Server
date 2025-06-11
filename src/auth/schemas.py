from pydantic import BaseModel


class AuthBase(BaseModel):
    username: str


class AuthCreate(AuthBase):
    password: str


class AuthRead(AuthBase):
    user_id: int

    model_config = {
        "from_attributes": True,
    }
