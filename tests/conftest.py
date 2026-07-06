"""
conftest.py

Infraestructura de testing reutilizable para proyectos FastAPI.

Responsabilidades:
- Crear una base SQLite en memoria.
- Crear todas las tablas antes de cada test.
- Eliminar todas las tablas al finalizar.
- Reemplazar la dependencia get_db() de FastAPI.
- Proveer un TestClient listo para usar.
"""

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.dependencies import get_db
from app.main import app


# -------------------------------------------------------------------
# Base SQLite en memoria
# -------------------------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# -------------------------------------------------------------------
# Base de datos para cada test
# -------------------------------------------------------------------

@pytest.fixture(scope="function")
def db_session():

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# -------------------------------------------------------------------
# Reemplaza get_db()
# -------------------------------------------------------------------

@pytest.fixture(scope="function")
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()