from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ....application.dto.department_dto import DepartmentResponseDTO, DepartmentCreateDTO, DepartmentUpdateDTO
from ....application.services.department_service import DepartmentService
from ....infrastructure.db import get_session
from ....infrastructure.repositories.department_repo_impl import DepartmentRepoImpl

router = APIRouter(prefix="/deps", tags=["Departamentos"])


def get_service(session: Session = Depends(get_session)) -> DepartmentService:
    repo = DepartmentRepoImpl(session)
    return DepartmentService(repo)


@router.post("/", response_model=DepartmentResponseDTO)
def create_department(dto: DepartmentCreateDTO, service: DepartmentService = Depends(get_service)):
    return service.create_department(dto)


@router.put("/{dep_id}", response_model=DepartmentResponseDTO)
def update_department(dep_id: int, dto: DepartmentUpdateDTO, service: DepartmentService = Depends(get_service)):
    return service.update_department(dep_id, dto)


@router.get("/{dep_id}", response_model=DepartmentResponseDTO)
def get_department_by_id(dep_id: int, service: DepartmentService = Depends(get_service)):
    return service.get_department_by_id(dep_id)


@router.get("/", response_model=list[DepartmentResponseDTO])
def get_departments(service: DepartmentService = Depends(get_service)):
    return service.get_departments()


@router.delete("/{dep_id}")
def delete_department(dep_id: int, service: DepartmentService = Depends(get_service)):
    service.delete_department(dep_id)
    return {"mensaje": "Departamento eliminado correctamente"}
