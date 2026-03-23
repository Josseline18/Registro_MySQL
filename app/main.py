# El archivo principal: levanta FastAPI, recibe el POST, guarda el cliente en MySQL y llama a rabbit_producer.py para enviar el mensaje a RabbitMQ.
from fastapi import FastAPI
from app.infrastructure.database import engine, Base
from app.domain.models import Cliente  # noqa: F401 - necesario para crear tablas
from app.adapters.routes import router

# Crear las tablas en MySQL al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Registro de Clientes",
    description="Registra clientes en MySQL y envía mensajes a RabbitMQ",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "API de Registro de Clientes - RabbitMQ + MySQL"}


app.include_router(router)
