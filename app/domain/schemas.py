from typing import Optional
from pydantic import BaseModel, ConfigDict


class ClienteBase(BaseModel):
    username: str
    placa: str


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


