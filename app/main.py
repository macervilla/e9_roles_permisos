import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.auth import router as auth_router
from app.cache.redis_client import redis_client
from app.database import Base, engine
from app.exceptions.handlers import global_exception_handler
from app.limiter import limiter

# logger.info("api_iniciada")
from app.middlewares.logging_middleware import LoggingMiddleware
from app.routers.cargos import router as cargos_router
from app.routers.docentes import router as docentes_router
from app.routers.health import router as health_router
from app.routers.roles import router as roles_router
from app.routers.usuarios import router as usuarios_router

if os.getenv("TESTING") != "1":
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
        "https://e9-roles-permisos-1.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
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


@app.get("/redis")
def probar_redis():
    redis_client.set("hola", "mundo")

    return {"redis": redis_client.get("hola")}
