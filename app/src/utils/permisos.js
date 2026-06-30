export function obtenerRolId() {
  return Number(localStorage.getItem("rol_id"));
}

export function obtenerNombre() {
  return localStorage.getItem("nombre") || "Usuario";
}

export function nombreRol() {
  const rolId = obtenerRolId();

  if (rolId === 1) return "Administrador";
  if (rolId === 2) return "Consulta";
  if (rolId === 3) return "Operador";

  return "Sin rol";
}

export function esAdmin() {
  return obtenerRolId() === 1;
}

export function esOperador() {
  return obtenerRolId() === 3;
}

export function puedeCrearEditar() {
  return esAdmin() || esOperador();
}

export function puedeEliminar() {
  return esAdmin();
}