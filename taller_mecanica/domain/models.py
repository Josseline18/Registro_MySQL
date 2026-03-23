#define la tabla usuarios en MySQL (columnas: id, username, password, created_at)
from sqlalchemy import Column, Integer, String
from taller_mecanica.infrastructure.database import Base


class TallerIngreso(Base):
    __tablename__ = "taller_ingresos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    placa = Column(String(20), unique=True, nullable=False)
    cliente_id = Column(Integer, nullable=False, index=True)