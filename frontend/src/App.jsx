import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import Layout from "./components/Layout";
import Cargos from "./pages/Cargos";
import Docentes from "./pages/Docentes";
import Usuarios from "./pages/Usuarios";
import Roles from "./pages/Roles";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import RutaProtegida from "./components/RutaProtegida.jsx";

function App() {
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL.replace(/\/$/, "")}>
<Routes>
  <Route path="/login" element={<Login />} />

  <Route
    element={
      <RutaProtegida>
        <Layout />
      </RutaProtegida>
    }
  >
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/" element={<Navigate to="/dashboard" />} />
    <Route path="/cargos" element={<Cargos />} />
    <Route path="/docentes" element={<Docentes />} />
    <Route path="/usuarios" element={<Usuarios />} />
    <Route path="/roles" element={<Roles />} />
  </Route>
</Routes>
    </BrowserRouter>
  );
}

export default App;