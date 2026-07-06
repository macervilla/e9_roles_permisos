from app.models import RolDB


class RolRepository:

    def __init__(self, db):
        self.db = db

    def listar(self):
        return self.db.query(RolDB).filter(RolDB.activo == True).all()

    def listarinactivos(self):
        return self.db.query(RolDB).filter(RolDB.activo == False).all()

    def obtener_por_id(self, rol_id: int):
        return self.db.query(RolDB).filter(RolDB.id == rol_id).first()

    def crear(self, datos):
        rol = RolDB(nombre=datos.nombre, activo=True)

        self.db.add(rol)
        self.db.commit()
        self.db.refresh(rol)

        return rol

    def actualizar(self, rol_id: int, datos):
        rol = self.obtener_por_id(rol_id)

        if not rol:
            return None

        rol.nombre = datos.nombre
        rol.activo = datos.activo

        self.db.commit()
        self.db.refresh(rol)

        return rol

    def eliminar(self, rol_id: int):
        rol = self.obtener_por_id(rol_id)

        if not rol:
            return None

        rol.activo = False

        self.db.commit()
        self.db.refresh(rol)

        return rol
