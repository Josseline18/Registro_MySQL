from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ClienteBase(BaseModel):
    username: str
    placa: str


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TallerCreate(BaseModel):
    marca: str = Field(..., min_length=1, max_length=100)
    modelo: str = Field(..., min_length=1, max_length=100)
    placa: str = Field(..., min_length=1, max_length=20)
    cliente_id: int


class TallerResponse(TallerCreate):
    id: int

    class Config:
        from_attributes = True


