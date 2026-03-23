from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.infrastructure.rabbit_producer import enviar_mensaje  # Agregar esto
from app.domain.models import Cliente
from app.domain.schemas import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/", response_model=list[ClienteResponse])
def get_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(data: ClienteCreate, db: Session = Depends(get_db)):
    existente = db.query(Cliente).filter(
        or_(Cliente.username == data.username, Cliente.placa == data.placa)
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="username o placa ya existen")

    nuevo = Cliente(username=data.username, placa=data.placa)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # antes: enviar_mensaje(f"Cliente creado: {nuevo.username}, Placa: {nuevo.placa}")
    enviar_mensaje(username=nuevo.username, placa=nuevo.placa)

    return nuevo


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente_by_id(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente