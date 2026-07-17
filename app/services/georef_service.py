from httpx import HTTPError

from app.core.http_client import http_client


class GeorefService:
    BASE_URL = "https://apis.datos.gob.ar/georef/api"

    async def obtener_provincias(self):
        try:
            datos = await http_client.get(f"{self.BASE_URL}/provincias")

            return datos.get("provincias", [])

        except HTTPError as error:
            raise Exception(
                f"Error consultando provincias en Georef: {error}"
            ) from error

    async def obtener_localidades(self, provincia: str):
        try:
            datos = await http_client.get(
                f"{self.BASE_URL}/localidades",
                params={
                    "provincia": provincia,
                    "max": 5000,
                },
            )

            return datos.get("localidades", [])

        except HTTPError as error:
            raise Exception(
                f"Error consultando localidades en Georef: {error}"
            ) from error

    async def obtener_localidad(self, localidad_id: str):
        try:
            datos = await http_client.get(
                f"{self.BASE_URL}/localidades",
                params={
                    "id": localidad_id,
                },
            )

            localidades = datos.get("localidades", [])

            if not localidades:
                return None

            return localidades[0]

        except HTTPError as error:
            raise Exception(
                f"Error consultando la localidad en Georef: {error}"
            ) from error


georef_service = GeorefService()
