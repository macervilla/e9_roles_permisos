function TablaUsuarios({ usuarios, roles, onEditar, onBlanquearClave }) {
  const obtenerNombreRol = (usuario) => {
    const rolId = usuario.rol_id || usuario.rolid || usuario.id_rol;
    const rol = roles.find((r) => r.id === rolId);

    return rol ? rol.nombre : rolId;
  };

  return (
    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Usuario</th>
          <th>Rol</th>
          <th>Activo</th>
          <th>Acciones</th>
        </tr>
      </thead>

      <tbody>
        {usuarios.map((usuario) => (
          <tr key={usuario.id}>
            <td>{usuario.id}</td>
            <td>{usuario.nombre}</td>
            <td>{usuario.usuario}</td>
            <td>{obtenerNombreRol(usuario)}</td>
            <td>{usuario.activo ? "Sí" : "No"}</td>
            <td>
              <button
                className="btn-editar"
                onClick={() => onEditar(usuario)}
              >
                Editar
              </button>

              <button
                className="btn-blanquear"
                onClick={() => onBlanquearClave(usuario)}
              >
                Blanquear clave
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TablaUsuarios;