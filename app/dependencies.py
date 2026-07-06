from fastapi import Depends

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


def get_cargo_service(db=Depends(get_db)):
    return CargoService(CargoRepository(db))


def get_docente_service(db=Depends(get_db)):
    return DocenteService(DocenteRepository(db))


def get_rol_service(db=Depends(get_db)):
    return RolService(RolRepository(db))


def get_usuario_service(db=Depends(get_db)):
    return UsuarioService(UsuarioRepository(db))