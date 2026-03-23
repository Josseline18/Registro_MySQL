from fastapi import FastAPI
from taller_mecanica.adapters.routes import router
from taller_mecanica.infrastructure.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservicio Taller Mecanica")
app.include_router(router)
