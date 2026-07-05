from fastapi import APIRouter, Depends

from app.schemas import (
    ActivoUpdate,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioRolUpdate,
    UsuarioUpdate,
    UsuarioClaveUpdate
)

from app.services.usuario_service import UsuarioService
from app.dependencies import get_usuario_service
from app.schemas import CambiarClave


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.listar_usuarios()

@router.get("/inactivos", response_model=list[UsuarioResponse])
def listar_usuarios_inactivos(
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.listar_usuarios_inactivos()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.obtener_usuario(usuario_id)


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(
    datos: UsuarioCreate,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.crear_usuario(datos)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.actualizar_usuario(usuario_id, datos)

@router.put("/{usuario_id}/clave", response_model=UsuarioResponse)
def cambiar_clave(
    usuario_id: int,
    datos: UsuarioClaveUpdate,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.cambiar_clave(usuario_id, datos.clave)

@router.put("/{usuario_id}/blanquear-clave", response_model=UsuarioResponse)
def blanquear_clave(
    usuario_id: int,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.blanquear_clave(usuario_id)

@router.put("/{usuario_id}/rol", response_model=UsuarioResponse)
def cambiar_rol(
    usuario_id: int,
    datos: UsuarioRolUpdate,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.cambiar_rol(usuario_id, datos.rol_id)


@router.put("/{usuario_id}/activo", response_model=UsuarioResponse)
def cambiar_activo(
    usuario_id: int,
    datos: ActivoUpdate,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.cambiar_activo(usuario_id, datos.activo)

@router.put("/{id}/cambiar-clave")
def cambiar_clave(
    id: int,
    datos: CambiarClave,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.cambiar_clave(id, datos.nueva_clave)

