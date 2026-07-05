import { useEffect, useState } from "react";
import api from "../api/axios";

import FormularioDocente from "../components/FormularioDocente";
import TablaDocentes from "../components/TablaDocentes";

function Docentes() {
  const [mostrarInactivos, setMostrarInactivos] = useState(false);
  
  const [docentes, setDocentes] = useState([]);
  const [cargos, setCargos] = useState([]);

  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [docenteEditandoId, setDocenteEditandoId] = useState(null);

  const [nombre, setNombre] = useState("");
  const [cargoId, setCargoId] = useState("");
  const [activo, setActivo] = useState(true);

  useEffect(() => {
    cargarDocentes();
    cargarCargos();
  }, [mostrarInactivos]);

  const cargarDocentes = async () => {
    try {
        const url = mostrarInactivos ? "/docentes/inactivos" : "/docentes/";
        const respuesta = await api.get(url);
        setDocentes(respuesta.data);
    } catch (error) {
        console.error(error);
    }
  };

  const cargarCargos = async () => {
    const respuesta = await api.get("/cargos/");
    setCargos(respuesta.data);
  };

  const nuevoDocente = () => {
    setDocenteEditandoId(null);
    setNombre("");
    setCargoId("");
    setActivo(true);
    setMostrarFormulario(true);
  };

  const editarDocente = (docente) => {
    setDocenteEditandoId(docente.id);
    setNombre(docente.nombre);
    setCargoId(docente.cargo_id || docente.cargoid || docente.id_cargo);
    setActivo(docente.activo);
    setMostrarFormulario(true);
  };

  const limpiarFormulario = () => {
    setDocenteEditandoId(null);
    setNombre("");
    setCargoId("");
    setActivo(true);
    setMostrarFormulario(false);
  };

  const guardarDocente = async () => {
    const datosDocente = {
      nombre: nombre,
      cargo_id: Number(cargoId),
      activo: activo,
    };

    if (docenteEditandoId === null) {
      await api.post("/docentes/", datosDocente);
    } else {
      await api.put(`/docentes/${docenteEditandoId}`, datosDocente);
    }

    await cargarDocentes();
    limpiarFormulario();
  };

  return (
         <div className="card">
      <h1>Listado de docentes</h1>
      <div className="barra-acciones">
       
        <button
          className={mostrarInactivos ? "btn-inactivos" : "btn-activos"}
            onClick={() => setMostrarInactivos(!mostrarInactivos)}
            style={{ width: "150px" }}
        >
            {mostrarInactivos ? "Ver activos" : "Ver inactivos"}
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
        setNombre={setNombre}
        setCargoId={setCargoId}
        setActivo={setActivo}
        onGuardar={guardarDocente}
        onCancelar={limpiarFormulario}
      />

      <br />
      <br />

      <TablaDocentes
        docentes={docentes}
        cargos={cargos}
        onEditar={editarDocente}
      />
    </div>
  );
}

export default Docentes;