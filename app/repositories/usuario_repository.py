from app.models import RolDB, UsuarioDB


class UsuarioRepository:

    def __init__(self, db):
        self.db = db

    def listar(self):
        return self.db.query(UsuarioDB).filter(UsuarioDB.activo == True).all()
    
    def listar_usuarios_inactivos(self):
        return self.db.query(UsuarioDB).filter(UsuarioDB.activo == False).all()

   
    def obtener_por_id(self, usuario_id: int):
        return self.db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()

    def obtener_por_usuario(self, usuario: str):
        return self.db.query(UsuarioDB).filter(UsuarioDB.usuario == usuario).first()

    def existe_rol(self, rol_id: int):
        return self.db.query(RolDB).filter(RolDB.id == rol_id).first() is not None

    def crear(self, datos):
        usuario = UsuarioDB(
            usuario=datos.usuario,
            nombre=datos.nombre,
            clave=datos.clave,
            rol_id=datos.rol_id,
            activo=True
        )

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)

        return usuario

    def actualizar(self, usuario_id: int, datos):
        usuario = self.obtener_por_id(usuario_id)

        if not usuario:
            return None

        usuario.usuario = datos.usuario
        usuario.nombre=datos.nombre
        usuario.rol_id = datos.rol_id

        self.db.commit()
        self.db.refresh(usuario)

        return usuario

    def cambiar_rol(self, usuario_id: int, rol_id: int):
        usuario = self.obtener_por_id(usuario_id)

        if not usuario:
            return None

        usuario.rol_id = rol_id

        self.db.commit()
        self.db.refresh(usuario)

        return usuario

    def cambiar_activo(self, usuario_id: int, activo: bool):
        usuario = self.obtener_por_id(usuario_id)

        if not usuario:
            return None

        usuario.activo = activo

        self.db.commit()
        self.db.refresh(usuario)

        return usuario
def cambiar_clave(self, usuario_id: int, clave_hash: str):
    usuario = self.obtener_por_id(usuario_id)

    if not usuario:
        return None

    usuario.clave = clave_hash

    self.db.commit()
    self.db.refresh(usuario)

    return usuario