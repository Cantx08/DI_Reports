from ...application.dto.department_dto import DepartmentCreateDTO, DepartmentResponseDTO, DepartmentUpdateDTO
from ...domain.entities.department import Department
from ...domain.repositories.department_repository import IDepartmentRepository


class DepartmentService:
    """Servicio para la gestión de departamentos."""

    def __init__(self, repository: IDepartmentRepository):
        self.repository = repository

    def create_department(self, dto: DepartmentCreateDTO) -> DepartmentResponseDTO:
        department = Department(
            dep_id=None,  # Se asignará automáticamente por la BD
            dep_code=dto.dep_code,
            dep_name=dto.dep_name,
            fac_name=dto.fac_name
        )
        created_department = self.repository.create(department)
        return DepartmentResponseDTO(
            dep_id=created_department.dep_id,
            dep_code=created_department.dep_code,
            dep_name=created_department.dep_name,
            fac_name=created_department.fac_name
        )

    def get_departments(self) -> list[DepartmentResponseDTO]:
        departments = self.repository.get_all()
        return [
            DepartmentResponseDTO(
                dep_id=dep.dep_id,
                dep_code=dep.dep_code,
                dep_name=dep.dep_name,
                fac_name=dep.fac_name
            ) for dep in departments
        ]

    def get_department_by_id(self, dep_id: int) -> DepartmentResponseDTO:
        department = self.repository.get_by_id(dep_id)
        return DepartmentResponseDTO(
            dep_id=department.dep_id,
            dep_code=department.dep_code,
            dep_name=department.dep_name,
            fac_name=department.fac_name
        )

    def update_department(self, dep_id: int, dep_dto: DepartmentUpdateDTO) -> DepartmentResponseDTO:
        department = self.repository.get_by_id(dep_id)
        if not department:
            raise ValueError("Departamento no encontrado.")

        if dep_dto.dep_code: department.dep_code = dep_dto.dep_code
        if dep_dto.dep_name: department.dep_name = dep_dto.dep_name
        if dep_dto.fac_name: department.fac_name = dep_dto.fac_name

        updated = self.repository.update(department)
        return DepartmentResponseDTO(
            dep_id=updated.dep_id,
            dep_code=updated.dep_code,
            dep_name=updated.dep_name,
            fac_name=updated.fac_name
        )

    def delete_department(self, dep_id: int):
        return self.repository.delete(dep_id)
