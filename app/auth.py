from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import UsuarioDB
from app.schemas import Token
from app.seguridad import verificar_clave, crear_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.usuario == form_data.username
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o clave incorrectos"
        )

    if not verificar_clave(form_data.password, usuario.clave):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o clave incorrectos"
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    token = crear_token({
        "sub": usuario.usuario,
        "id": usuario.id,
        "rol_id": usuario.rol_id
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "rol_id": usuario.rol_id,
        "nombre": usuario.nombre
    }