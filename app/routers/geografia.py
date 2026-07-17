from fastapi import APIRouter, HTTPException

from app.services.georef_service import georef_service

router = APIRouter(
    prefix="/geografia",
    tags=["Geografía"],
)


@router.get("/provincias")
async def provincias():
    try:
        return await georef_service.obtener_provincias()

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )


@router.get("/localidades")
async def localidades(provincia: str):
    try:
        return await georef_service.obtener_localidades(provincia)

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )


@router.get("/localidad/{localidad_id}")
async def obtener_localidad(localidad_id: str):
    try:
        localidad = await georef_service.obtener_localidad(localidad_id)

        if not localidad:
            raise HTTPException(
                status_code=404,
                detail="Localidad no encontrada",
            )

        return localidad

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error
