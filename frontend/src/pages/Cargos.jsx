import { useEffect, useState } from "react";
import api from "../api/axios";

import FormularioCargo from "../components/FormularioCargo";
import TablaCargos from "../components/TablaCargos";
import ModalEliminar from "../components/ModalEliminar";

function Cargos() {
  const [mostrarInactivos, setMostrarInactivos] = useState(false);
  const [cargos, setCargos] = useState([]);
  const [mostrarFormulario, setMostrarFormulario] = useState(false);

  const [cargoEditandoId, setCargoEditandoId] = useState(null);
  const [nombre, setNombre] = useState("");
  const [activo, setActivo] = useState(true);

  const [mostrarModalEliminar, setMostrarModalEliminar] = useState(false);
  const [cargoEliminarId, setCargoEliminarId] = useState(null);

    useEffect(() => {
    cargarCargos();
    }, [mostrarInactivos]);

    const cargarCargos = async () => {
    try {
        const url = mostrarInactivos ? "/cargos/inactivos" : "/cargos/";
        const respuesta = await api.get(url);
        setCargos(respuesta.data);
    } catch (error) {
        console.error(error);
    }
    };
  const limpiarFormulario = () => {
    setCargoEditandoId(null);
    setNombre("");
    setActivo(true);
    setMostrarFormulario(false);
  };

  const nuevoCargo = () => {
    setCargoEditandoId(null);
    setNombre("");
    setActivo(true);
    setMostrarFormulario(true);
  };

  const editarCargo = (cargo) => {
    setCargoEditandoId(cargo.id);
    setNombre(cargo.nombre);
    setActivo(cargo.activo);
    setMostrarFormulario(true);
  };

  const guardarCargo = async () => {
    try {
      const datosCargo = {
        nombre: nombre,
        activo: activo,
      };

      if (cargoEditandoId === null) {
        await api.post("/cargos/", datosCargo);
      } else {
        await api.put(`/cargos/${cargoEditandoId}`, datosCargo);
      }

      await cargarCargos();
      limpiarFormulario();
    } catch (error) {
      console.error(error);
    }
  };

  const abrirModalEliminar = (id) => {
    setCargoEliminarId(id);
    setMostrarModalEliminar(true);
  };
  const activarCargo = async (cargo) => {
  try {
    const datosCargo = {
      nombre: cargo.nombre,
      activo: true,
    };

    await api.put(`/cargos/${cargo.id}`, datosCargo);

    await cargarCargos();
  } catch (error) {
    console.error(error);
  }
};


  const confirmarEliminar = async () => {
    try {
      await api.delete(`/cargos/${cargoEliminarId}`);

      await cargarCargos();

      setMostrarModalEliminar(false);
      setCargoEliminarId(null);
    } catch (error) {
      console.error(error);
    }
  };

  return (
     <div className="card">
      <h1>Listado de cargos</h1>
   <div className="barra-acciones">
      
        <button
           className={!mostrarInactivos ? "btn-inactivos" : "btn-activos"}
           onClick={() => setMostrarInactivos(!mostrarInactivos)}
            style={{ width: "150px" }}
        >
            {mostrarInactivos ? "Ver activos" : "Ver inactivos"}
        </button>

        <button className="btn-nuevo"
            onClick={nuevoCargo}
            style={{ width: "110px" }}
        >
            Nuevo Cargo
        </button>
        </div>

      <FormularioCargo
        visible={mostrarFormulario}
        cargoEditandoId={cargoEditandoId}
        nombre={nombre}
        activo={activo}
        setNombre={setNombre}
        setActivo={setActivo}
        onGuardar={guardarCargo}
        onCancelar={limpiarFormulario}
      />

      <br />
      <br />
        
      <TablaCargos
        cargos={cargos}
        mostrarInactivos={mostrarInactivos}
        onEditar={editarCargo}
        onEliminar={abrirModalEliminar}
        onActivar={activarCargo}
     />

      <ModalEliminar
        visible={mostrarModalEliminar}
        mensaje="¿Desea eliminar este cargo?"
        onConfirmar={confirmarEliminar}
        onCancelar={() => setMostrarModalEliminar(false)}
      />
    </div>
  );
}

export default Cargos;