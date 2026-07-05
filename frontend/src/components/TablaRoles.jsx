function TablaRoles({
  roles,
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
        {roles.map((rol) => (
          <tr key={rol.id}>
            <td>{rol.id}</td>
            <td>{rol.nombre}</td>
            <td>{rol.activo ? "Sí" : "No"}</td>
            <td>
              <button className="btn-nuevo" onClick={() => onEditar(rol)}>Editar</button>

              {" "}

              {mostrarInactivos ? (
                <button className="btn-activar" onClick={() => onActivar(rol)}>
                  Activar
                </button>
              ) : (
                <button className="btn-eliminar" onClick={() => onEliminar(rol.id)}>
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

export default TablaRoles;