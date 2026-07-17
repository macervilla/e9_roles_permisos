from fastapi import HTTPException

from app.services.georef_service import georef_service


class DocenteService:
    def __init__(self, repository):
        self.repository = repository

    async def enriquecer_docente(self, docente):
        docente.provincia_nombre = None
        docente.localidad_nombre = None

        if not docente.localidad_id_georef:
            return docente

        try:
            localidad = await georef_service.obtener_localidad(
                docente.localidad_id_georef
            )

            if not localidad:
                return docente

            docente.localidad_nombre = localidad.get("nombre")

            provincia = localidad.get("provincia") or {}
            docente.provincia_nombre = provincia.get("nombre")

        except Exception as error:
            print(f"No se pudo enriquecer el docente {docente.id}: {error}")

        return docente

    async def listar_docentes(self):
        docentes = self.repository.listar()
        resultado = []

        for docente in docentes:
            docente_enriquecido = await self.enriquecer_docente(docente)
            resultado.append(docente_enriquecido)

        return resultado

    async def listar_docentes_inactivos(self):
        docentes = self.repository.listar_docentes_inactivos()
        resultado = []

        for docente in docentes:
            docente_enriquecido = await self.enriquecer_docente(docente)
            resultado.append(docente_enriquecido)

        return resultado

    async def obtener_docente(self, docente_id: int):
        docente = self.repository.obtener_por_id(docente_id)

        if not docente:
            raise HTTPException(
                status_code=404,
                detail="Docente no encontrado",
            )

        return await self.enriquecer_docente(docente)

    def crear_docente(self, docente):
        if not self.repository.existe_cargo(docente.cargo_id):
            raise HTTPException(
                status_code=400,
                detail="El cargo no existe",
            )

        return self.repository.crear(docente)

    def actualizar_docente(self, docente_id: int, datos):
        if not self.repository.existe_cargo(datos.cargo_id):
            raise HTTPException(
                status_code=400,
                detail="El cargo no existe",
            )

        docente = self.repository.actualizar(
            docente_id,
            datos,
        )

        if not docente:
            raise HTTPException(
                status_code=404,
                detail="Docente no encontrado",
            )

        return docente

    def cambiar_activo(
        self,
        docente_id: int,
        activo: bool,
    ):
        docente = self.repository.cambiar_activo(
            docente_id,
            activo,
        )

        if not docente:
            raise HTTPException(
                status_code=404,
                detail="Docente no encontrado",
            )

        return docente
