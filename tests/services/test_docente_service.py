from app.services.docente_service import DocenteService


class MockDocenteRepository:

    def listar(self):
        return [
            {"id": 1, "nombre": "Juan", "apellido": "Perez"},
            {"id": 2, "nombre": "Ana", "apellido": "Gomez"},
        ]

    def obtener_por_id(self, docente_id):
        if docente_id == 1:
            return {
                "id": 1,
                "nombre": "Juan",
                "apellido": "Perez"
            }

        return None


def test_listar_docentes():

    repo_mock = MockDocenteRepository()
    service = DocenteService(repo_mock)

    resultado = service.listar_docentes()

    assert len(resultado) == 2
    assert resultado[0]["nombre"] == "Juan"


def test_obtener_docente_existente():

    repo_mock = MockDocenteRepository()
    service = DocenteService(repo_mock)

    resultado = service.obtener_docente(1)

    assert resultado is not None
    assert resultado["apellido"] == "Perez"


def test_obtener_docente_inexistente():

    repo_mock = MockDocenteRepository()
    service = DocenteService(repo_mock)

    try:
        service.obtener_docente(99)
        assert False
    except Exception:
        assert True