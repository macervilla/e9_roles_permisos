from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_crear_cargo():

    response = client.post("/cargos/", json={"nombre": "Director"})

    assert response.status_code == 200

    data = response.json()

    assert data["nombre"] == "Director"


def test_listar_cargos():

    response = client.get("/cargos/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_obtener_cargo():

    response = client.get("/cargos/1")

    assert response.status_code == 200
