from fastapi import HTTPException


class DocenteService:
    def __init__(self, repository):
        self.repository = repository

    def listar_docentes(self):
        return self.repository.listar()

    def listar_docentes_inactivos(self):
        return self.repository.listar_docentes_inactivos()

    def obtener_docente(self, docente_id: int):
        docente = self.repository.obtener_por_id(docente_id)

        if not docente:
            raise HTTPException(status_code=404, detail="Docente no encontrado")

        return docente

    def crear_docente(self, docente):
        if not self.repository.existe_cargo(docente.cargo_id):
            raise HTTPException(status_code=400, detail="El cargo no existe")

        return self.repository.crear(docente)

    def actualizar_docente(self, docente_id: int, datos):
        if not self.repository.existe_cargo(datos.cargo_id):
            raise HTTPException(status_code=400, detail="El cargo no existe")

        docente = self.repository.actualizar(docente_id, datos)

        if not docente:
            raise HTTPException(status_code=404, detail="Docente no encontrado")

        return docente

    def cambiar_activo(self, docente_id: int, activo: bool):
        docente = self.repository.cambiar_activo(docente_id, activo)

        if not docente:
            raise HTTPException(status_code=404, detail="Docente no encontrado")

        return docente
