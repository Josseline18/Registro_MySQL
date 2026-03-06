#El archivo principal: levanta FastAPI, recibe el POST, guarda el usuario en MySQL y llama a rabbit_producer.py para enviar el mensaje a RabbitMQ.
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import engine, get_db, Base
from models import Usuario
from schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from rabbit_producer import send_message

# Crear las tablas en MySQL al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Registro de Usuarios",
    description="Registra usuarios en MySQL y envía mensajes a RabbitMQ",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "API de Registro de Usuarios - RabbitMQ + MySQL"}


#POST (Create) 
@app.post("/registrar", response_model=UsuarioResponse)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(
        username=usuario.username,
        password=usuario.password
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
        message_status=message_status
    )


#GET (Listar usuarios)
@app.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [
        {"id": u.id, "username": u.username, "created_at": str(u.created_at)}
        for u in usuarios
    ]


#GET (Obtener un usuario por ID)
@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": usuario.id,
        "username": usuario.username,
        "created_at": str(usuario.created_at)
    }


#PUT (Actualizar usuario)
@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos.username is not None:
        usuario.username = datos.username
    if datos.password is not None:
        usuario.password = datos.password

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
        message_status=message_status
    )


#DELETE (Eliminar usuario)
@app.delete("/usuarios/{usuario_id}")
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
