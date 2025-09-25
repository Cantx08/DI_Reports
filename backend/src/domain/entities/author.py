""" Módulo que define la entidad Autor. """
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional
from ..exceptions.domain_exceptions import EmptyFieldException
from ..value_objects.author import DNI

# Constantes para la validación de fechas de nacimiento
MIN_DATE = date(1950, 1, 1)
MAX_DATE = date(2000, 1, 1)


class Gender(Enum):
    """ Enum para el género del docente. """
    MASCULINO = "M"
    FEMENINO = "F"


@dataclass
class Author:
    """ Entidad que representa un autor. """
    author_id: Optional[int]
    dni: DNI
    title: Optional[str]
    name: str
    surname: str
    birth_date: date
    gender: Gender
    position: str
    department_id: int

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise EmptyFieldException("nombres")
        if not self.surname or not self.surname.strip():
            raise EmptyFieldException("apellidos")
        if not self.birth_date:
            raise EmptyFieldException("fecha de nacimiento")
        if not self.gender:
            raise EmptyFieldException("género")
        if self.gender not in Gender:
            raise ValueError("Género inválido. Debe ser 'M' o 'F'.")
        if not self.position or not self.position.strip():
            raise EmptyFieldException("cargo")
        if not self.department_id or self.department_id <= 0:
            raise ValueError("El investigador debe pertenecer a un departamento.")
        if not self.is_birth_date_valid():
            raise ValueError(f"Fecha fuera de rango permitido: {MIN_DATE} y {MAX_DATE}.")

    def __str__(self):
        if not self.title:
            return f"{self.name} {self.surname}"
        return f"{self.title} {self.name} {self.surname}"
    
    @property
    def full_name(self) -> str:
        """ Retorna el nombre completo del autor. """
        return f"{self.name} {self.surname}"

    def is_birth_date_valid(self) -> bool:
        return MIN_DATE <= self.birth_date <= MAX_DATE
