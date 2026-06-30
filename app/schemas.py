from pydantic import BaseModel


# ---------- Activo ----------

class ActivoUpdate(BaseModel):
    activo: bool


# ---------- Roles ----------

class RolCreate(BaseModel):
    nombre: str


class RolUpdate(BaseModel):
    nombre: str
    activo: bool


class RolResponse(BaseModel):
    id: int
    nombre: str
    activo: bool

    class Config:
        from_attributes = True


# ---------- Cargos ----------

class CargoCreate(BaseModel):
    nombre: str
    activo: bool = True


class CargoUpdate(BaseModel):
    nombre: str
    activo: bool = True


class CargoResponse(BaseModel):
    id: int
    nombre: str
    activo: bool

    class Config:
        from_attributes = True


# ---------- Docentes ----------

class DocenteCreate(BaseModel):
    nombre: str
    cargo_id: int
    activo: bool = True


class DocenteResponse(BaseModel):
    id: int
    nombre: str
    cargo_id: int
    activo: bool

    class Config:
        from_attributes = True


# ---------- Usuarios ----------

class UsuarioCreate(BaseModel):
    usuario: str
    clave: str
    nombre: str
    rol_id: int
class UsuarioUpdate(BaseModel):
    usuario: str
    nombre: str
    rol_id: int
    activo: bool = True


class UsuarioClaveUpdate(BaseModel):
    clave: str

class UsuarioResponse(BaseModel):
    id: int
    usuario: str
    nombre: str
    rol_id: int
    activo: bool

    class Config:
        from_attributes = True


class UsuarioRolUpdate(BaseModel):
    rol_id: int


# ---------- JWT ----------
class Token(BaseModel):
    access_token: str
    token_type: str
    rol_id: int
    nombre: str


class CambiarClave(BaseModel):
    nueva_clave: str
