function FormularioCargo({
  visible,
  cargoEditandoId,
  nombre,
  activo,
  setNombre,
  setActivo,
  onGuardar,
  onCancelar
}) {

  if (!visible) return null;

  return (
    <div>

      <h3>
        {cargoEditandoId === null
          ? "Nuevo Cargo"
          : "Editar Cargo"}
      </h3>

      <label>Nombre:</label>

      <input
        type="text"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />

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

      <button className="btn-guardar" onClick={onGuardar}>
        Guardar
      </button>

      {" "}

      <button className="btn-cancelar" onClick={onCancelar}>
        Cancelar
      </button>

    </div>
  );
}

export default FormularioCargo;