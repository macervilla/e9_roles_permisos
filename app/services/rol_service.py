from fastapi import HTTPException


class RolService:
    def __init__(self, repository):
        self.repository = repository

    def listar_roles(self):
        return self.repository.listar()

    def listar_rolesinactivos(self):
        return self.repository.listarinactivos()

    def obtener_rol(self, rol_id: int):
        rol = self.repository.obtener_por_id(rol_id)

        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        return rol

    def crear_rol(self, datos):
        return self.repository.crear(datos)

    def actualizar_rol(self, rol_id: int, datos):
        rol = self.repository.actualizar(rol_id, datos)

        if not rol:
            raise ValueError("Rol no encontrado")

        return rol

    def eliminar_rol(self, rol_id: int):
        rol = self.repository.eliminar(rol_id)

        if not rol:
            raise ValueError("Rol no encontrado")

        return rol
