""" Servicio para la gestión de autores. """
from typing import List

from ..dto.author_dto import AuthorCreateDTO, AuthorUpdateDTO, AuthorResponseDTO, ScopusAccountResponseDTO
from ...domain.entities.author import Author
from ...domain.repositories.author_repository import IAuthorRepository
from ...domain.repositories.scopus_account_repository import IScopusAccountRepository
from ...domain.value_objects.author import DNI


class AuthorService:
    """ Servicio para la gestión de autores. """

    def __init__(self, author_repository: IAuthorRepository, scopus_repository: IScopusAccountRepository):
        self.author_repository = author_repository
        self.scopus_repository = scopus_repository

    def create_author(self, dto: AuthorCreateDTO) -> AuthorResponseDTO:
        """Crea un nuevo autor."""
        # Verificar que no exista un autor con el mismo DNI
        existing_author = self.author_repository.get_by_dni(dto.dni)
        if existing_author:
            raise ValueError(f"Ya existe un autor con DNI {dto.dni}")

        author = Author(
            author_id=None,
            dni=DNI(dto.dni),
            title=dto.title,
            name=dto.first_name,
            surname=dto.last_name,
            birth_date=dto.birth_date,
            gender=dto.gender,
            position=dto.position,
            department_id=dto.department_id
        )
        
        created_author = self.author_repository.create(author)
        return self._to_response_dto(created_author)

    def get_authors(self) -> List[AuthorResponseDTO]:
        """Obtiene todos los autores."""
        authors = self.author_repository.get_all()
        return [self._to_response_dto(author) for author in authors]

    def get_author_by_id(self, author_id: int) -> AuthorResponseDTO:
        """Obtiene un autor por su ID."""
        author = self.author_repository.get_by_id(author_id)
        if not author:
            raise ValueError("Autor no encontrado")
        return self._to_response_dto(author)

    def get_authors_by_department(self, department_id: int) -> List[AuthorResponseDTO]:
        """Obtiene autores por ID de departamento."""
        authors = self.author_repository.get_by_department_id(department_id)
        return [self._to_response_dto(author) for author in authors]

    def update_author(self, author_id: int, dto: AuthorUpdateDTO) -> AuthorResponseDTO:
        """Actualiza un autor existente."""
        author = self.author_repository.get_by_id(author_id)
        if not author:
            raise ValueError("Autor no encontrado")

        # Verificar DNI único si se está actualizando
        if dto.dni and dto.dni != author.dni.value:
            existing_author = self.author_repository.get_by_dni(dto.dni)
            if existing_author and existing_author.author_id != author_id:
                raise ValueError(f"Ya existe un autor con DNI {dto.dni}")

        # Actualizar campos si se proporcionan
        if dto.dni:
            author.dni = DNI(dto.dni)
        if dto.title is not None:
            author.title = dto.title
        if dto.first_name:
            author.name = dto.first_name
        if dto.last_name:
            author.surname = dto.last_name
        if dto.birth_date:
            author.birth_date = dto.birth_date
        if dto.gender:
            author.gender = dto.gender
        if dto.position:
            author.position = dto.position
        if dto.department_id:
            author.department_id = dto.department_id

        updated_author = self.author_repository.update(author)
        return self._to_response_dto(updated_author)

    def delete_author(self, author_id: int) -> None:
        """Elimina un autor."""
        author = self.author_repository.get_by_id(author_id)
        if not author:
            raise ValueError("Autor no encontrado")
        
        self.author_repository.delete(author_id)

    def search_authors_by_name(self, search_term: str) -> List[AuthorResponseDTO]:
        """Busca autores por nombre completo."""
        if not search_term or not search_term.strip():
            raise ValueError("El término de búsqueda no puede estar vacío")
        
        authors = self.author_repository.search_by_name(search_term)
        return [self._to_response_dto(author) for author in authors]

    def get_scopus_account_ids_by_author_name(self, search_term: str) -> List[dict]:
        """Obtiene los ID de cuentas Scopus por nombre de autor."""
        if not search_term or not search_term.strip():
            raise ValueError("El término de búsqueda no puede estar vacío")
        
        authors = self.author_repository.search_by_name(search_term)
        result = []
        
        for author in authors:
            scopus_accounts = self.scopus_repository.get_by_author_id(author.author_id or 0)
            scopus_ids = [account.scopus_id for account in scopus_accounts if account.scopus_id]
            
            if scopus_ids:  # Solo incluir autores que tienen cuentas Scopus
                result.append({
                    "author_id": author.author_id,
                    "full_name": author.full_name,
                    "dni": author.dni.value,
                    "scopus_account_ids": scopus_ids
                })
        
        return result

    def _to_response_dto(self, author: Author) -> AuthorResponseDTO:
        """Convierte una entidad Author a DTO de respuesta."""
        # Obtener las cuentas Scopus del autor
        scopus_accounts = self.scopus_repository.get_by_author_id(author.author_id or 0)
        scopus_dtos = [
            ScopusAccountResponseDTO(
                scopus_id=account.scopus_id,
                username=account.username,
                affiliation=account.affiliation
            )
            for account in scopus_accounts
        ]

        return AuthorResponseDTO(
            author_id=author.author_id or 0,
            dni=author.dni.value,
            title=author.title,
            first_name=author.name,
            last_name=author.surname,
            birth_date=author.birth_date,
            gender=author.gender,
            position=author.position,
            department_id=author.department_id,
            scopus_accounts=scopus_dtos
        )