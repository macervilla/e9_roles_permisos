import { Link, Outlet } from "react-router-dom";
import {
  obtenerNombre,
  nombreRol,
  esAdmin,
  esOperador,
} from "../utils/permisos";

function Layout() {
  const cerrarSesion = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("rol_id");
  localStorage.removeItem("nombre");

  const esProduccion = window.location.hostname === "acersistemas.site";

  window.location.href = esProduccion ? "/e9/login" : "/login";
};
  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>e7React</h2>

        <div style={{ marginBottom: "25px", color: "white" }}>
          <strong>{obtenerNombre()}</strong>
          <br />
          <small>{nombreRol()}</small>
        </div>

        <nav className="menu">
          <Link to="/dashboard">Dashboard</Link>

          {(esAdmin() || esOperador()) && (
            <Link to="/cargos">Cargos</Link>
          )}

          <Link to="/docentes">Docentes</Link>

          {esAdmin() && (
            <>
              <Link to="/usuarios">Usuarios</Link>
              <Link to="/roles">Roles</Link>
            </>
          )}

          <button
            onClick={cerrarSesion}
            style={{
              marginTop: "30px",
              background: "#dc3545",
              color: "white",
              border: "none",
              padding: "10px",
              borderRadius: "6px",
              cursor: "pointer",
            }}
          >
            Cerrar sesión
          </button>
        </nav>
      </aside>

      <main className="contenido">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;