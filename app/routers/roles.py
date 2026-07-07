from fastapi import APIRouter, Depends

from app.dependencies import get_rol_service
from app.schemas import RolCreate, RolResponse, RolUpdate
from app.seguridad import requiere_roles
from app.services.rol_service import RolService

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get(
    "/",
    response_model=list[RolResponse],
    dependencies=[Depends(requiere_roles([1]))],
)
def listar_roles(service: RolService = Depends(get_rol_service)):
    return service.listar_roles()


@router.get(
    "/{rol_id}",
    response_model=RolResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def obtener_rol(
    rol_id: int,
    service: RolService = Depends(get_rol_service),
):
    return service.obtener_rol(rol_id)


@router.post(
    "/",
    response_model=RolResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def crear_rol(
    rol: RolCreate,
    service: RolService = Depends(get_rol_service),
):
    return service.crear_rol(rol)


@router.put(
    "/{rol_id}",
    response_model=RolResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def actualizar_rol(
    rol_id: int,
    rol: RolUpdate,
    service: RolService = Depends(get_rol_service),
):
    return service.actualizar_rol(rol_id, rol)


@router.delete(
    "/{rol_id}",
    response_model=RolResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def eliminar_rol(
    rol_id: int,
    service: RolService = Depends(get_rol_service),
):
    return service.eliminar_rol(rol_id)
