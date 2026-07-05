function FormularioDocente({
  visible,
  docenteEditandoId,
  nombre,
  cargoId,
  activo,
  cargos,
  setNombre,
  setCargoId,
  setActivo,
  onGuardar,
  onCancelar,
}) {
  if (!visible) return null;

  return (
    <div>
      <h3>{docenteEditandoId === null ? "Nuevo Docente" : "Editar Docente"}</h3>

      <label>Nombre:</label>
      <input
        type="text"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />

      <br />
      <br />

      <label>Cargo:</label>
      <select value={cargoId} onChange={(e) => setCargoId(e.target.value)}>
        <option value="">Seleccione cargo</option>

        {cargos.map((cargo) => (
          <option key={cargo.id} value={cargo.id}>
            {cargo.nombre}
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

export default FormularioDocente;