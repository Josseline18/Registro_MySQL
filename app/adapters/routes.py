from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.infrastructure.database import get_db
from app.domain.models import Usuario
from app.domain.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.infrastructure.rabbit_producer import send_message

router = APIRouter()


# POST - Crear usuario
@router.post("/registrar", response_model=UsuarioResponse)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(
        username=usuario.username,
        especie=usuario.especie,
        titular=usuario.titular
    )

    try:
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"El usuario '{usuario.username}' ya existe"
        )

    mensaje = {
        "event": "user_registered",
        "user_id": nuevo_usuario.id,
        "username": nuevo_usuario.username,
        "especie": nuevo_usuario.especie,
        "titular": nuevo_usuario.titular,
        "message": f"Usuario '{nuevo_usuario.username}' registrado exitosamente"
    }

    try:
        send_message(mensaje)
        message_status = "Mensaje enviado a RabbitMQ exitosamente"
    except Exception as e:
        message_status = f"Usuario guardado, pero error en RabbitMQ: {str(e)}"

    return UsuarioResponse(
        id=nuevo_usuario.id,
        username=nuevo_usuario.username,
        especie=nuevo_usuario.especie,
        titular=nuevo_usuario.titular,
        message_status=message_status
    )


# GET - Listar todos los usuarios
@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "especie": u.especie,
            "titular": u.titular,
            "created_at": str(u.created_at)
        }
        for u in usuarios
    ]


# GET - Obtener un usuario por ID
@router.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": usuario.id,
        "username": usuario.username,
        "especie": usuario.especie,
        "titular": usuario.titular,
        "created_at": str(usuario.created_at)
    }


# PUT - Actualizar usuario
@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos.username is not None:
        usuario.username = datos.username
    if datos.especie is not None:
        usuario.especie = datos.especie
    if datos.titular is not None:
        usuario.titular = datos.titular

    try:
        db.commit()
        db.refresh(usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"El username '{datos.username}' ya existe"
        )

    mensaje = {
        "event": "user_updated",
        "user_id": usuario.id,
        "username": usuario.username,
        "especie": usuario.especie,
        "titular": usuario.titular,
        "message": f"Usuario '{usuario.username}' actualizado exitosamente"
    }

    try:
        send_message(mensaje)
        message_status = "Mensaje enviado a RabbitMQ exitosamente"
    except Exception as e:
        message_status = f"Usuario actualizado, pero error en RabbitMQ: {str(e)}"

    return UsuarioResponse(
        id=usuario.id,
        username=usuario.username,
        especie=usuario.especie,
        titular=usuario.titular,
        message_status=message_status
    )


# DELETE - Eliminar usuario
@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    username = usuario.username

    db.delete(usuario)
    db.commit()

    mensaje = {
        "event": "user_deleted",
        "user_id": usuario_id,
        "username": username,
        "message": f"Usuario '{username}' eliminado exitosamente"
    }

    try:
        send_message(mensaje)
        message_status = "Mensaje enviado a RabbitMQ exitosamente"
    except Exception as e:
        message_status = f"Usuario eliminado, pero error en RabbitMQ: {str(e)}"

    return {
        "detail": f"Usuario '{username}' eliminado",
        "message_status": message_status
    }