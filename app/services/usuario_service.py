from fastapi import HTTPException
from app.seguridad import hashear_clave


class UsuarioService:

    def __init__(self, repository):
        self.repository = repository

    def listar_usuarios(self):
        return self.repository.listar()

    def listar_usuarios_inactivos(self):
        return self.repository.listar_usuarios_inactivos()

    def obtener_usuario(self, usuario_id: int):
        usuario = self.repository.obtener_por_id(usuario_id)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return usuario

    def crear_usuario(self, datos):
        usuario_existente = self.repository.obtener_por_usuario(datos.usuario)

        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )

        if not self.repository.existe_rol(datos.rol_id):
            raise HTTPException(
                status_code=400,
                detail="El rol no existe"
            )

        datos.clave = hashear_clave(datos.clave)

        return self.repository.crear(datos)

    def actualizar_usuario(self, usuario_id: int, datos):
        usuario_existente = self.repository.obtener_por_usuario(datos.usuario)

        if usuario_existente and usuario_existente.id != usuario_id:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )

        if not self.repository.existe_rol(datos.rol_id):
            raise HTTPException(
                status_code=400,
                detail="El rol no existe"
            )

        usuario = self.repository.actualizar(usuario_id, datos)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return usuario

    def blanquear_clave(self, usuario_id: int):
        usuario = self.repository.obtener_por_id(usuario_id)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        clave_hash = hashear_clave(usuario.usuario)

        return self.repository.blanquear_clave(
            usuario_id,
            clave_hash
    )

    def cambiar_rol(self, usuario_id: int, rol_id: int):
        if not self.repository.existe_rol(rol_id):
            raise HTTPException(
                status_code=400,
                detail="El rol no existe"
            )

        usuario = self.repository.cambiar_rol(usuario_id, rol_id)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return usuario

    def cambiar_activo(self, usuario_id: int, activo: bool):
        usuario = self.repository.cambiar_activo(usuario_id, activo)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return usuario

    def cambiar_clave(self, usuario_id: int, nueva_clave: str):
        clave_hash = hashear_clave(nueva_clave)

        usuario = self.repository.cambiar_clave(
            usuario_id,
            clave_hash
        )

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return usuario
    