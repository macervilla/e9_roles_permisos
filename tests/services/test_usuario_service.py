import pytest
from fastapi import HTTPException

from app.services.usuario_service import UsuarioService


class MockRepository:

    def listar(self):
        return ["usuario1", "usuario2"]

    def listar_usuarios_inactivos(self):
        return ["usuario_inactivo"]

    def obtener_por_id(self, usuario_id):
        if usuario_id == 1:
            return {"id": 1, "usuario": "admin"}
        return None

    def obtener_por_usuario(self, usuario):

        if usuario == "existente":

            class Usuario:
                id = 1

            return Usuario()

        return None

    def existe_rol(self, rol_id):
        return rol_id == 1

    def crear(self, datos):
        return datos


@pytest.fixture
def service():
    return UsuarioService(MockRepository())


class DatosUsuario:

    def __init__(self, usuario, clave, rol_id):
        self.usuario = usuario
        self.clave = clave
        self.rol_id = rol_id


def test_listar_usuarios(service):
    resultado = service.listar_usuarios()

    assert resultado == ["usuario1", "usuario2"]


def test_listar_usuarios_inactivos(service):
    resultado = service.listar_usuarios_inactivos()

    assert resultado == ["usuario_inactivo"]


def test_obtener_usuario_existente(service):
    usuario = service.obtener_usuario(1)

    assert usuario["id"] == 1


def test_obtener_usuario_inexistente(service):

    with pytest.raises(HTTPException) as exc:

        service.obtener_usuario(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Usuario no encontrado"


def test_crear_usuario_correcto(service):

    datos = DatosUsuario(usuario="nuevo", clave="1234", rol_id=1)

    usuario = service.crear_usuario(datos)

    assert usuario.usuario == "nuevo"
    assert usuario.rol_id == 1
    assert usuario.clave != "1234"


def test_crear_usuario_existente(service):

    datos = DatosUsuario(usuario="existente", clave="1234", rol_id=1)

    with pytest.raises(HTTPException) as exc:

        service.crear_usuario(datos)

    assert exc.value.status_code == 400
    assert exc.value.detail == "El usuario ya existe"


def test_crear_usuario_rol_inexistente(service):

    datos = DatosUsuario(usuario="nuevo", clave="1234", rol_id=999)

    with pytest.raises(HTTPException) as exc:

        service.crear_usuario(datos)

    assert exc.value.status_code == 400
    assert exc.value.detail == "El rol no existe"
