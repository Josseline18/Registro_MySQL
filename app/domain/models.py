#define la tabla usuarios en MySQL (columnas: id, username, password, created_at)
from sqlalchemy import Column, Integer, String
from app.infrastructure.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    placa = Column(String(20), unique=True, nullable=False)