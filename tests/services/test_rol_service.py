import pytest
from fastapi import HTTPException

from app.services.rol_service import RolService


class MockRolRepository:
    def listar(self):
        return [
            {"id": 1, "nombre": "Juan"},
            {"id": 2, "nombre": "Ana"},
        ]

    def obtener_por_id(self, rol_id):
        if rol_id == 1:
            return {"id": 1, "nombre": "Juan"}

        return None


def test_listar_roles():
    repo_mock = MockRolRepository()
    service = RolService(repo_mock)

    resultado = service.listar_roles()

    assert len(resultado) == 2
    assert resultado[0]["nombre"] == "Juan"


def test_obtener_rol_existente():
    repo_mock = MockRolRepository()
    service = RolService(repo_mock)

    resultado = service.obtener_rol(1)

    assert resultado is not None
    assert resultado["nombre"] == "Juan"


def test_obtener_rol_inexistente():
    repo_mock = MockRolRepository()
    service = RolService(repo_mock)

    with pytest.raises(HTTPException) as exc:
        service.obtener_rol(99)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Rol no encontrado"
