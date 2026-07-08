import os

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.limiter import limiter
from app.models import UsuarioDB
from app.schemas import RefreshTokenRequest, Token
from app.seguridad import crear_token, verificar_clave
from app.services.refresh_token_service import (
    crear_refresh_token,
    invalidar_refresh_token,
    rotar_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


def crear_access_token_usuario(usuario: UsuarioDB) -> str:
    return crear_token(
        {
            "sub": usuario.usuario,
            "id": usuario.id,
            "rol_id": usuario.rol_id,
        }
    )


LOGIN_RATE_LIMIT = "1000/minute" if os.getenv("TESTING") == "1" else "5/minute"


@router.post("/login", response_model=Token)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = (
        db.query(UsuarioDB).filter(UsuarioDB.usuario == form_data.username).first()
    )

    if not usuario or not verificar_clave(form_data.password, usuario.clave):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o clave incorrectos",
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    access_token = crear_access_token_usuario(usuario)
    refresh_token = crear_refresh_token(
        db,
        usuario,
        invalidar_anteriores=True,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "rol_id": usuario.rol_id,
        "nombre": usuario.nombre,
    }


@router.post("/refresh", response_model=Token)
def refresh_token(
    datos: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    usuario, nuevo_refresh_token = rotar_refresh_token(db, datos.refresh_token)
    nuevo_access_token = crear_access_token_usuario(usuario)

    return {
        "access_token": nuevo_access_token,
        "refresh_token": nuevo_refresh_token,
        "token_type": "bearer",
        "rol_id": usuario.rol_id,
        "nombre": usuario.nombre,
    }


@router.post("/logout")
def logout(
    datos: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    invalidar_refresh_token(db, datos.refresh_token)

    return {"mensaje": "Sesión cerrada correctamente"}
