""" Servicio para la gestión de cuentas Scopus. """
from typing import List
from ...domain.entities.scopus_account import ScopusAccount
from ...domain.repositories.scopus_account_repository import IScopusAccountRepository
from ...domain.repositories.author_repository import IAuthorRepository
from ..dto.scopus_account_dto import ScopusAccountCreateDTO, ScopusAccountUpdateDTO, ScopusAccountResponseDTO


def _to_response_dto(account: ScopusAccount) -> ScopusAccountResponseDTO:
    """Convierte una entidad ScopusAccount a DTO de respuesta."""
    return ScopusAccountResponseDTO(
        scopus_id=account.scopus_id or 0,
        username=account.username,
        affiliation=account.affiliation,
        author_id=account.author_id
    )


class ScopusAccountService:
    """ Servicio para la gestión de cuentas Scopus. """

    def __init__(self, scopus_repository: IScopusAccountRepository, author_repository: IAuthorRepository):
        self.scopus_repository = scopus_repository
        self.author_repository = author_repository

    def create_scopus_account(self, dto: ScopusAccountCreateDTO) -> ScopusAccountResponseDTO:
        """Crea una nueva cuenta Scopus."""
        # Verificar que el autor existe
        author = self.author_repository.get_by_id(dto.author_id)
        if not author:
            raise ValueError("El autor especificado no existe")

        # Verificar que no exista una cuenta con el mismo username
        existing_account = self.scopus_repository.get_by_username(dto.username)
        if existing_account:
            raise ValueError(f"Ya existe una cuenta Scopus con el username {dto.username}")

        scopus_account = ScopusAccount(
            scopus_id=None,
            username=dto.username,
            affiliation=dto.affiliation,
            author_id=dto.author_id
        )
        
        created_account = self.scopus_repository.create(scopus_account)
        return _to_response_dto(created_account)

    def get_scopus_accounts(self) -> List[ScopusAccountResponseDTO]:
        """Obtiene todas las cuentas Scopus."""
        accounts = self.scopus_repository.get_all()
        return [_to_response_dto(account) for account in accounts]

    def get_scopus_account_by_id(self, scopus_id: int) -> ScopusAccountResponseDTO:
        """Obtiene una cuenta Scopus por su ID."""
        account = self.scopus_repository.get_by_id(scopus_id)
        if not account:
            raise ValueError("Cuenta Scopus no encontrada")
        return _to_response_dto(account)

    def get_scopus_accounts_by_author(self, author_id: int) -> List[ScopusAccountResponseDTO]:
        """Obtiene cuentas Scopus por autor."""
        # Verificar que el autor existe
        author = self.author_repository.get_by_id(author_id)
        if not author:
            raise ValueError("El autor especificado no existe")

        accounts = self.scopus_repository.get_by_author_id(author_id)
        return [_to_response_dto(account) for account in accounts]

    def update_scopus_account(self, scopus_id: int, dto: ScopusAccountUpdateDTO) -> ScopusAccountResponseDTO:
        """Actualiza una cuenta Scopus existente."""
        account = self.scopus_repository.get_by_id(scopus_id)
        if not account:
            raise ValueError("Cuenta Scopus no encontrada")

        # Verificar username único si se está actualizando
        if dto.username and dto.username != account.username:
            existing_account = self.scopus_repository.get_by_username(dto.username)
            if existing_account and existing_account.scopus_id != scopus_id:
                raise ValueError(f"Ya existe una cuenta Scopus con el username {dto.username}")

        # Verificar que el nuevo autor existe si se está actualizando
        if dto.author_id and dto.author_id != account.author_id:
            author = self.author_repository.get_by_id(dto.author_id)
            if not author:
                raise ValueError("El autor especificado no existe")

        # Actualizar campos si se proporcionan
        if dto.username:
            account.username = dto.username
        if dto.affiliation:
            account.affiliation = dto.affiliation
        if dto.author_id:
            account.author_id = dto.author_id

        updated_account = self.scopus_repository.update(account)
        return _to_response_dto(updated_account)

    def delete_scopus_account(self, scopus_id: int) -> None:
        """Elimina una cuenta Scopus."""
        account = self.scopus_repository.get_by_id(scopus_id)
        if not account:
            raise ValueError("Cuenta Scopus no encontrada")
        
        self.scopus_repository.delete(scopus_id)
