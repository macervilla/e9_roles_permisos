from unittest.mock import AsyncMock, patch

import pytest

from app.services.georef_service import GeorefService


@pytest.mark.asyncio
async def test_obtener_provincias():
    respuesta_georef = {
        "provincias": [
            {
                "id": "14",
                "nombre": "Córdoba",
            },
            {
                "id": "78",
                "nombre": "Santa Cruz",
            },
        ]
    }

    with patch(
        "app.services.georef_service.http_client.get",
        new=AsyncMock(return_value=respuesta_georef),
    ) as mock_get:
        servicio = GeorefService()

        resultado = await servicio.obtener_provincias()

    assert resultado == respuesta_georef["provincias"]

    mock_get.assert_awaited_once_with(f"{servicio.BASE_URL}/provincias")


@pytest.mark.asyncio
async def test_obtener_localidades():
    respuesta_georef = {
        "localidades": [
            {
                "id": "14014020",
                "nombre": "Cavanagh",
                "provincia": {
                    "id": "14",
                    "nombre": "Córdoba",
                },
            }
        ]
    }

    with patch(
        "app.services.georef_service.http_client.get",
        new=AsyncMock(return_value=respuesta_georef),
    ) as mock_get:
        servicio = GeorefService()

        resultado = await servicio.obtener_localidades("Córdoba")

    assert resultado == respuesta_georef["localidades"]

    mock_get.assert_awaited_once_with(
        f"{servicio.BASE_URL}/localidades",
        params={
            "provincia": "Córdoba",
            "max": 5000,
        },
    )


@pytest.mark.asyncio
async def test_obtener_localidad_por_id():
    respuesta_georef = {
        "localidades": [
            {
                "id": "14014020",
                "nombre": "Cavanagh",
                "provincia": {
                    "id": "14",
                    "nombre": "Córdoba",
                },
            }
        ]
    }

    with patch(
        "app.services.georef_service.http_client.get",
        new=AsyncMock(return_value=respuesta_georef),
    ) as mock_get:
        servicio = GeorefService()

        resultado = await servicio.obtener_localidad("14014020")

    assert resultado["id"] == "14014020"
    assert resultado["nombre"] == "Cavanagh"
    assert resultado["provincia"]["nombre"] == "Córdoba"

    mock_get.assert_awaited_once_with(
        f"{servicio.BASE_URL}/localidades",
        params={
            "id": "14014020",
        },
    )


@pytest.mark.asyncio
async def test_obtener_localidad_inexistente():
    with patch(
        "app.services.georef_service.http_client.get",
        new=AsyncMock(return_value={"localidades": []}),
    ):
        servicio = GeorefService()

        resultado = await servicio.obtener_localidad("99999999")

    assert resultado is None
