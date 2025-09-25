""" DTOS para Autor. """
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field
from ...domain.entities.author import Gender


class AuthorCreateDTO(BaseModel):
    """DTO para crear un autor."""
    dni: str = Field(..., description="DNI del autor")
    title: Optional[str] = Field(None, description="Título académico")
    first_name: str = Field(..., description="Nombres del autor")
    last_name: str = Field(..., description="Apellidos del autor")
    birth_date: date = Field(..., description="Fecha de nacimiento")
    gender: Gender = Field(..., description="Género")
    position: str = Field(..., description="Cargo o posición")
    department_id: int = Field(..., description="ID del departamento")


class AuthorUpdateDTO(BaseModel):
    """DTO para actualizar un autor."""
    dni: Optional[str] = Field(None, description="DNI del autor")
    title: Optional[str] = Field(None, description="Título académico")
    first_name: Optional[str] = Field(None, description="Nombres del autor")
    last_name: Optional[str] = Field(None, description="Apellidos del autor")
    birth_date: Optional[date] = Field(None, description="Fecha de nacimiento")
    gender: Optional[Gender] = Field(None, description="Género")
    position: Optional[str] = Field(None, description="Cargo o posición")
    department_id: Optional[int] = Field(None, description="ID del departamento")


class ScopusAccountResponseDTO(BaseModel):
    """DTO para la respuesta de cuenta Scopus."""
    scopus_id: int
    username: str
    affiliation: str

    class Config:
        from_attributes = True


class AuthorResponseDTO(BaseModel):
    """DTO para la respuesta de autor."""
    author_id: int
    dni: str
    title: Optional[str]
    first_name: str
    last_name: str
    birth_date: date
    gender: Gender
    position: str
    department_id: int
    scopus_accounts: Optional[List[ScopusAccountResponseDTO]] = []

    class Config:
        from_attributes = True