from pydantic import BaseModel
from typing import Optional


class UsuarioCreate(BaseModel):
    username: str
    especie: str
    titular: str


class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    especie: Optional[str] = None
    titular: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: int
    username: str
    especie: str
    titular: str
    message_status: str

    class Config:
        from_attributes = True