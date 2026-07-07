from app.models import RolDB, UsuarioDB
from app.seguridad import hashear_clave


def test_login_correcto(client, db_session):
    rol = RolDB(id=1, nombre="admin", activo=True)
    db_session.add(rol)

    usuario = UsuarioDB(
        usuario="admin",
        clave=hashear_clave("1234"),
        nombre="Administrador",
        rol_id=1,
        activo=True,
    )
    db_session.add(usuario)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "1234",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["rol_id"] == 1
    assert data["nombre"] == "Administrador"


def test_login_usuario_inexistente(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "noexiste",
            "password": "1234",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario o clave incorrectos"


def test_login_clave_incorrecta(client, db_session):
    rol = RolDB(id=1, nombre="admin", activo=True)
    db_session.add(rol)

    usuario = UsuarioDB(
        usuario="admin",
        clave=hashear_clave("1234"),
        nombre="Administrador",
        rol_id=1,
        activo=True,
    )
    db_session.add(usuario)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "incorrecta",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario o clave incorrectos"


def test_login_usuario_inactivo(client, db_session):
    rol = RolDB(id=1, nombre="admin", activo=True)
    db_session.add(rol)

    usuario = UsuarioDB(
        usuario="admin",
        clave=hashear_clave("1234"),
        nombre="Administrador",
        rol_id=1,
        activo=False,
    )
    db_session.add(usuario)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "1234",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Usuario inactivo"
