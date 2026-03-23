from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from taller_mecanica.infrastructure.database import get_db
from taller_mecanica.infrastructure.client_validator import cliente_existe
from taller_mecanica.domain.models import TallerIngreso
from taller_mecanica.domain.schemas import TallerCreate, TallerResponse

router = APIRouter(prefix="/taller", tags=["taller"])


@router.get("/", response_model=list[TallerResponse])
def get_ingresos(db: Session = Depends(get_db)):
    return db.query(TallerIngreso).all()


@router.post("/", response_model=TallerResponse, status_code=status.HTTP_201_CREATED)
def create_ingreso(data: TallerCreate, db: Session = Depends(get_db)):
    if not cliente_existe(data.cliente_id):
        raise HTTPException(status_code=400, detail="cliente_id no existe en microservicio clientes")

    existe_placa = db.query(TallerIngreso).filter(TallerIngreso.placa == data.placa).first()
    if existe_placa:
        raise HTTPException(status_code=400, detail="placa ya registrada en taller")

    nuevo = TallerIngreso(
        marca=data.marca,
        modelo=data.modelo,
        placa=data.placa,
        cliente_id=data.cliente_id
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo