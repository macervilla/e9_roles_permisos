import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Login() {
  const [usuario, setUsuario] = useState("");
  const [clave, setClave] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const ingresar = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const formData = new URLSearchParams();
      formData.append("username", usuario);
      formData.append("password", clave);

      const response = await api.post("/auth/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("refresh_token", response.data.refresh_token);
      localStorage.setItem("rol_id", response.data.rol_id);
      localStorage.setItem("nombre", response.data.nombre);
      
    
      navigate("/dashboard");
    } catch (error) {
      console.error(error);
      setError("Usuario o clave incorrectos");
    }
  };

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={ingresar}>
        <h2>Iniciar sesión</h2>

        <input
          type="text"
          placeholder="Usuario"
          value={usuario}
          onChange={(e) => setUsuario(e.target.value)}
        />

        <input
          type="password"
          placeholder="Clave"
          value={clave}
          onChange={(e) => setClave(e.target.value)}
        />

        {error && <p className="login-error">{error}</p>}

        <button type="submit">Ingresar</button>
      </form>
    </div>
  );
}

export default Login;