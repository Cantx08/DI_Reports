"""
Controlador REST para la gestión de cuentas Scopus.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....application.dto.scopus_account_dto import ScopusAccountCreateDTO, ScopusAccountUpdateDTO, ScopusAccountResponseDTO
from ....application.services.scopus_account_service import ScopusAccountService
from ....infrastructure.db import get_session
from ....infrastructure.repositories.author_repo_impl import AuthorRepoImpl
from ....infrastructure.repositories.scopus_account_repo_impl import ScopusAccountRepoImpl

router = APIRouter(prefix="/scopus-accounts", tags=["Cuentas Scopus"])


def get_scopus_service(session: Session = Depends(get_session)) -> ScopusAccountService:
    """Factory para crear el servicio de cuentas Scopus."""
    scopus_repo = ScopusAccountRepoImpl(session)
    author_repo = AuthorRepoImpl(session)
    return ScopusAccountService(scopus_repo, author_repo)


@router.post("/", response_model=ScopusAccountResponseDTO)
def create_scopus_account(dto: ScopusAccountCreateDTO, service: ScopusAccountService = Depends(get_scopus_service)):
    """Crea una nueva cuenta Scopus."""
    try:
        return service.create_scopus_account(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[ScopusAccountResponseDTO])
def get_scopus_accounts(service: ScopusAccountService = Depends(get_scopus_service)):
    """Obtiene todas las cuentas Scopus."""
    try:
        return service.get_scopus_accounts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/{scopus_id}", response_model=ScopusAccountResponseDTO)
def get_scopus_account_by_id(scopus_id: int, service: ScopusAccountService = Depends(get_scopus_service)):
    """Obtiene una cuenta Scopus por su ID."""
    try:
        return service.get_scopus_account_by_id(scopus_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/author/{author_id}", response_model=List[ScopusAccountResponseDTO])
def get_scopus_accounts_by_author(author_id: int, service: ScopusAccountService = Depends(get_scopus_service)):
    """Obtiene cuentas Scopus por autor."""
    try:
        return service.get_scopus_accounts_by_author(author_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put("/{scopus_id}", response_model=ScopusAccountResponseDTO)
def update_scopus_account(scopus_id: int, dto: ScopusAccountUpdateDTO, service: ScopusAccountService = Depends(get_scopus_service)):
    """Actualiza una cuenta Scopus existente."""
    try:
        return service.update_scopus_account(scopus_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{scopus_id}")
def delete_scopus_account(scopus_id: int, service: ScopusAccountService = Depends(get_scopus_service)):
    """Elimina una cuenta Scopus."""
    try:
        service.delete_scopus_account(scopus_id)
        return {"mensaje": "Cuenta Scopus eliminada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")