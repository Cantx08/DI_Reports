""" Módulo que define la entidad Cuenta Scopus. """
from dataclasses import dataclass
from typing import Optional
from ..exceptions.domain_exceptions import EmptyFieldException


@dataclass
class ScopusAccount:
    """ Entidad que representa una cuenta de Scopus asociada a un autor. """

    scopus_id: Optional[int]
    username: str
    affiliation: str
    author_id: int

    def __post_init__(self):
        if not self.username or not self.username.strip():
            raise EmptyFieldException("nombre de usuario")
        if not self.affiliation or not self.affiliation.strip():
            raise EmptyFieldException("afiliación")
        if self.author_id is None or self.author_id <= 0:
            raise ValueError("ID de autor inválido")

    def __str__(self):
        return f"{self.username} - {self.affiliation}"