function TablaDocentes({ docentes, cargos, onEditar }) {
  const obtenerNombreCargo = (docente) => {
    const cargoId = docente.cargo_id || docente.cargoid || docente.id_cargo;
    const cargo = cargos.find((c) => c.id === cargoId);
    return cargo ? cargo.nombre : cargoId;
  };

  return (
    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Cargo</th>
          <th>Activo</th>
          <th>Acciones</th>
        </tr>
      </thead>

      <tbody>
        {docentes.map((docente) => (
          <tr key={docente.id}>
            <td>{docente.id}</td>
            <td>{docente.nombre}</td>
            <td>{obtenerNombreCargo(docente)}</td>
            <td>{docente.activo ? "Sí" : "No"}</td>
            <td>
              <button className="btn-editar" onClick={() => onEditar(docente)}>Editar</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TablaDocentes;