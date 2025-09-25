""" Implementación del repositorio para la entidad Departamento. """
from typing import List
from sqlalchemy.orm import Session
from ...domain.entities.department import Department
from ...domain.repositories.department_repository import IDepartmentRepository
from ..models.department import DepartmentModel


class DepartmentRepoImpl(IDepartmentRepository):
    """Implementación del repositorio de departamentos."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, department: Department) -> Department:
        # No incluir dep_id para permitir autoincrement
        department_db = DepartmentModel(
            dep_code=department.dep_code,
            dep_name=department.dep_name,
            fac_name=department.fac_name
        )
        self.session.add(department_db)
        self.session.commit()
        self.session.refresh(department_db)

        # Actualizar el objeto de dominio con el ID generado
        department.dep_id = department_db.dep_id
        return department

    def get_all(self) -> List[Department]:
        departments = self.session.query(DepartmentModel).all()
        return [
            Department(
                dep_id=dep.dep_id,
                dep_code=dep.dep_code,
                dep_name=dep.dep_name,
                fac_name=dep.fac_name
            ) for dep in departments
        ]

    def get_by_id(self, dep_id: int) -> Department | None:
        department_db = self.session.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()
        if not department_db:
            raise ValueError("El departamento no fue encontrado.")
        return Department(
            dep_id=department_db.dep_id,
            dep_code=department_db.dep_code,
            dep_name=department_db.dep_name,
            fac_name=department_db.fac_name
        )

    def update(self, department: Department) -> Department:
        department_db = self.session.query(DepartmentModel).filter(DepartmentModel.dep_id == department.dep_id).first()
        if not department_db:
            raise ValueError("El departamento no fue encontrado.")

        department_db.dep_code = department.dep_code
        department_db.dep_name = department.dep_name
        department_db.fac_name = department.fac_name

        self.session.commit()
        self.session.refresh(department_db)

        return department

    def delete(self, dep_id: int) -> None:
        department_db = self.session.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()
        if not department_db:
            raise ValueError("El departamento no fue encontrado.")
        else:
            self.session.delete(department_db)
            self.session.commit()
