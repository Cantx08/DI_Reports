""" Interfaz del repositorio para la entidad de Cuenta Scopus. """
from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.entities.scopus_account import ScopusAccount


class IScopusAccountRepository(ABC):
    """ Repositorio de cuentas Scopus."""
    @abstractmethod
    def create(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """ Agregar una cuenta de Scopus. """
        pass

    @abstractmethod
    def get_all(self) -> List[ScopusAccount]:
        """ Obtener todas las cuentas Scopus. """
        pass

    @abstractmethod
    def get_by_id(self, scopus_id: int) -> Optional[ScopusAccount]:
        """ Obtener una cuenta Scopus por su ID. """
        pass

    @abstractmethod
    def get_by_author_id(self, author_id: int) -> List[ScopusAccount]:
        """ Obtener cuentas Scopus por ID de autor. """
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[ScopusAccount]:
        """ Obtener una cuenta Scopus por nombre de usuario. """
        pass

    @abstractmethod
    def update(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """ Actualizar una cuenta Scopus existente."""
        pass

    @abstractmethod
    def delete(self, scopus_id: int) -> None:
        """ Eliminar una cuenta Scopus. """
        pass
