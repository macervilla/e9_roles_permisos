from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException

from app.services.docente_service import DocenteService


def crear_docente_mock(
    docente_id: int = 1,
    nombre: str = "Juan Pérez",
    provincia_id: str | None = "14",
    localidad_id: str | None = "14014020",
):
    return SimpleNamespace(
        id=docente_id,
        nombre=nombre,
        cargo_id=1,
        activo=True,
        provincia_id_georef=provincia_id,
        localidad_id_georef=localidad_id,
    )


@pytest.mark.asyncio
async def test_listar_docentes():
    docente_1 = crear_docente_mock(
        docente_id=1,
        nombre="Juan Pérez",
        provincia_id=None,
        localidad_id=None,
    )

    docente_2 = crear_docente_mock(
        docente_id=2,
        nombre="Ana Gómez",
        provincia_id=None,
        localidad_id=None,
    )

    repository = Mock()
    repository.listar.return_value = [
        docente_1,
        docente_2,
    ]

    service = DocenteService(repository)

    resultado = await service.listar_docentes()

    assert len(resultado) == 2
    assert resultado[0].nombre == "Juan Pérez"
    assert resultado[1].nombre == "Ana Gómez"

    repository.listar.assert_called_once_with()


@pytest.mark.asyncio
async def test_obtener_docente_existente():
    docente = crear_docente_mock(
        provincia_id=None,
        localidad_id=None,
    )

    repository = Mock()
    repository.obtener_por_id.return_value = docente

    service = DocenteService(repository)

    resultado = await service.obtener_docente(1)

    assert resultado is docente
    assert resultado.nombre == "Juan Pérez"
    assert resultado.provincia_nombre is None
    assert resultado.localidad_nombre is None

    repository.obtener_por_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_obtener_docente_inexistente():
    repository = Mock()
    repository.obtener_por_id.return_value = None

    service = DocenteService(repository)

    with pytest.raises(HTTPException) as exc:
        await service.obtener_docente(99)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Docente no encontrado"

    repository.obtener_por_id.assert_called_once_with(99)


@pytest.mark.asyncio
async def test_enriquecer_docente_con_georef():
    repository = Mock()
    service = DocenteService(repository)

    docente = crear_docente_mock()

    respuesta_georef = {
        "id": "14014020",
        "nombre": "Cavanagh",
        "provincia": {
            "id": "14",
            "nombre": "Córdoba",
        },
    }

    with patch(
        "app.services.docente_service.georef_service.obtener_localidad",
        new=AsyncMock(return_value=respuesta_georef),
    ) as mock_georef:
        resultado = await service.enriquecer_docente(docente)

    assert resultado.provincia_nombre == "Córdoba"
    assert resultado.localidad_nombre == "Cavanagh"

    mock_georef.assert_awaited_once_with("14014020")


@pytest.mark.asyncio
async def test_enriquecer_docente_sin_localidad():
    repository = Mock()
    service = DocenteService(repository)

    docente = crear_docente_mock(
        provincia_id=None,
        localidad_id=None,
    )

    with patch(
        "app.services.docente_service.georef_service.obtener_localidad",
        new=AsyncMock(),
    ) as mock_georef:
        resultado = await service.enriquecer_docente(docente)

    assert resultado.provincia_nombre is None
    assert resultado.localidad_nombre is None

    mock_georef.assert_not_awaited()


@pytest.mark.asyncio
async def test_enriquecer_docente_si_georef_falla():
    repository = Mock()
    service = DocenteService(repository)

    docente = crear_docente_mock()

    with patch(
        "app.services.docente_service.georef_service.obtener_localidad",
        new=AsyncMock(side_effect=Exception("Georef no disponible")),
    ) as mock_georef:
        resultado = await service.enriquecer_docente(docente)

    assert resultado.provincia_nombre is None
    assert resultado.localidad_nombre is None

    mock_georef.assert_awaited_once_with("14014020")


@pytest.mark.asyncio
async def test_listar_docentes_enriquecidos():
    docente = crear_docente_mock()

    repository = Mock()
    repository.listar.return_value = [docente]

    service = DocenteService(repository)

    respuesta_georef = {
        "id": "14014020",
        "nombre": "Cavanagh",
        "provincia": {
            "id": "14",
            "nombre": "Córdoba",
        },
    }

    with patch(
        "app.services.docente_service.georef_service.obtener_localidad",
        new=AsyncMock(return_value=respuesta_georef),
    ) as mock_georef:
        resultado = await service.listar_docentes()

    assert len(resultado) == 1
    assert resultado[0].provincia_nombre == "Córdoba"
    assert resultado[0].localidad_nombre == "Cavanagh"

    repository.listar.assert_called_once_with()
    mock_georef.assert_awaited_once_with("14014020")
