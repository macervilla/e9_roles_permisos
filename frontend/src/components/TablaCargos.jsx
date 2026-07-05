function TablaCargos({
  cargos,
  mostrarInactivos,
  onEditar,
  onEliminar,
  onActivar,
}) {
  return (
    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Activo</th>
          <th>Acciones</th>
        </tr>
      </thead>

      <tbody>
        {cargos.map((cargo) => (
          <tr key={cargo.id}>
            <td>{cargo.id}</td>
            <td>{cargo.nombre}</td>
            <td>{cargo.activo ? "Sí" : "No"}</td>
            <td>
              <button className="btn-editar" onClick={() => onEditar(cargo)}>Editar</button>

              {" "}

              {mostrarInactivos ? (
                <button  className="btn-activar" onClick={() => onActivar(cargo)}>
                  Activar
                </button>
              ) : (
                <button className="btn-eliminar" onClick={() => onEliminar(cargo.id)}>
                  Eliminar
                </button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TablaCargos;