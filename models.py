#define la tabla usuarios en MySQL (columnas: id, username, password, created_at)
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())