function ModalEliminar({
  visible,
  mensaje,
  onConfirmar,
  onCancelar
}) {
  if (!visible) return null;

  return (
    <div className="modal-fondo">
      <div className="modal-contenido">
        <h2>Confirmar acción</h2>

        <p>{mensaje}</p>

        <div className="modal-botones">
          <button
            className="btn-cancelar"
            onClick={onCancelar}
          >
            Cancelar
          </button>

          <button
            className="btn-eliminar"
            onClick={onConfirmar}
          >
            Confirmar
          </button>
        </div>
      </div>
    </div>
  );
}

export default ModalEliminar;