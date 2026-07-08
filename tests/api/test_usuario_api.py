from app.models import RolDB, UsuarioDB
from app.seguridad import hashear_clave, verificar_clave


def crear_admin_y_token(client, db_session):
    rol_admin = db_session.query(RolDB).filter(RolDB.id == 1).first()

    if not rol_admin:
        db_session.add(RolDB(id=1, nombre="admin", activo=True))
        db_session.commit()

    admin = db_session.query(UsuarioDB).filter(UsuarioDB.usuario == "admin").first()

    if not admin:
        admin = UsuarioDB(
            usuario="admin",
            clave=hashear_clave("1234"),
            nombre="Administrador",
            rol_id=1,
            activo=True,
        )
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "1234"},
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    token = data.get("access_token") or data.get("access") or data.get("token")

    assert token is not None, f"Login no devolvió token. Respuesta: {data}"

    return {"Authorization": f"Bearer {token}"}


def crear_rol(db_session, rol_id=2, nombre="consulta"):
    rol = db_session.query(RolDB).filter(RolDB.id == rol_id).first()

    if rol:
        return rol

    rol = RolDB(id=rol_id, nombre=nombre, activo=True)
    db_session.add(rol)
    db_session.commit()
    db_session.refresh(rol)

    return rol


def crear_usuario(db_session, usuario="juan", rol_id=1, activo=True):
    existente = db_session.query(UsuarioDB).filter(UsuarioDB.usuario == usuario).first()

    if existente:
        return existente

    crear_rol(db_session, rol_id=rol_id, nombre="admin" if rol_id == 1 else "consulta")

    nuevo = UsuarioDB(
        usuario=usuario,
        clave=hashear_clave("1234"),
        nombre="Juan Perez",
        rol_id=rol_id,
        activo=activo,
    )

    db_session.add(nuevo)
    db_session.commit()
    db_session.refresh(nuevo)

    return nuevo


def test_listar_usuarios(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.get("/usuarios/", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_usuarios_sin_token(client):
    response = client.get("/usuarios/")

    assert response.status_code == 401


def test_obtener_usuario_existente(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    usuario = crear_usuario(db_session, usuario="maria", rol_id=1)

    response = client.get(f"/usuarios/{usuario.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["usuario"] == "maria"


def test_obtener_usuario_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.get("/usuarios/999", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


def test_crear_usuario(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    crear_rol(db_session, rol_id=2, nombre="consulta")

    response = client.post(
        "/usuarios/",
        json={
            "usuario": "nuevo",
            "clave": "1234",
            "nombre": "Usuario Nuevo",
            "rol_id": 2,
        },
        headers=headers,
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["usuario"] == "nuevo"
    assert data["nombre"] == "Usuario Nuevo"
    assert data["rol_id"] == 2
    assert data["activo"] is True


def test_crear_usuario_sin_token(client):
    response = client.post(
        "/usuarios/",
        json={
            "usuario": "nuevo_sin_token",
            "clave": "1234",
            "nombre": "Usuario Nuevo",
            "rol_id": 1,
        },
    )

    assert response.status_code == 401


def test_crear_usuario_duplicado(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    crear_usuario(db_session, usuario="repetido", rol_id=1)

    response = client.post(
        "/usuarios/",
        json={
            "usuario": "repetido",
            "clave": "1234",
            "nombre": "Duplicado",
            "rol_id": 1,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El usuario ya existe"


def test_crear_usuario_rol_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.post(
        "/usuarios/",
        json={
            "usuario": "nuevo_rol_inexistente",
            "clave": "1234",
            "nombre": "Usuario Nuevo",
            "rol_id": 999,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El rol no existe"


def test_crear_usuario_datos_invalidos(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.post(
        "/usuarios/",
        json={},
        headers=headers,
    )

    assert response.status_code == 422


def test_actualizar_usuario(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    usuario = crear_usuario(db_session, usuario="viejo", rol_id=1)
    crear_rol(db_session, rol_id=2, nombre="consulta")

    response = client.put(
        f"/usuarios/{usuario.id}",
        json={
            "usuario": "nuevo_nombre",
            "nombre": "Nombre Actualizado",
            "rol_id": 2,
            "activo": True,
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["usuario"] == "nuevo_nombre"
    assert data["nombre"] == "Nombre Actualizado"
    assert data["rol_id"] == 2


def test_actualizar_usuario_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.put(
        "/usuarios/999",
        json={
            "usuario": "noexiste",
            "nombre": "No Existe",
            "rol_id": 1,
            "activo": True,
        },
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


def test_actualizar_usuario_duplicado(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    crear_usuario(db_session, usuario="usuario1", rol_id=1)
    usuario2 = crear_usuario(db_session, usuario="usuario2", rol_id=1)

    response = client.put(
        f"/usuarios/{usuario2.id}",
        json={
            "usuario": "usuario1",
            "nombre": "Duplicado",
            "rol_id": 1,
            "activo": True,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El usuario ya existe"


def test_actualizar_usuario_rol_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    usuario = crear_usuario(db_session, usuario="usuario_rol_invalido", rol_id=1)

    response = client.put(
        f"/usuarios/{usuario.id}",
        json={
            "usuario": "usuario_rol_invalido",
            "nombre": "Usuario",
            "rol_id": 999,
            "activo": True,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El rol no existe"


def test_cambiar_clave(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    usuario = crear_usuario(db_session, usuario="cambio_clave", rol_id=1)

    response = client.put(
        f"/usuarios/{usuario.id}/clave",
        json={"clave": "nueva123"},
        headers=headers,
    )

    assert response.status_code == 200

    db_session.refresh(usuario)

    assert verificar_clave("nueva123", usuario.clave)


def test_cambiar_clave_usuario_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)

    response = client.put(
        "/usuarios/999/clave",
        json={"clave": "nueva123"},
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


def test_blanquear_clave(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    usuario = crear_usuario(db_session, usuario="blanqueo", rol_id=1)

    response = client.put(
        f"/usuarios/{usuario.id}/blanquear-clave",
        headers=headers,
    )

    assert response.status_code == 200

    db_session.refresh(usuario)

    assert verificar_clave("blanqueo", usuario.clave)


def test_cambiar_rol(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    usuario = crear_usuario(db_session, usuario="cambio_rol", rol_id=1)
    crear_rol(db_session, rol_id=2, nombre="consulta")

    response = client.put(
        f"/usuarios/{usuario.id}/rol",
        json={"rol_id": 2},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["rol_id"] == 2


def test_cambiar_rol_inexistente(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    usuario = crear_usuario(db_session, usuario="rol_invalido", rol_id=1)

    response = client.put(
        f"/usuarios/{usuario.id}/rol",
        json={"rol_id": 999},
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El rol no existe"


def test_cambiar_activo(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    usuario = crear_usuario(db_session, usuario="inactivar", rol_id=1)

    response = client.put(
        f"/usuarios/{usuario.id}/activo",
        json={"activo": False},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["activo"] is False


def test_listar_usuarios_inactivos(client, db_session):
    headers = crear_admin_y_token(client, db_session)
    crear_usuario(db_session, usuario="inactivo", rol_id=1, activo=False)

    response = client.get("/usuarios/inactivos", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["usuario"] == "inactivo"
