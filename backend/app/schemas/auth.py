from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator
import re

class Token(BaseModel):
    access_token: str
    token_type: str

class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):  #Herencia de RolBase, se crea un rol
    pass

class RolSchema(RolBase):  #Herencia de RolBase, devuelve un rol desde la BD
    id: int
    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):  #Herencia de BaseModel, se crea un usuario
    nombre: str
    apellido: str
    cedula: str
    celular: Optional[str] = None
    correo: EmailStr  #Validacion de que el correo sea valido
    estado: Optional[str] = "Activo"
    intentos_fallidos: Optional[int] = 0
    biografia: Optional[str] = None
    ultima_conexion: Optional[datetime] = None

    @field_validator("nombre", "apellido")  #Validacion de que el nombre y apellido solo contengan letras y espacios
    @classmethod  #Decorador que indica que el metodo es de clase
    def validate_names(cls, v):  #Metodo que valida el nombre y apellido
        if not v: return v  #Si el nombre o apellido es None, se devuelve
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", v):  #Si el nombre o apellido no contiene letras y espacios
            raise ValueError("El nombre/apellido solo puede contener letras y espacios")  #Se lanza un error
        return v  #Se devuelve el nombre o apellido

    @field_validator("cedula")  #Validacion de que la cedula solo contenga numeros
    @classmethod
    def validate_cedula(cls, v):
        if v is None: return v
        if not v.isdigit(): raise ValueError("La cédula debe contener solo números")
        if not (6 <= len(v) <= 10): raise ValueError("La cédula debe tener entre 6 y 10 dígitos")
        return v

    @field_validator("celular")
    @classmethod
    def validate_celular(cls, v):
        if v is None: return v
        if not re.match(r"^3[0-9]{9}$", v): raise ValueError("El celular debe empezar con 3 y tener exactamente 10 dígitos numéricos")
        return v

class UsuarioCreate(UsuarioBase):  #La herencia que encapsula validaciones desde UsuarioBase
    password: str
    roles_ids: List[int] 

class UsuarioSchema(UsuarioBase):
    id: int
    fecha_creacion: datetime
    ultima_conexion: Optional[datetime] = None
    roles: List[RolSchema] = []
    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    cedula: Optional[str] = None
    celular: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None
    biografia: Optional[str] = None
    estado: Optional[str] = None
    roles_ids: Optional[List[int]] = None

    @field_validator("nombre", "apellido")
    @classmethod
    def validate_names(cls, v):
        if not v: return v
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", v):
            raise ValueError("El nombre/apellido solo puede contener letras y espacios")
        return v

    @field_validator("cedula")
    @classmethod
    def validate_cedula(cls, v):
        if v is None: return v
        if not v.isdigit(): raise ValueError("La cédula debe contener solo números")
        if not (6 <= len(v) <= 10): raise ValueError("La cédula debe tener entre 6 y 10 dígitos")
        return v

    @field_validator("celular")
    @classmethod
    def validate_celular(cls, v):
        if v is None: return v
        if not re.match(r"^3[0-9]{9}$", v): raise ValueError("El celular debe empezar con 3 y tener exactamente 10 dígitos numéricos")
        return v

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    correo: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
