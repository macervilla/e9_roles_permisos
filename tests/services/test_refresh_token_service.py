from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.services.refresh_token_service import (
    crear_refresh_token,
    generar_refresh_token,
    hashear_refresh_token,
    invalidar_refresh_token,
    invalidar_refresh_tokens_usuario,
    rotar_refresh_token,
)


def test_generar_refresh_token():
    token = generar_refresh_token()

    assert isinstance(token, str)
    assert len(token) > 40


def test_hashear_refresh_token():
    token = "mi_token"

    hash1 = hashear_refresh_token(token)
    hash2 = hashear_refresh_token(token)

    assert hash1 == hash2
    assert hash1 != token
    assert len(hash1) == 64


def test_crear_refresh_token():
    db = MagicMock()

    usuario = MagicMock()
    usuario.id = 1

    token = crear_refresh_token(db, usuario)

    assert isinstance(token, str)
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_crear_refresh_token_invalidando_anteriores():
    db = MagicMock()

    usuario = MagicMock()
    usuario.id = 5

    with patch(
        "app.services.refresh_token_service.invalidar_refresh_tokens_usuario"
    ) as mock_invalidar:
        crear_refresh_token(db, usuario, invalidar_anteriores=True)

    mock_invalidar.assert_called_once_with(db, 5)


def test_rotar_refresh_token_invalido():
    db = MagicMock()

    query = MagicMock()
    filtro = MagicMock()

    db.query.return_value = query
    query.filter.return_value = filtro
    filtro.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        rotar_refresh_token(db, "abc")

    assert exc.value.status_code == 401
    assert exc.value.detail == "Refresh token inválido"


def test_rotar_refresh_token_expirado():
    db = MagicMock()

    registro = MagicMock()
    registro.expira_en = datetime.utcnow() - timedelta(days=1)
    registro.activo = True

    query = MagicMock()
    filtro = MagicMock()

    db.query.return_value = query
    query.filter.return_value = filtro
    filtro.first.return_value = registro

    with pytest.raises(HTTPException) as exc:
        rotar_refresh_token(db, "abc")

    assert exc.value.status_code == 401
    assert exc.value.detail == "Refresh token expirado"

    assert registro.activo is False
    db.commit.assert_called()


def test_rotar_refresh_token_usuario_inactivo():
    db = MagicMock()

    registro = MagicMock()
    registro.expira_en = datetime.utcnow() + timedelta(days=1)
    registro.usuario_id = 1
    registro.activo = True

    usuario = MagicMock()
    usuario.activo = False

    query_refresh = MagicMock()
    filtro_refresh = MagicMock()

    query_usuario = MagicMock()
    filtro_usuario = MagicMock()

    db.query.side_effect = [
        query_refresh,
        query_usuario,
    ]

    query_refresh.filter.return_value = filtro_refresh
    filtro_refresh.first.return_value = registro

    query_usuario.filter.return_value = filtro_usuario
    filtro_usuario.first.return_value = usuario

    with pytest.raises(HTTPException) as exc:
        rotar_refresh_token(db, "abc")

    assert exc.value.status_code == 401
    assert exc.value.detail == "Usuario inválido"


def test_rotar_refresh_token_ok():
    db = MagicMock()

    registro = MagicMock()
    registro.expira_en = datetime.utcnow() + timedelta(days=1)
    registro.usuario_id = 1
    registro.activo = True

    usuario = MagicMock()
    usuario.id = 1
    usuario.activo = True

    query_refresh = MagicMock()
    filtro_refresh = MagicMock()

    query_usuario = MagicMock()
    filtro_usuario = MagicMock()

    db.query.side_effect = [
        query_refresh,
        query_usuario,
    ]

    query_refresh.filter.return_value = filtro_refresh
    filtro_refresh.first.return_value = registro

    query_usuario.filter.return_value = filtro_usuario
    filtro_usuario.first.return_value = usuario

    with patch(
        "app.services.refresh_token_service.crear_refresh_token",
        return_value="nuevo_refresh",
    ):
        usuario_devuelto, token = rotar_refresh_token(db, "abc")

    assert usuario_devuelto == usuario
    assert token == "nuevo_refresh"

    assert registro.activo is False
    db.commit.assert_called()


def test_invalidar_refresh_token_existente():
    db = MagicMock()

    registro = MagicMock()
    registro.activo = True

    query = MagicMock()
    filtro = MagicMock()

    db.query.return_value = query
    query.filter.return_value = filtro
    filtro.first.return_value = registro

    invalidar_refresh_token(db, "abc")

    assert registro.activo is False
    db.commit.assert_called_once()


def test_invalidar_refresh_token_inexistente():
    db = MagicMock()

    query = MagicMock()
    filtro = MagicMock()

    db.query.return_value = query
    query.filter.return_value = filtro
    filtro.first.return_value = None

    invalidar_refresh_token(db, "abc")

    db.commit.assert_not_called()


def test_invalidar_refresh_tokens_usuario():
    db = MagicMock()

    query = MagicMock()
    filtro = MagicMock()

    db.query.return_value = query
    query.filter.return_value = filtro

    invalidar_refresh_tokens_usuario(db, 7)

    filtro.update.assert_called_once_with({"activo": False})
    db.commit.assert_called_once()
