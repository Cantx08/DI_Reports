from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Publicaciones y Certificaciones de Scopus",
    description="API para consulta de publicaciones académicas de Scopus y generación de reportes.",
    version="1.0.0"
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


@app.get("/health")
async def health_check():
    """Endpoint de salud."""
    return {"status": "healthy", "message": "API funcionando correctamente"}