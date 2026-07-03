import os

from app.database import SessionLocal
from app.models import RolDB, UsuarioDB
from app.seguridad import hashear_clave


def main():
    db = SessionLocal()

    try:
        rol = db.query(RolDB).filter(RolDB.nombre == "administrador").first()

        if not rol:
            rol = RolDB(nombre="administrador", activo=True)
            db.add(rol)
            db.commit()
            db.refresh(rol)

        usuario = db.query(UsuarioDB).filter(UsuarioDB.usuario == "admin").first()

        if not usuario:
            usuario = UsuarioDB(
                nombre="Administrador",
                usuario="admin",
                clave=hashear_clave(os.getenv("ADMIN_CLAVE", "admin")),
                rol_id=rol.id,
                activo=True
            )
            db.add(usuario)
            db.commit()

        print("Seed inicial ejecutado correctamente")

    finally:
        db.close()


if __name__ == "__main__":
    main()