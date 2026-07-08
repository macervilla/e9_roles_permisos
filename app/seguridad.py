from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "clave_super_secreta_cambiar_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hashear_clave(clave: str) -> str:
    return pwd_context.hash(clave)


def verificar_clave(clave_plana: str, clave_hash: str) -> bool:
    return pwd_context.verify(clave_plana, clave_hash)


def crear_token(data: dict):
    datos = data.copy()

    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos.update({"exp": expiracion})

    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        usuario = payload.get("sub")

        if usuario is None:
            raise credenciales_exception

        return {"usuario": usuario, "rol_id": payload.get("rol_id")}

    except JWTError:
        raise credenciales_exception


def requiere_roles(roles_permitidos: list[int]):
    def validador(usuario_actual=Depends(obtener_usuario_actual)):
        if usuario_actual["rol_id"] not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para realizar esta acción",
            )

        return usuario_actual

    return validador
