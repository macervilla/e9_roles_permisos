from app.models import CargoDB, DocenteDB, RolDB, UsuarioDB
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


def crear_cargo(db_session):
    cargo = CargoDB(nombre="Profesor", activo=True)

    db_session.add(cargo)
    db_session.commit()
    db_session.refresh(cargo)

    return cargo


def test_listar_docentes(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.get("/docentes/", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crear_docente(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    cargo = crear_cargo(db_session)

    response = client.post(
        "/docentes/",
        json={
            "nombre": "Juan Perez",
            "cargo_id": cargo.id,
            "activo": True,
        },
        headers=headers,
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["nombre"] == "Juan Perez"
    assert data["cargo_id"] == cargo.id
    assert data["activo"] is True


def test_obtener_docente_existente(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    cargo = crear_cargo(db_session)

    docente = DocenteDB(
        nombre="Carlos",
        cargo_id=cargo.id,
        activo=True,
    )

    db_session.add(docente)
    db_session.commit()
    db_session.refresh(docente)

    response = client.get(f"/docentes/{docente.id}", headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == docente.id
    assert data["nombre"] == "Carlos"
    assert data["cargo_id"] == cargo.id
    assert data["activo"] is True


def test_obtener_docente_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.get("/docentes/999", headers=headers)

    assert response.status_code == 404


def test_actualizar_docente(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    cargo = crear_cargo(db_session)

    docente = DocenteDB(
        nombre="Viejo",
        cargo_id=cargo.id,
        activo=True,
    )

    db_session.add(docente)
    db_session.commit()
    db_session.refresh(docente)

    response = client.put(
        f"/docentes/{docente.id}",
        json={
            "nombre": "Nuevo",
            "cargo_id": cargo.id,
            "activo": True,
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == docente.id
    assert data["nombre"] == "Nuevo"
    assert data["cargo_id"] == cargo.id
    assert data["activo"] is True


def test_actualizar_docente_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    cargo = crear_cargo(db_session)

    response = client.put(
        "/docentes/999",
        json={
            "nombre": "Nuevo",
            "cargo_id": cargo.id,
            "activo": True,
        },
        headers=headers,
    )

    assert response.status_code == 404


def test_inactivar_docente(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    cargo = crear_cargo(db_session)

    docente = DocenteDB(
        nombre="Pedro",
        cargo_id=cargo.id,
        activo=True,
    )

    db_session.add(docente)
    db_session.commit()
    db_session.refresh(docente)

    response = client.put(
        f"/docentes/{docente.id}/activo",
        json={"activo": False},
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == docente.id
    assert data["activo"] is False


def test_listar_docentes_sin_token(client):
    response = client.get("/docentes/")

    assert response.status_code == 401


def test_crear_docente_sin_token(client, db_session):
    cargo = crear_cargo(db_session)

    response = client.post(
        "/docentes/",
        json={
            "nombre": "Juan",
            "cargo_id": cargo.id,
            "activo": True,
        },
    )

    assert response.status_code == 401


def test_crear_docente_con_cargo_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.post(
        "/docentes/",
        json={
            "nombre": "Juan",
            "cargo_id": 999,
            "activo": True,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El cargo no existe"


def test_crear_docente_datos_invalidos(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.post(
        "/docentes/",
        json={},
        headers=headers,
    )

    assert response.status_code == 422
