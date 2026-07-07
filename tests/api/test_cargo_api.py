from app.models import CargoDB, RolDB, UsuarioDB
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


def test_listar_cargos(client):
    response = client.get("/cargos/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crear_cargo(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.post(
        "/cargos/",
        json={"nombre": "Director", "activo": True},
        headers=headers,
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["nombre"] == "Director"
    assert data["activo"] is True


def test_obtener_cargo_existente(client, db_session):
    cargo = CargoDB(nombre="Secretario", activo=True)
    db_session.add(cargo)
    db_session.commit()
    db_session.refresh(cargo)

    response = client.get(f"/cargos/{cargo.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == cargo.id
    assert data["nombre"] == "Secretario"


def test_obtener_cargo_inexistente(client):
    response = client.get("/cargos/999")

    assert response.status_code == 404


def test_actualizar_cargo(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    cargo = CargoDB(nombre="Viejo", activo=True)
    db_session.add(cargo)
    db_session.commit()
    db_session.refresh(cargo)

    response = client.put(
        f"/cargos/{cargo.id}",
        json={"nombre": "Nuevo", "activo": True},
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == cargo.id
    assert data["nombre"] == "Nuevo"
    assert data["activo"] is True


def test_actualizar_cargo_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.put(
        "/cargos/999",
        json={"nombre": "No existe", "activo": True},
        headers=headers,
    )

    assert response.status_code == 404


def test_eliminar_cargo(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    cargo = CargoDB(nombre="Eliminar", activo=True)
    db_session.add(cargo)
    db_session.commit()
    db_session.refresh(cargo)

    response = client.delete(
        f"/cargos/{cargo.id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == cargo.id
    assert data["activo"] is False


def test_eliminar_cargo_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.delete(
        "/cargos/999",
        headers=headers,
    )

    assert response.status_code == 404


def test_crear_cargo_sin_token(client):
    response = client.post(
        "/cargos/",
        json={"nombre": "Director", "activo": True},
    )

    assert response.status_code == 401


def test_crear_cargo_con_datos_invalidos(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.post(
        "/cargos/",
        json={},
        headers=headers,
    )

    assert response.status_code == 422
