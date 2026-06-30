from fastapi import APIRouter, Depends

from app.schemas import ActivoUpdate, DocenteCreate, DocenteResponse
from app.services.docente_service import DocenteService
from app.dependencies import get_docente_service


router = APIRouter(
    prefix="/docentes",
    tags=["Docentes"]
)


@router.get("/", response_model=list[DocenteResponse])
def listar_docentes(
    service: DocenteService = Depends(get_docente_service)
):
    return service.listar_docentes()

@router.get("/inactivos", response_model=list[DocenteResponse])
def listar_docentes_inactivos(
    service: DocenteService = Depends(get_docente_service)
):
    return service.listar_docentes_inactivos()

@router.get("/{docente_id}", response_model=DocenteResponse)
def obtener_docente(
    docente_id: int,
    service: DocenteService = Depends(get_docente_service)
):
    return service.obtener_docente(docente_id)


@router.post("/", response_model=DocenteResponse)
def crear_docente(
    docente: DocenteCreate,
    service: DocenteService = Depends(get_docente_service)
):
    return service.crear_docente(docente)


@router.put("/{docente_id}", response_model=DocenteResponse)
def actualizar_docente(
    docente_id: int,
    docente: DocenteCreate,
    service: DocenteService = Depends(get_docente_service)
):
    return service.actualizar_docente(docente_id, docente)


@router.put("/{docente_id}/activo", response_model=DocenteResponse)
def cambiar_activo(
    docente_id: int,
    datos: ActivoUpdate,
    service: DocenteService = Depends(get_docente_service)
):
    return service.cambiar_activo(docente_id, datos.activo)
