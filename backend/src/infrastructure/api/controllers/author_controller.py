""" Controlador REST para la gestión de autores. """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....application.dto.author_dto import AuthorCreateDTO, AuthorUpdateDTO, AuthorResponseDTO
from ....application.services.author_service import AuthorService
from ....infrastructure.db import get_session
from ....infrastructure.repositories.author_repo_impl import AuthorRepoImpl
from ....infrastructure.repositories.scopus_account_repo_impl import ScopusAccountRepoImpl

router = APIRouter(prefix="/authors", tags=["Autores"])


def get_author_service(session: Session = Depends(get_session)) -> AuthorService:
    """ Factory para crear el servicio de autores. """
    author_repo = AuthorRepoImpl(session)
    scopus_repo = ScopusAccountRepoImpl(session)
    return AuthorService(author_repo, scopus_repo)


@router.post("/", response_model=AuthorResponseDTO)
def create_author(dto: AuthorCreateDTO, service: AuthorService = Depends(get_author_service)):
    """ Crea un nuevo autor. """
    try:
        return service.create_author(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[AuthorResponseDTO])
def get_authors(service: AuthorService = Depends(get_author_service)):
    """ Obtiene todos los autores. """
    try:
        return service.get_authors()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/{author_id}", response_model=AuthorResponseDTO)
def get_author_by_id(author_id: int, service: AuthorService = Depends(get_author_service)):
    """ Obtiene un autor por su ID. """
    try:
        return service.get_author_by_id(author_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/department/{department_id}", response_model=List[AuthorResponseDTO])
def get_authors_by_department(department_id: int, service: AuthorService = Depends(get_author_service)):
    """ Obtiene autores por departamento. """
    try:
        return service.get_authors_by_department(department_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put("/{author_id}", response_model=AuthorResponseDTO)
def update_author(author_id: int, dto: AuthorUpdateDTO, service: AuthorService = Depends(get_author_service)):
    """ Actualiza un autor existente. """
    try:
        return service.update_author(author_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{author_id}")
def delete_author(author_id: int, service: AuthorService = Depends(get_author_service)):
    """ Elimina un autor. """
    try:
        service.delete_author(author_id)
        return {"mensaje": "Autor eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/search/{search_term}", response_model=List[AuthorResponseDTO])
def search_authors_by_name(search_term: str, service: AuthorService = Depends(get_author_service)):
    """ Busca autores por nombre completo. """
    try:
        return service.search_authors_by_name(search_term)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/scopus-ids/{search_term}")
def get_scopus_ids_by_author_name(search_term: str, service: AuthorService = Depends(get_author_service)):
    """ Obtiene los IDS de cuentas Scopus pertenecientes a un autor. """
    try:
        return service.get_scopus_account_ids_by_author_name(search_term)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
