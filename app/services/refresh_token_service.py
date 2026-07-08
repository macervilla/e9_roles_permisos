import hashlib
import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import RefreshTokenDB, UsuarioDB

REFRESH_TOKEN_EXPIRE_DAYS = 7


def generar_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hashear_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def crear_refresh_token(
    db: Session,
    usuario: UsuarioDB,
    invalidar_anteriores: bool = False,
) -> str:
    if invalidar_anteriores:
        invalidar_refresh_tokens_usuario(db, usuario.id)

    token = generar_refresh_token()
    token_hash = hashear_refresh_token(token)

    nuevo_refresh = RefreshTokenDB(
        usuario_id=usuario.id,
        token_hash=token_hash,
        activo=True,
        expira_en=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.add(nuevo_refresh)
    db.commit()

    return token


def rotar_refresh_token(db: Session, refresh_token: str) -> tuple[UsuarioDB, str]:
    token_hash = hashear_refresh_token(refresh_token)

    registro = (
        db.query(RefreshTokenDB)
        .filter(
            RefreshTokenDB.token_hash == token_hash,
            RefreshTokenDB.activo == True,
        )
        .first()
    )

    if not registro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido",
        )

    if registro.expira_en < datetime.utcnow():
        registro.activo = False
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expirado",
        )

    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == registro.usuario_id).first()

    if not usuario or not usuario.activo:
        registro.activo = False
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inválido",
        )

    registro.activo = False

    nuevo_refresh_token = crear_refresh_token(db, usuario)

    db.commit()

    return usuario, nuevo_refresh_token


def invalidar_refresh_token(db: Session, refresh_token: str) -> None:
    token_hash = hashear_refresh_token(refresh_token)

    registro = (
        db.query(RefreshTokenDB)
        .filter(
            RefreshTokenDB.token_hash == token_hash,
            RefreshTokenDB.activo == True,
        )
        .first()
    )

    if registro:
        registro.activo = False
        db.commit()


def invalidar_refresh_tokens_usuario(db: Session, usuario_id: int) -> None:
    db.query(RefreshTokenDB).filter(
        RefreshTokenDB.usuario_id == usuario_id,
        RefreshTokenDB.activo == True,
    ).update({"activo": False})

    db.commit()
