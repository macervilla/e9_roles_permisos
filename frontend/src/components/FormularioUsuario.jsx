function FormularioUsuario({
  visible,
  usuarioEditandoId,
  nombre,
  usuario,clave,
  rolId,
  roles,
  activo,
  setNombre,setUsuario,setClave,
  setRolId,
  setActivo,
  onGuardar,
  onCancelar,
}) {
  if (!visible) return null;

  return (
    <div>
      <h3>{usuarioEditandoId === null ? "Nuevo Usuario" : "Editar Usuario"}</h3>

      <label>Nombre:</label>
      <input
        type="text"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />
      <label>Usuario:</label>
      <input
        type="text"
        value={usuario}
        onChange={(e) => setUsuario(e.target.value)}
      />
      <br />
      <br />

      <label>Rol:</label>
      <select value={rolId} onChange={(e) => setRolId(e.target.value)}>
        <option value="">Seleccione rol</option>

        {roles.map((rol) => (
          <option key={rol.id} value={rol.id}>
            {rol.nombre}
          </option>
        ))}
      </select>

      <br />
      <br />

      <label>
        <input
          type="checkbox"
          checked={activo}
          onChange={(e) => setActivo(e.target.checked)}
        />
        Activo
      </label>

      <br />
      <br />

      <button className="btn-guardar" onClick={onGuardar}>Guardar</button>
      {" "}
      <button className="btn-cancelar" onClick={onCancelar}>Cancelar</button>
    </div>
  );
}

export default FormularioUsuario;