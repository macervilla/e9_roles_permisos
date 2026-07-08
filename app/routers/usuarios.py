import json

from fastapi import APIRouter, Depends

from app.cache.redis_client import redis_client
from app.dependencies import get_usuario_service
from app.schemas import (
    ActivoUpdate,
    UsuarioClaveUpdate,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioRolUpdate,
    UsuarioUpdate,
)
from app.seguridad import requiere_roles
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

CACHE_USUARIOS_LISTA = "usuarios:lista"
CACHE_USUARIOS_INACTIVOS = "usuarios:inactivos"
CACHE_TTL_SEGUNDOS = 60


def limpiar_cache_usuarios():
    redis_client.delete(CACHE_USUARIOS_LISTA)
    redis_client.delete(CACHE_USUARIOS_INACTIVOS)


def usuario_a_dict(usuario):
    return UsuarioResponse.model_validate(usuario).model_dump()


@router.get(
    "/",
    response_model=list[UsuarioResponse],
    dependencies=[Depends(requiere_roles([1]))],
)
def listar_usuarios(service: UsuarioService = Depends(get_usuario_service)):
    cache = redis_client.get(CACHE_USUARIOS_LISTA)

    if cache:
        print("Usuarios activos obtenidos desde Redis")
        return json.loads(cache)

    print("Usuarios activos obtenidos desde MySQL")

    usuarios = service.listar_usuarios()
    resultado = [usuario_a_dict(usuario) for usuario in usuarios]

    redis_client.setex(
        CACHE_USUARIOS_LISTA,
        CACHE_TTL_SEGUNDOS,
        json.dumps(resultado),
    )

    return resultado


@router.get(
    "/inactivos",
    response_model=list[UsuarioResponse],
    dependencies=[Depends(requiere_roles([1]))],
)
def listar_usuarios_inactivos(service: UsuarioService = Depends(get_usuario_service)):
    cache = redis_client.get(CACHE_USUARIOS_INACTIVOS)

    if cache:
        print("Usuarios inactivos obtenidos desde Redis")
        return json.loads(cache)

    print("Usuarios inactivos obtenidos desde MySQL")

    usuarios = service.listar_usuarios_inactivos()
    resultado = [usuario_a_dict(usuario) for usuario in usuarios]

    redis_client.setex(
        CACHE_USUARIOS_INACTIVOS,
        CACHE_TTL_SEGUNDOS,
        json.dumps(resultado),
    )

    return resultado


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def obtener_usuario(
    usuario_id: int,
    service: UsuarioService = Depends(get_usuario_service),
):
    return service.obtener_usuario(usuario_id)


@router.post(
    "/",
    response_model=UsuarioResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def crear_usuario(
    datos: UsuarioCreate,
    service: UsuarioService = Depends(get_usuario_service),
):
    usuario = service.crear_usuario(datos)
    limpiar_cache_usuarios()
    return usuario


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def actualizar_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    service: UsuarioService = Depends(get_usuario_service),
):
    usuario = service.actualizar_usuario(usuario_id, datos)
    limpiar_cache_usuarios()
    return usuario


@router.put(
    "/{usuario_id}/clave",
    response_model=UsuarioResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def actualizar_clave(
    usuario_id: int,
    datos: UsuarioClaveUpdate,
    service: UsuarioService = Depends(get_usuario_service),
):
    usuario = service.cambiar_clave(usuario_id, datos.clave)
    limpiar_cache_usuarios()
    return usuario


@router.put(
    "/{usuario_id}/blanquear-clave",
    response_model=UsuarioResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def blanquear_clave(
    usuario_id: int,
    service: UsuarioService = Depends(get_usuario_service),
):
    usuario = service.blanquear_clave(usuario_id)
    limpiar_cache_usuarios()
    return usuario


@router.put(
    "/{usuario_id}/rol",
    response_model=UsuarioResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def cambiar_rol(
    usuario_id: int,
    datos: UsuarioRolUpdate,
    service: UsuarioService = Depends(get_usuario_service),
):
    usuario = service.cambiar_rol(usuario_id, datos.rol_id)
    limpiar_cache_usuarios()
    return usuario


@router.put(
    "/{usuario_id}/activo",
    response_model=UsuarioResponse,
    dependencies=[Depends(requiere_roles([1]))],
)
def cambiar_activo(
    usuario_id: int,
    datos: ActivoUpdate,
    service: UsuarioService = Depends(get_usuario_service),
):
    usuario = service.cambiar_activo(usuario_id, datos.activo)
    limpiar_cache_usuarios()
    return usuario
