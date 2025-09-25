""" DTOS para Departamento. """
from typing import Optional

from pydantic import BaseModel


class DepartmentCreateDTO(BaseModel):
    """ DTO para crear un departamento. """
    dep_code: str
    dep_name: str
    fac_name: str


class DepartmentUpdateDTO(BaseModel):
    """ DTO para actualizar un departamento. """
    dep_code: Optional[str] = None
    dep_name: Optional[str] = None
    fac_name: Optional[str] = None


class DepartmentResponseDTO(BaseModel):
    """ DTO para la respuesta de un departamento. """
    dep_id: int
    dep_code: str
    dep_name: str
    fac_name: str

    class Config:
        from_attributes = True
