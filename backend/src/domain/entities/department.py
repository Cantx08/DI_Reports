""" Módulo que define la entidad Departamento. """
from dataclasses import dataclass
from typing import Optional
from ..exceptions.domain_exceptions import EmptyFieldException


@dataclass
class Department:
    """Clase que representa un departamento."""

    dep_id: Optional[int]
    dep_code: str
    dep_name: str
    fac_name: str

    def __post_init__(self):
        if not self.dep_code:
            raise EmptyFieldException("sigla de departamento")
        if not self.dep_name:
            raise EmptyFieldException("departamento")
        if not self.fac_name:
            raise EmptyFieldException("facultad")

    def __str__(self):
        return f"{self.dep_name} ({self.dep_code})"
