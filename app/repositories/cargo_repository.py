from sqlalchemy.orm import Session
from app.models import CargoDB


class CargoRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(CargoDB).filter(CargoDB.activo == True).all()
    
    def listar_cargos_inactivos(self):
        return self.db.query(CargoDB).filter(CargoDB.activo == False).all()

    def obtener_por_id(self, cargo_id: int):
        return self.db.query(CargoDB).filter(CargoDB.id == cargo_id).first()

    def crear(self, datos):
        cargo = CargoDB(
            nombre=datos.nombre,
            activo=datos.activo
        )

        self.db.add(cargo)
        self.db.commit()
        self.db.refresh(cargo)
        return cargo

    def actualizar(self, cargo_id: int, datos):
        cargo = self.obtener_por_id(cargo_id)

        if not cargo:
            return None

        cargo.nombre = datos.nombre
        cargo.activo = datos.activo

        self.db.commit()
        self.db.refresh(cargo)
        return cargo

    def eliminar(self, cargo_id: int):
        cargo = self.obtener_por_id(cargo_id)

        if not cargo:
            return None

        cargo.activo = False
        self.db.commit()
        self.db.refresh(cargo)
        return cargo
