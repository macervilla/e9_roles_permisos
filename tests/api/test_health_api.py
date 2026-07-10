from unittest.mock import MagicMock, patch


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_ok(client):
    fake_db = MagicMock()

    with patch("app.routers.health.SessionLocal", return_value=fake_db):
        response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "database": "ok",
    }

    fake_db.execute.assert_called_once()
    fake_db.close.assert_called_once()


def test_ready_error(client):
    fake_db = MagicMock()
    fake_db.execute.side_effect = Exception("Base de datos no disponible")

    with patch("app.routers.health.SessionLocal", return_value=fake_db):
        response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "not ready",
        "database": "error",
    }

    fake_db.execute.assert_called_once()
    fake_db.close.assert_called_once()
