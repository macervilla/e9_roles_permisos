import { useEffect, useState } from "react";
import api from "../api/axios";

import FormularioUsuario from "../components/FormularioUsuario";
import TablaUsuarios from "../components/TablaUsuarios";

function Usuarios() {
  const [mostrarInactivos, setMostrarInactivos] = useState(false);
  const [usuarios, setUsuarios] = useState([]);
  const [roles, setRoles] = useState([]);

  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [usuarioEditandoId, setUsuarioEditandoId] = useState(null);

  const [nombre, setNombre] = useState("");
  const [usuario, setUsuario] = useState("");
  const [clave, setClave] = useState("");
  const [rolId, setRolId] = useState("");
  const [activo, setActivo] = useState(true);

  const [mostrarModal, setMostrarModal] = useState(false);
  const [usuarioSeleccionado, setUsuarioSeleccionado] = useState(null);

  useEffect(() => {
    cargarUsuarios();
    cargarRoles();
  }, [mostrarInactivos]);

  const cargarUsuarios = async () => {
    try {
      const url = mostrarInactivos ? "/usuarios/inactivos" : "/usuarios/";
      const respuesta = await api.get(url);
      setUsuarios(respuesta.data);
    } catch (error) {
      console.error(error);
    }
  };

  const cargarRoles = async () => {
    try {
      const respuesta = await api.get("/roles/");
      setRoles(respuesta.data);
    } catch (error) {
      console.error(error);
    }
  };

  const nuevoUsuario = () => {
    setUsuarioEditandoId(null);
    setNombre("");
    setUsuario("");
    setClave("");
    setRolId("");
    setActivo(true);
    setMostrarFormulario(true);
  };

  const editarUsuario = (usuarioSeleccionado) => {
    setUsuarioEditandoId(usuarioSeleccionado.id);
    setUsuario(usuarioSeleccionado.usuario);
    setNombre(usuarioSeleccionado.nombre);
    setClave("");
    setRolId(usuarioSeleccionado.rol_id);
    setActivo(usuarioSeleccionado.activo);
    setMostrarFormulario(true);
  };

  const limpiarFormulario = () => {
    setUsuarioEditandoId(null);
    setNombre("");
    setUsuario("");
    setClave("");
    setRolId("");
    setActivo(true);
    setMostrarFormulario(false);
  };

  const guardarUsuario = async () => {
    const datosUsuario = {
      nombre,
      usuario,
      rol_id: Number(rolId),
      activo,
    };

    if (usuarioEditandoId === null) {
      datosUsuario.clave = clave || usuario;
      await api.post("/usuarios/", datosUsuario);
    } else {
      await api.put(`/usuarios/${usuarioEditandoId}`, datosUsuario);
    }

    await cargarUsuarios();
    limpiarFormulario();
  };

  const abrirModalBlanqueo = (usuarioSeleccionado) => {
    setUsuarioSeleccionado(usuarioSeleccionado);
    setMostrarModal(true);
  };

  const cerrarModalBlanqueo = () => {
    setMostrarModal(false);
    setUsuarioSeleccionado(null);
  };

  const confirmarBlanqueo = async () => {
    await api.put(`/usuarios/${usuarioSeleccionado.id}/blanquear-clave`);

    cerrarModalBlanqueo();
    await cargarUsuarios();
  };

  return (
    <div className="card">
      <h1>Listado de usuarios</h1>

      <div className="barra-acciones">
        <button
          className={mostrarInactivos ? "btn-inactivos" : "btn-activos"}
          onClick={() => setMostrarInactivos(!mostrarInactivos)}
          style={{ width: "150px" }}
        >
          {mostrarInactivos ? "Ver activos" : "Ver inactivos"}
        </button>

        <button onClick={nuevoUsuario} className="btn-nuevo">
          Nuevo usuario
        </button>
      </div>

      <FormularioUsuario
        visible={mostrarFormulario}
        usuarioEditandoId={usuarioEditandoId}
        usuario={usuario}
        nombre={nombre}
        clave={clave}
        rolId={rolId}
        activo={activo}
        roles={roles}
        setNombre={setNombre}
        setUsuario={setUsuario}
        setClave={setClave}
        setRolId={setRolId}
        setActivo={setActivo}
        onGuardar={guardarUsuario}
        onCancelar={limpiarFormulario}
      />

      <br />
      <br />

      <TablaUsuarios
        usuarios={usuarios}
        roles={roles}
        onEditar={editarUsuario}
        onBlanquearClave={abrirModalBlanqueo}
      />

      {mostrarModal && usuarioSeleccionado && (
        <div className="modal-fondo">
          <div className="modal-contenido">
            <h2>Blanquear contraseña</h2>

            <p>
              ¿Desea blanquear la contraseña del usuario{" "}
              <strong>{usuarioSeleccionado.usuario}</strong>?
            </p>

            <p>
              La nueva contraseña será:{" "}
              <strong>{usuarioSeleccionado.usuario}</strong>
            </p>

            <div className="modal-botones">
              <button className="btn-cancelar" onClick={cerrarModalBlanqueo}>
                Cancelar
              </button>

              <button className="btn-blanquear" onClick={confirmarBlanqueo}>
                Blanquear
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Usuarios;