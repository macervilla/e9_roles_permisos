from sqlalchemy.orm import Session
from app.models import CargoDB, DocenteDB
from app.schemas import DocenteCreate


class DocenteRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(DocenteDB).filter(DocenteDB.activo == True).all()

    def listar_docentes_inactivos(self):
        return self.db.query(DocenteDB).filter(DocenteDB.activo == False).all()

    def obtener_por_id(self, docente_id: int):
        return self.db.query(DocenteDB).filter(DocenteDB.id == docente_id).first()

    def existe_cargo(self, cargo_id: int):
        return self.db.query(CargoDB).filter(CargoDB.id == cargo_id).first() is not None

    def crear(self, docente: DocenteCreate):
        nuevo_docente = DocenteDB(**docente.model_dump())

        self.db.add(nuevo_docente)
        self.db.commit()
        self.db.refresh(nuevo_docente)

        return nuevo_docente

    def actualizar(self, docente_id: int, datos: DocenteCreate):
        docente = self.obtener_por_id(docente_id)

        if not docente:
            return None

        docente.nombre = datos.nombre
        docente.cargo_id = datos.cargo_id
        docente.activo = datos.activo

        self.db.commit()
        self.db.refresh(docente)

        return docente

    def cambiar_activo(self, docente_id: int, activo: bool):
        docente = self.obtener_por_id(docente_id)

        if not docente:
            return None

        docente.activo = activo

        self.db.commit()
        self.db.refresh(docente)

        return docente
