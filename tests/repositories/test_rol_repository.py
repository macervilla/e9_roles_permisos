from types import SimpleNamespace

from app.models import RolDB
from app.repositories.rol_repository import RolRepository


def test_listar_roles_activos(db_session):
    db_session.add(RolDB(nombre="admin", activo=True))
    db_session.add(RolDB(nombre="consulta", activo=False))
    db_session.commit()

    repo = RolRepository(db_session)

    resultado = repo.listar()

    assert len(resultado) == 1
    assert resultado[0].nombre == "admin"
    assert resultado[0].activo is True


def test_listar_roles_inactivos(db_session):
    db_session.add(RolDB(nombre="admin", activo=True))
    db_session.add(RolDB(nombre="consulta", activo=False))
    db_session.commit()

    repo = RolRepository(db_session)

    resultado = repo.listarinactivos()

    assert len(resultado) == 1
    assert resultado[0].nombre == "consulta"
    assert resultado[0].activo is False


def test_obtener_rol_por_id_existente(db_session):
    rol = RolDB(nombre="admin", activo=True)
    db_session.add(rol)
    db_session.commit()
    db_session.refresh(rol)

    repo = RolRepository(db_session)

    resultado = repo.obtener_por_id(rol.id)

    assert resultado is not None
    assert resultado.id == rol.id
    assert resultado.nombre == "admin"


def test_obtener_rol_por_id_inexistente(db_session):
    repo = RolRepository(db_session)

    resultado = repo.obtener_por_id(999)

    assert resultado is None


def test_crear_rol(db_session):
    repo = RolRepository(db_session)
    datos = SimpleNamespace(nombre="operador")

    resultado = repo.crear(datos)

    assert resultado.id is not None
    assert resultado.nombre == "operador"
    assert resultado.activo is True


def test_actualizar_rol_existente(db_session):
    rol = RolDB(nombre="viejo", activo=True)
    db_session.add(rol)
    db_session.commit()
    db_session.refresh(rol)

    repo = RolRepository(db_session)
    datos = SimpleNamespace(nombre="nuevo", activo=False)

    resultado = repo.actualizar(rol.id, datos)

    assert resultado is not None
    assert resultado.nombre == "nuevo"
    assert resultado.activo is False


def test_actualizar_rol_inexistente(db_session):
    repo = RolRepository(db_session)
    datos = SimpleNamespace(nombre="no existe", activo=True)

    resultado = repo.actualizar(999, datos)

    assert resultado is None


def test_eliminar_rol_existente(db_session):
    rol = RolDB(nombre="eliminar", activo=True)
    db_session.add(rol)
    db_session.commit()
    db_session.refresh(rol)

    repo = RolRepository(db_session)

    resultado = repo.eliminar(rol.id)

    assert resultado is not None
    assert resultado.id == rol.id
    assert resultado.activo is False


def test_eliminar_rol_inexistente(db_session):
    repo = RolRepository(db_session)

    resultado = repo.eliminar(999)

    assert resultado is None
