# e9 - Roles y Permisos

![CI](https://github.com/macervilla/e9_roles_permisos/actions/workflows/ci.yml/badge.svg)
![Coverage](https://codecov.io/gh/macervilla/e9_roles_permisos/branch/main/graph/badge.svg)
# e9 - Roles y Permisos

[![CI - FastAPI Tests](https://github.com/macervilla/e9_roles_permisos/actions/workflows/ci.yml/badge.svg)](https://github.com/macervilla/e9_roles_permisos/actions/workflows/ci.yml)

[![codecov](https://codecov.io/gh/macervilla/e9_roles_permisos/branch/main/graph/badge.svg)](https://app.codecov.io/gh/macervilla/e9_roles_permisos)
Proyecto Full Stack desarrollado como práctica de arquitectura moderna con **FastAPI + React**, incorporando autenticación JWT, control de acceso basado en roles, cache con Redis, observabilidad, Docker, CI/CD y testing automatizado.

---

# Tecnologías

- FastAPI
- React + Vite
- SQLAlchemy
- MySQL
- Redis
- JWT + Refresh Token Rotation
- Alembic
- Docker & Docker Compose
- GitHub Actions
- Pytest
- Codecov

---

# Funcionalidades

- Login con JWT
- Refresh Token con rotación
- Roles y permisos
- CRUD de Usuarios
- CRUD de Docentes
- CRUD de Cargos
- Cache con Redis
- Logging estructurado
- Correlation ID
- Health Checks
- Métricas Prometheus
- Docker Compose
- CI/CD con GitHub Actions
- Cobertura de código con Codecov
- Tests Unitarios
- Tests de API
- Tests End-to-End

---

# Estructura

```
.
├── app/
├── frontend/
├── tests/
├── alembic/
├── docker/
├── .github/
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Instalación

```bash
git clone https://github.com/macervilla/e9_roles_permisos.git

cd e9_roles_permisos
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Levantar el proyecto

```bash
docker compose up --build
```

Backend

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

Frontend

```
http://localhost:5173
```

---

# Testing

Ejecutar todos los tests

```bash
pytest
```

Cobertura

```bash
pytest --cov=app --cov-report=html
```

---

# Calidad del código

Este proyecto utiliza:

- Ruff
- Black
- isort
- pre-commit
- GitHub Actions
- Codecov

---

# Roadmap implementado

- ✅ FastAPI
- ✅ SQLAlchemy
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
- ✅ Alembic
- ✅ GitHub Actions
- ✅ Codecov
- ✅ Pytest
- ✅ E2E Testing

---

# Autor

Alejandro Cervilla