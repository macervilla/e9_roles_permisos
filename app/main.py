import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.auth import router as auth_router
from app.database import Base, engine
from app.exceptions.handlers import global_exception_handler

# logger.info("api_iniciada")
from app.middlewares.logging_middleware import LoggingMiddleware
from app.routers.cargos import router as cargos_router
from app.routers.docentes import router as docentes_router
from app.routers.health import router as health_router
from app.routers.roles import router as roles_router
from app.routers.usuarios import router as usuarios_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Etapa e9 - Roles y permisos",
    version="0.1.0",
    root_path=os.getenv("ROOT_PATH", ""),
)
app.add_exception_handler(Exception, global_exception_handler)
app.add_middleware(LoggingMiddleware)
Instrumentator().instrument(app).expose(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(cargos_router)
app.include_router(docentes_router)
app.include_router(roles_router)
app.include_router(health_router)


@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}


@app.get("/error")
def provocar_error():
    return 1 / 0
