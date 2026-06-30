from app.database import SessionLocal

from app.repositories.cargo_repository import CargoRepository
from app.repositories.docente_repository import DocenteRepository
from app.repositories.rol_repository import RolRepository
from app.repositories.usuario_repository import UsuarioRepository

from app.services.cargo_service import CargoService
from app.services.docente_service import DocenteService
from app.services.rol_service import RolService
from app.services.usuario_service import UsuarioService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cargo_service():
    db = SessionLocal()
    try:
        repository = CargoRepository(db)
        service = CargoService(repository)
        yield service
    finally:
        db.close()


def get_docente_service():
    db = SessionLocal()
    try:
        repository = DocenteRepository(db)
        service = DocenteService(repository)
        yield service
    finally:
        db.close()


def get_rol_service():
    db = SessionLocal()
    try:
        repository = RolRepository(db)
        service = RolService(repository)
        yield service
    finally:
        db.close()


def get_usuario_service():
    db = SessionLocal()
    try:
        repository = UsuarioRepository(db)
        service = UsuarioService(repository)
        yield service
    finally:
        db.close()