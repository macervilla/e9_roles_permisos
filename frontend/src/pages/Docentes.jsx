import { useEffect, useState } from "react";
import api from "../api/axios";

import FormularioDocente from "../components/FormularioDocente";
import TablaDocentes from "../components/TablaDocentes";

function Docentes() {
  const [mostrarInactivos, setMostrarInactivos] = useState(false);

  const [docentes, setDocentes] = useState([]);
  const [cargos, setCargos] = useState([]);
  const [provincias, setProvincias] = useState([]);
  const [localidades, setLocalidades] = useState([]);

  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [docenteEditandoId, setDocenteEditandoId] = useState(null);

  const [nombre, setNombre] = useState("");
  const [cargoId, setCargoId] = useState("");
  const [activo, setActivo] = useState(true);
  const [provinciaId, setProvinciaId] = useState("");
  const [localidadId, setLocalidadId] = useState("");

  useEffect(() => {
    cargarDocentes();
    cargarCargos();
    cargarProvincias();
  }, [mostrarInactivos]);

  const cargarDocentes = async () => {
    try {
      const url = mostrarInactivos
        ? "/docentes/inactivos"
        : "/docentes/";

      const respuesta = await api.get(url);
      setDocentes(respuesta.data);
    } catch (error) {
      console.error("Error cargando docentes:", error);
    }
  };

  const cargarCargos = async () => {
    try {
      const respuesta = await api.get("/cargos/");
      setCargos(respuesta.data);
    } catch (error) {
      console.error("Error cargando cargos:", error);
    }
  };

  const ordenarPorNombre = (elementos) => {
  return [...elementos].sort((a, b) =>
    a.nombre.localeCompare(b.nombre, "es", {
      sensitivity: "base",
    })
  );
};

const cargarProvincias = async () => {
  try {
    const respuesta = await api.get("/geografia/provincias");

    setProvincias(
      ordenarPorNombre(respuesta.data)
    );
  } catch (error) {
    console.error("Error cargando provincias:", error);
    setProvincias([]);
  }
};

const cargarLocalidades = async (nombreProvincia) => {
  if (!nombreProvincia) {
    setLocalidades([]);
    return;
  }

  try {
    const respuesta = await api.get("/geografia/localidades", {
      params: {
        provincia: nombreProvincia,
      },
    });

    setLocalidades(
      ordenarPorNombre(respuesta.data)
    );
  } catch (error) {
    console.error("Error cargando localidades:", error);
    setLocalidades([]);
  }
};
  const nuevoDocente = () => {
    setDocenteEditandoId(null);
    setNombre("");
    setCargoId("");
    setActivo(true);
    setProvinciaId("");
    setLocalidadId("");
    setLocalidades([]);
    setMostrarFormulario(true);
  };

  const editarDocente = async (docente) => {
    const provinciaSeleccionada =
      docente.provincia_id_georef || "";

    setDocenteEditandoId(docente.id);
    setNombre(docente.nombre);
    setCargoId(
      docente.cargo_id ||
      docente.cargoid ||
      docente.id_cargo ||
      ""
    );
    setActivo(docente.activo);
    setProvinciaId(provinciaSeleccionada);
    setLocalidadId(docente.localidad_id_georef || "");
    setLocalidades([]);
    setMostrarFormulario(true);

    if (provinciaSeleccionada) {
      const provincia = provincias.find(
        (item) => String(item.id) === String(provinciaSeleccionada)
      );

      if (provincia) {
        await cargarLocalidades(provincia.nombre);
      }
    }
  };

  const limpiarFormulario = () => {
    setDocenteEditandoId(null);
    setNombre("");
    setCargoId("");
    setActivo(true);
    setProvinciaId("");
    setLocalidadId("");
    setLocalidades([]);
    setMostrarFormulario(false);
  };

  const guardarDocente = async () => {
    if (!nombre.trim()) {
      alert("Debe ingresar el nombre del docente.");
      return;
    }

    if (!cargoId) {
      alert("Debe seleccionar un cargo.");
      return;
    }

    const datosDocente = {
      nombre: nombre.trim(),
      cargo_id: Number(cargoId),
      activo,
      provincia_id_georef: provinciaId || null,
      localidad_id_georef: localidadId || null,
    };

    try {
      if (docenteEditandoId === null) {
        await api.post("/docentes/", datosDocente);
      } else {
        await api.put(
          `/docentes/${docenteEditandoId}`,
          datosDocente
        );
      }

      await cargarDocentes();
      limpiarFormulario();
    } catch (error) {
      console.error("Error guardando docente:", error);

      const mensaje =
        error.response?.data?.detail ||
        "No se pudo guardar el docente.";

      alert(mensaje);
    }
  };

  return (
    <div className="card">
      <h1>Listado de docentes</h1>

      <div className="barra-acciones">
        <button
          className={
            mostrarInactivos
              ? "btn-inactivos"
              : "btn-activos"
          }
          onClick={() =>
            setMostrarInactivos(!mostrarInactivos)
          }
          style={{ width: "150px" }}
        >
          {mostrarInactivos
            ? "Ver activos"
            : "Ver inactivos"}
        </button>

        <button
          className="btn-nuevo"
          onClick={nuevoDocente}
        >
          Nuevo Docente
        </button>
      </div>

      <FormularioDocente
        visible={mostrarFormulario}
        docenteEditandoId={docenteEditandoId}
        nombre={nombre}
        cargoId={cargoId}
        activo={activo}
        cargos={cargos}
        provincias={provincias}
        localidades={localidades}
        provinciaId={provinciaId}
        localidadId={localidadId}
        setNombre={setNombre}
        setCargoId={setCargoId}
        setActivo={setActivo}
        setProvinciaId={setProvinciaId}
        setLocalidadId={setLocalidadId}
        cargarLocalidades={cargarLocalidades}
        onGuardar={guardarDocente}
        onCancelar={limpiarFormulario}
      />

      <br />
      <br />

      <TablaDocentes
        docentes={docentes}
        cargos={cargos}
        localidades={localidades}
        provincias={provincias}
        mostrarInactivos={mostrarInactivos}
        onEditar={editarDocente}
      />
    </div>
  );
}

export default Docentes;