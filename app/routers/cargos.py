from fastapi import APIRouter, Depends, HTTPException

from app.schemas import CargoCreate, CargoResponse, CargoUpdate
from app.services.cargo_service import CargoService
from app.dependencies import get_cargo_service
from app.seguridad import obtener_usuario_actual, requiere_roles

router = APIRouter(prefix="/cargos", tags=["Cargos"])


@router.get("/", response_model=list[CargoResponse])
def listar_cargos(service: CargoService = Depends(get_cargo_service)):
    return service.listar_cargos()


@router.get("/inactivos", response_model=list[CargoResponse])
def listar_cargos_inactivos(service: CargoService = Depends(get_cargo_service)):
    return service.listar_cargos_inactivos()


@router.get("/{cargo_id}", response_model=CargoResponse)
def obtener_cargo(cargo_id: int, service: CargoService = Depends(get_cargo_service)):
    try:
        return service.obtener_cargo(cargo_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/", response_model=CargoResponse)
def crear_cargo(datos: CargoCreate, service: CargoService = Depends(get_cargo_service)):
    return service.crear_cargo(datos)


@router.put("/{cargo_id}", response_model=CargoResponse)
def actualizar_cargo(
    cargo_id: int,
    datos: CargoUpdate,
    service: CargoService = Depends(get_cargo_service),
):
    try:
        return service.actualizar_cargo(cargo_id, datos)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{cargo_id}", response_model=CargoResponse)
def eliminar_cargo(cargo_id: int, service: CargoService = Depends(get_cargo_service)):
    try:
        return service.eliminar_cargo(cargo_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
