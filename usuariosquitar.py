from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import UsuarioDB
from app.schemas import UsuarioCrear, UsuarioRespuesta
from app.seguridad import hashear_clave, obtener_usuario_actual


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

from app.seguridad import hashear_clave, obtener_usuario_actual, requiere_admin
@router.post("/", response_model=UsuarioRespuesta)
def crear_usuario(
    datos: UsuarioCrear,
    db: Session = Depends(get_db),
    usuario_actual=Depends(requiere_admin)
):
    nuevo_usuario = UsuarioDB(
        usuario=datos.usuario,
        clave=hashear_clave(datos.clave),
        nombre=datos.nombre,
        rol_id=datos.rol_id,
        activo=True
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


@router.get("/", response_model=list[UsuarioRespuesta])
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    return db.query(UsuarioDB).all()