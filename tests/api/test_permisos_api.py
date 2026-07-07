from app.models import RolDB, UsuarioDB
from app.seguridad import hashear_clave


def crear_usuario(db_session, usuario, clave, nombre, rol_id):
    db_session.add(RolDB(id=rol_id, nombre=nombre, activo=True))
    db_session.add(
        UsuarioDB(
            usuario=usuario,
            clave=hashear_clave(clave),
            nombre=nombre,
            rol_id=rol_id,
            activo=True,
        )
    )
    db_session.commit()


def obtener_token(client, usuario, clave):
    response = client.post(
        "/auth/login",
        data={"username": usuario, "password": clave},
    )
    return response.json()["access_token"]


def test_consulta_no_puede_crear_cargo(client, db_session):
    crear_usuario(db_session, "consulta", "1234", "Consulta", 3)

    token = obtener_token(client, "consulta", "1234")

    response = client.post(
        "/cargos/",
        json={"nombre": "Director"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_admin_puede_crear_cargo(client, db_session):
    crear_usuario(db_session, "admin", "1234", "Admin", 1)

    token = obtener_token(client, "admin", "1234")

    response = client.post(
        "/cargos/",
        json={"nombre": "Director"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code in (200, 201)
    assert response.json()["nombre"] == "Director"
