from pydantic import BaseModel
from typing import Optional


class UsuarioCreate(BaseModel):
    username: str
    password: str


class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: int
    username: str
    message_status: str

    class Config:
        from_attributes = True