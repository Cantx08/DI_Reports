""" Interfaz del repositorio para la entidad de Departamento. """
from abc import ABC, abstractmethod
from typing import List

from ..entities.department import Department


class IDepartmentRepository(ABC):
    """ Repositorio de departamentos. """

    @abstractmethod
    def create(self, department: Department) -> Department:
        """ Agregar un departamento. """
        pass

    @abstractmethod
    def get_all(self) -> List[Department]:
        """ Obtener todos los departamentos. """
        pass

    @abstractmethod
    def get_by_id(self, dep_id: int) -> Department:
        """ Obtener un departamento por su id. """
        pass


    @abstractmethod
    def update(self, department: Department) -> Department:
        """ Actualizar un departamento. """
        pass

    @abstractmethod
    def delete(self, dep_id: int) -> None:
        """ Eliminar un departamento. """
        pass
