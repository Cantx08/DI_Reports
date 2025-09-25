""" Controlador REST para la gestión de departamentos. """
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from ....application.dto.department_dto import DepartmentResponseDTO, DepartmentCreateDTO, DepartmentUpdateDTO
from ....application.services.department_service import DepartmentService
from ....infrastructure.db import get_session
from ....infrastructure.repositories.department_repo_impl import DepartmentRepoImpl

router = APIRouter(prefix="/deps", tags=["Departamentos"])


def get_service(session: Session = Depends(get_session)) -> DepartmentService:
    """ Factory para crear el servicio de departamentos. """
    repo = DepartmentRepoImpl(session)
    return DepartmentService(repo)


@router.post("/", response_model=DepartmentResponseDTO)
def create_department(dto: DepartmentCreateDTO, service: DepartmentService = Depends(get_service)):
    """ Crea un nuevo departamento. """
    try:
        return service.create_department(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=list[DepartmentResponseDTO])
def get_departments(service: DepartmentService = Depends(get_service)):
    """ Obtiene todos los departamentos. """
    try:
        return service.get_departments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/{dep_id}", response_model=DepartmentResponseDTO)
def get_department_by_id(dep_id: int, service: DepartmentService = Depends(get_service)):
    """ Obtiene un departamento por su ID. """
    try:
        return service.get_department_by_id(dep_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put("/{dep_id}", response_model=DepartmentResponseDTO)
def update_department(dep_id: int, dto: DepartmentUpdateDTO, service: DepartmentService = Depends(get_service)):
    """ Actualiza un departamento existente. """
    try:
        return service.update_department(dep_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{dep_id}")
def delete_department(dep_id: int, service: DepartmentService = Depends(get_service)):
    """ Elimina un departamento. """
    try:
        service.delete_department(dep_id)
        return {"mensaje": "Departamento eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
