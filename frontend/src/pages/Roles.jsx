import { useEffect, useState } from "react";
import api from "../api/axios";

import FormularioRol from "../components/FormularioRol";
import TablaRoles from "../components/TablaRoles";
import ModalEliminar from "../components/ModalEliminar";

function Roles() {
  const [roles, setRoles] = useState([]);
  const [mostrarInactivos, setMostrarInactivos] = useState(false);

  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [rolEditandoId, setRolEditandoId] = useState(null);
  const [nombre, setNombre] = useState("");
  const [activo, setActivo] = useState(true);

  const [mostrarModalEliminar, setMostrarModalEliminar] = useState(false);
  const [rolEliminarId, setRolEliminarId] = useState(null);

  useEffect(() => {
    cargarRoles();
  }, [mostrarInactivos]);

  const cargarRoles = async () => {
    try {
      const url = mostrarInactivos ? "/roles/inactivos" : "/roles/";
      const respuesta = await api.get(url);
      setRoles(respuesta.data);
    } catch (error) {
      console.error(error);
    }
  };

  const nuevoRol = () => {
    setRolEditandoId(null);
    setNombre("");
    setActivo(true);
    setMostrarFormulario(true);
  };

  const editarRol = (rol) => {
    setRolEditandoId(rol.id);
    setNombre(rol.nombre);
    setActivo(rol.activo);
    setMostrarFormulario(true);
  };

  const limpiarFormulario = () => {
    setRolEditandoId(null);
    setNombre("");
    setActivo(true);
    setMostrarFormulario(false);
  };

  const guardarRol = async () => {
    try {
      const datosRol = {
        nombre: nombre,
        activo: activo,
      };

      if (rolEditandoId === null) {
        await api.post("/roles/", datosRol);
      } else {
        await api.put(`/roles/${rolEditandoId}`, datosRol);
      }

      await cargarRoles();
      limpiarFormulario();
    } catch (error) {
      console.error(error);
    }
  };

  const abrirModalEliminar = (id) => {
    setRolEliminarId(id);
    setMostrarModalEliminar(true);
  };
const activarRol = async (rol) => {
  try {
    const datosRol = {
      nombre: rol.nombre,
      activo: true,
    };

    await api.put(`/roles/${rol.id}`, datosRol);

    await cargarRoles();
  } catch (error) {
    console.error(error);
  }
};
  const confirmarEliminar = async () => {
    try {
      await api.delete(`/roles/${rolEliminarId}`);

      await cargarRoles();

      setMostrarModalEliminar(false);
      setRolEliminarId(null);
    } catch (error) {
      console.error(error);
    }
  };

  return (
     <div className="card">
      <h1>Listado de roles</h1>

       <div className="barra-acciones">

        <button
         className={mostrarInactivos ? "btn-inactivos" : "btn-activos"}
         
            onClick={() => setMostrarInactivos(!mostrarInactivos)}
            style={{ width: "150px" }}
        >
            {mostrarInactivos ? "Ver activos" : "Ver inactivos"}
        </button>

        <button
            onClick={nuevoRol}
           className="btn-nuevo"
        >
            Nuevo Rol
        </button>
        </div>

      <FormularioRol
        visible={mostrarFormulario}
        rolEditandoId={rolEditandoId}
        nombre={nombre}
        activo={activo}
        setNombre={setNombre}
        setActivo={setActivo}
        onGuardar={guardarRol}
        onCancelar={limpiarFormulario}
      />

      <br />
      <br />

      <TablaRoles  
        roles={roles}
        mostrarInactivos={mostrarInactivos}
        onEditar={editarRol}
        onEliminar={abrirModalEliminar}
        onActivar={activarRol}
      />

      <ModalEliminar
        visible={mostrarModalEliminar}
        mensaje="¿Desea eliminar este rol?"
        onConfirmar={confirmarEliminar}
        onCancelar={() => setMostrarModalEliminar(false)}
      />
    </div>
  );
}

export default Roles;