from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import RolDB, UsuarioDB
from app.seguridad import hashear_clave

db: Session = SessionLocal()

try:

    # ======================
    # ROLES
    # ======================

    roles = ["Administrador", "Operador", "Consulta"]

    for nombre in roles:

        existe = db.query(RolDB).filter(RolDB.nombre == nombre).first()

        if not existe:
            db.add(RolDB(nombre=nombre, activo=True))

    db.commit()

    # ======================
    # ADMIN
    # ======================

    admin = db.query(UsuarioDB).filter(UsuarioDB.usuario == "admin").first()

    if not admin:

        rol_admin = db.query(RolDB).filter(RolDB.nombre == "Administrador").first()

        db.add(
            UsuarioDB(
                usuario="admin",
                clave=hashear_clave("admin123"),
                nombre="Administrador",
                rol_id=rol_admin.id,
                activo=True,
            )
        )

        db.commit()

    print("Seed ejecutado correctamente.")

finally:

    db.close()
