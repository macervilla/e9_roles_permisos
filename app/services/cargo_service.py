class CargoService:
    def __init__(self, repository):
        self.repository = repository

    def listar_cargos(self):
        return self.repository.listar()

    def listar_cargos_inactivos(self):
        return self.repository.listar_cargos_inactivos()

    def obtener_cargo(self, cargo_id: int):
        cargo = self.repository.obtener_por_id(cargo_id)

        if not cargo:
            raise ValueError("Cargo no encontrado")

        return cargo

    def crear_cargo(self, datos):
        return self.repository.crear(datos)

    def actualizar_cargo(self, cargo_id: int, datos):
        cargo = self.repository.actualizar(cargo_id, datos)

        if not cargo:
            raise ValueError("Cargo no encontrado")

        return cargo

    def eliminar_cargo(self, cargo_id: int):
        cargo = self.repository.eliminar(cargo_id)

        if not cargo:
            raise ValueError("Cargo no encontrado")

        return cargo
