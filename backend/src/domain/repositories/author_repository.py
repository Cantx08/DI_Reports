""" Interfaz del repositorio para la entidad Author. """
from abc import ABC, abstractmethod
from typing import List, Optional
from ...domain.entities.author import Author


class IAuthorRepository(ABC):
    """ Repositorio de autores. """

    @abstractmethod
    def create(self, author: Author) -> Author:
        """ Agregar un autor. """
        pass

    @abstractmethod
    def get_all(self) -> List[Author]:
        """ Obtener todos los autores. """
        pass

    @abstractmethod
    def get_by_id(self, author_id: int) -> Optional[Author]:
        """ Obtener un autor por su ID. """
        pass

    @abstractmethod
    def get_by_dni(self, dni: str) -> Optional[Author]:
        """ Obtiene un autor por su DNI. """
        pass

    @abstractmethod
    def get_by_department_id(self, department_id: int) -> List[Author]:
        """ Obtiene autores por ID de departamento. """
        pass

    @abstractmethod
    def update(self, author: Author) -> Author:
        """ Actualizar un autor existente. """
        pass

    @abstractmethod
    def delete(self, author_id: int) -> None:
        """ Eliminar un autor. """
        pass

    @abstractmethod
    def search_by_name(self, search_term: str) -> List[Author]:
        """ Buscar autores por nombre completo. """
        pass
