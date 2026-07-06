from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_rol_service
from app.schemas import RolCreate, RolResponse, RolUpdate
from app.services.rol_service import RolService

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=list[RolResponse])
def listar_roles(service: RolService = Depends(get_rol_service)):
    return service.listar_roles()


@router.get("/inactivos", response_model=list[RolResponse])
def listar_roles_inactivos(service: RolService = Depends(get_rol_service)):
    return service.listar_rolesinactivos()


@router.get("/{rol_id}", response_model=RolResponse)
def obtener_rol(rol_id: int, service: RolService = Depends(get_rol_service)):
    return service.obtener_rol(rol_id)


@router.post("/", response_model=RolResponse)
def crear_rol(datos: RolCreate, service: RolService = Depends(get_rol_service)):
    return service.crear_rol(datos)


@router.put("/{rol_id}", response_model=RolResponse)
def actualizar_rol(
    rol_id: int, datos: RolUpdate, service: RolService = Depends(get_rol_service)
):
    try:
        return service.actualizar_rol(rol_id, datos)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{rol_id}", response_model=RolResponse)
def eliminar_rol(rol_id: int, service: RolService = Depends(get_rol_service)):
    try:
        return service.eliminar_rol(rol_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
