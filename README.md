# e9 - Roles y Permisos

[![CI - FastAPI Tests](https://github.com/macervilla/e9_roles_permisos/actions/workflows/ci.yml/badge.svg)](https://github.com/macervilla/e9_roles_permisos/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/macervilla/e9_roles_permisos/branch/main/graph/badge.svg)](https://app.codecov.io/gh/macervilla/e9_roles_permisos)

Proyecto Full Stack desarrollado como práctica de arquitectura moderna utilizando **FastAPI + React**, incorporando autenticación JWT, control de acceso basado en roles, cache con Redis, observabilidad, Docker, CI/CD y testing automatizado.

---

# 📊 Calidad del proyecto

| Recurso | Acceso |
|---------|---------|
| 🚀 CI/CD | [Ver GitHub Actions](https://github.com/macervilla/e9_roles_permisos/actions/workflows/ci.yml) |
| 📈 Cobertura | [Ver reporte en Codecov](https://app.codecov.io/gh/macervilla/e9_roles_permisos) |
| 📄 Swagger | `http://localhost:8000/docs` *(cuando el backend está en ejecución)* |

---

# 🚀 Tecnologías

### Backend

- FastAPI
- SQLAlchemy
- Alembic
- MySQL
- Redis
- JWT Authentication
- Refresh Token Rotation
- Repository Pattern
- Dependency Injection

### Frontend

- React
- Vite
- Axios

### DevOps

- Docker
- Docker Compose
- GitHub Actions
- Codecov

### Testing y Calidad

- Pytest
- Coverage
- Ruff
- Black
- isort
- pre-commit

---

# ✨ Funcionalidades

- ✅ Login con JWT
- ✅ Refresh Token con rotación
- ✅ Roles y permisos
- ✅ CRUD de Usuarios
- ✅ CRUD de Docentes
- ✅ CRUD de Cargos
- ✅ Cache con Redis
- ✅ Logging profesional
- ✅ Correlation ID
- ✅ Health Checks
- ✅ Métricas para Prometheus
- ✅ Docker Compose
- ✅ GitHub Actions
- ✅ Cobertura de código con Codecov
- ✅ Tests Unitarios
- ✅ Tests de API
- ✅ Tests End-to-End (E2E)

---

# 📁 Estructura del proyecto

```text
.
├── .github/
│   └── workflows/
├── alembic/
├── app/
│   ├── cache/
│   ├── middleware/
│   ├── repositories/
│   ├── routers/
│   ├── services/
│   └── ...
├── docker/
├── frontend/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Instalación

## Clonar el repositorio

```bash
git clone https://github.com/macervilla/e9_roles_permisos.git

cd e9_roles_permisos
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configurar variables de entorno

Crear el archivo `.env` utilizando como base el archivo `.env.example`.

---

# 🐳 Ejecutar con Docker

```bash
docker compose up --build
```

---

# ▶️ Ejecutar en desarrollo

## Backend

```bash
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# 🌐 Accesos

## Backend

```
http://localhost:8000
```

## Swagger

```
http://localhost:8000/docs
```

## Frontend

```
http://localhost:5173
```

---

# 🧪 Testing

Ejecutar todos los tests

```bash
pytest
```

Generar cobertura

```bash
pytest --cov=app --cov-report=html
```

Abrir reporte HTML

```
htmlcov/index.html
```

---

# 📈 Integración Continua

Cada **push** o **Pull Request** ejecuta automáticamente:

- Instalación de dependencias
- Levantamiento de MySQL
- Levantamiento de Redis
- Ejecución de Pytest
- Generación de cobertura
- Publicación del reporte en Codecov

---

# 🏗️ Arquitectura

El proyecto implementa:

- Repository Pattern
- Service Layer
- Dependency Injection
- JWT Authentication
- Refresh Token Rotation
- Redis Cache
- Logging Middleware
- Correlation ID
- Health Checks
- Observabilidad
- Docker
- CI/CD

---

# 🛣️ Roadmap implementado

- ✅ FastAPI
- ✅ React
- ✅ SQLAlchemy
- ✅ Alembic
- ✅ Repository Pattern
- ✅ Dependency Injection
- ✅ JWT
- ✅ Refresh Token Rotation
- ✅ Roles y Permisos
- ✅ Redis Cache
- ✅ Logging
- ✅ Correlation ID
- ✅ Health Checks
- ✅ Prometheus
- ✅ Docker
- ✅ Docker Compose
- ✅ GitHub Actions
- ✅ Codecov
- ✅ Pytest
- ✅ E2E Testing

---

# 👨‍💻 Autor

**Alejandro Cervilla**

Proyecto desarrollado como práctica para consolidar conocimientos de desarrollo Backend y Full Stack con FastAPI, React y buenas prácticas de ingeniería de software.