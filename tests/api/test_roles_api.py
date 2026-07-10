from app.models import RolDB, UsuarioDB
from app.seguridad import hashear_clave


def crear_admin_y_token(client, db_session):
    db_session.add(RolDB(id=1, nombre="admin", activo=True))
    db_session.add(
        UsuarioDB(
            usuario="admin",
            clave=hashear_clave("1234"),
            nombre="Administrador",
            rol_id=1,
            activo=True,
        )
    )
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "1234"},
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_listar_roles(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.get(
        "/roles/",
        headers=headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crear_rol(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.post(
        "/roles/",
        json={"nombre": "Director", "activo": True},
        headers=headers,
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["nombre"] == "Director"
    assert data["activo"] is True


def test_obtener_rol_inexistente(client):
    response = client.get("/roles/999")

    assert response.status_code == 404


def test_actualizar_rol(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    rol = RolDB(nombre="Viejo", activo=True)
    db_session.add(rol)
    db_session.commit()
    db_session.refresh(rol)

    response = client.put(
        f"/roles/{rol.id}",
        json={"nombre": "Nuevo", "activo": True},
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == rol.id
    assert data["nombre"] == "Nuevo"
    assert data["activo"] is True


def test_eliminar_rol(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    rol = RolDB(nombre="Eliminar", activo=True)
    db_session.add(rol)
    db_session.commit()
    db_session.refresh(rol)

    response = client.delete(
        f"/roles/{rol.id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == rol.id
    assert data["activo"] is False


def test_eliminar_rol_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.delete(
        "/roles/999",
        headers=headers,
    )

    assert response.status_code == 404


def test_crear_rol_sin_token(client):
    response = client.post(
        "/roles/",
        json={"nombre": "Director", "activo": True},
    )

    assert response.status_code == 401


def test_crear_rol_con_datos_invalidos(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.post(
        "/roles/",
        json={},
        headers=headers,
    )

    assert response.status_code == 422
