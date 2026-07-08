import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

// ==============================
// Variables globales
// ==============================

let isRefreshing = false;
let refreshPromise = null;

// ==============================
// Request
// ==============================

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// ==============================
// Response
// ==============================

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    if (!error.response) {
      return Promise.reject(error);
    }

    if (
      error.response.status !== 401 ||
      originalRequest._retry ||
      originalRequest.url.includes("/auth/login") ||
      originalRequest.url.includes("/auth/refresh")
    ) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      // ==================================
      // Ya hay un refresh en ejecución
      // ==================================

      if (isRefreshing) {
        await refreshPromise;

        originalRequest.headers.Authorization =
          `Bearer ${localStorage.getItem("token")}`;

        return api(originalRequest);
      }

      // ==================================
      // Primer refresh
      // ==================================

      isRefreshing = true;

      refreshPromise = axios.post(
        `${api.defaults.baseURL}/auth/refresh`,
        {
          refresh_token: localStorage.getItem("refresh_token"),
        }
      );

      const response = await refreshPromise;

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      localStorage.setItem(
        "refresh_token",
        response.data.refresh_token
      );

      originalRequest.headers.Authorization =
        `Bearer ${response.data.access_token}`;

      return api(originalRequest);

    } catch (e) {

      localStorage.clear();

      const esProduccion =
        window.location.hostname === "acersistemas.site";

      window.location.href = esProduccion
        ? "/e9/login"
        : "/login";

      return Promise.reject(e);

    } finally {

      isRefreshing = false;
      refreshPromise = null;

    }
  }
);

export default api;