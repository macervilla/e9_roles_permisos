from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base


class RolDB(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)


class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(50), unique=True, index=True, nullable=False)
    clave = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    activo = Column(Boolean, default=True)


class CargoDB(Base):
    __tablename__ = "cargos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)


class DocenteDB(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    cargo_id = Column(Integer, ForeignKey("cargos.id"), nullable=False)
    activo = Column(Boolean, default=True)
