from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.db import engine
from src.infrastructure.models.base import Base
from src.infrastructure.api.controllers import department_controller, author_controller, scopus_account_controller
# Importar todos los modelos para que se registren
from src.infrastructure.models import department, author, scopus_account


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Sistema de Publicaciones y Certificaciones de Scopus",
    description="API para consulta de publicaciones académicas de Scopus y generación de reportes.",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar routers
app.include_router(department_controller.router)
app.include_router(author_controller.router)
app.include_router(scopus_account_controller.router)


@app.get("/health")
async def health_check():
    """Endpoint de salud."""
    return {"status": "healthy", "message": "API funcionando correctamente"}
