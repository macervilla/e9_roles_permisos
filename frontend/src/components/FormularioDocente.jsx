import { useMemo, useState } from "react";

function FormularioDocente({
  visible,
  docenteEditandoId,
  nombre,
  cargoId,
  activo,
  cargos,
  provincias,
  localidades,
  provinciaId,
  localidadId,
  setNombre,
  setCargoId,
  setActivo,
  setProvinciaId,
  setLocalidadId,
  cargarLocalidades,
  onGuardar,
  onCancelar,
}) {
  const [busquedaLocalidad, setBusquedaLocalidad] = useState("");

  const localidadesFiltradas = useMemo(() => {
    const texto = busquedaLocalidad
      .trim()
      .toLocaleLowerCase("es");

    const resultado = texto
      ? localidades.filter((localidad) =>
          localidad.nombre
            .toLocaleLowerCase("es")
            .includes(texto)
        )
      : localidades;

    return [...resultado].sort((a, b) =>
      a.nombre.localeCompare(b.nombre, "es", {
        sensitivity: "base",
      })
    );
  }, [localidades, busquedaLocalidad]);

  if (!visible) {
    return null;
  }

  const cambiarProvincia = async (evento) => {
    const nuevaProvinciaId = evento.target.value;

    const provinciaSeleccionada = provincias.find(
      (provincia) =>
        String(provincia.id) === String(nuevaProvinciaId)
    );

    setProvinciaId(nuevaProvinciaId);
    setLocalidadId("");
    setBusquedaLocalidad("");

    if (provinciaSeleccionada) {
      await cargarLocalidades(
        provinciaSeleccionada.nombre
      );
    }
  };

  const cancelarFormulario = () => {
    setBusquedaLocalidad("");
    onCancelar();
  };

  return (
    <div>
      <h3>
        {docenteEditandoId === null
          ? "Nuevo Docente"
          : "Editar Docente"}
      </h3>

      <label>Nombre:</label>

      <input
        type="text"
        value={nombre}
        onChange={(evento) =>
          setNombre(evento.target.value)
        }
      />

      <br />
      <br />

      <label>Cargo:</label>

      <select
        value={cargoId}
        onChange={(evento) =>
          setCargoId(evento.target.value)
        }
      >
        <option value="">Seleccione cargo</option>

        {cargos.map((cargo) => (
          <option
            key={cargo.id}
            value={cargo.id}
          >
            {cargo.nombre}
          </option>
        ))}
      </select>

      <br />
      <br />

      <label>Provincia:</label>

      <select
        value={provinciaId}
        onChange={cambiarProvincia}
      >
        <option value="">
          Seleccione provincia
        </option>

        {provincias.map((provincia) => (
          <option
            key={provincia.id}
            value={provincia.id}
          >
            {provincia.nombre}
          </option>
        ))}
      </select>

      <br />
      <br />

      <label>Buscar localidad:</label>

      <input
        type="text"
        value={busquedaLocalidad}
        placeholder="Escriba parte del nombre"
        disabled={!provinciaId}
        onChange={(evento) =>
          setBusquedaLocalidad(evento.target.value)
        }
      />

      <br />
      <br />

      <label>Localidad:</label>

      <select
        value={localidadId}
        disabled={!provinciaId}
        onChange={(evento) =>
          setLocalidadId(evento.target.value)
        }
      >
        <option value="">
          Seleccione localidad
        </option>

        {localidadesFiltradas.map((localidad) => (
          <option
            key={localidad.id}
            value={localidad.id}
          >
            {localidad.nombre}
          </option>
        ))}
      </select>

      {provinciaId && busquedaLocalidad && (
        <p>
          Coincidencias encontradas:{" "}
          {localidadesFiltradas.length}
        </p>
      )}

      <br />

      <label>
        <input
          type="checkbox"
          checked={activo}
          onChange={(evento) =>
            setActivo(evento.target.checked)
          }
        />
        Activo
      </label>

      <br />
      <br />

      <button
        className="btn-guardar"
        onClick={onGuardar}
      >
        Guardar
      </button>

      {" "}

      <button
        className="btn-cancelar"
        onClick={cancelarFormulario}
      >
        Cancelar
      </button>
    </div>
  );
}

export default FormularioDocente;