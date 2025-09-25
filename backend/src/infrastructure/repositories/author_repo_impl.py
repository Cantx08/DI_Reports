""" Implementación del repositorio para la entidad Autor. """
from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.entities.author import Author
from ...domain.repositories.author_repository import IAuthorRepository
from ...domain.value_objects.author import DNI
from ..models.author import AuthorModel


def _to_domain_entity(author_db: AuthorModel) -> Author:
    """Convierte un modelo de base de datos a entidad de dominio."""
    return Author(
        author_id=author_db.author_id,
        dni=DNI(author_db.dni),
        title=author_db.title,
        name=author_db.first_name,
        surname=author_db.last_name,
        birth_date=author_db.birth_date,
        gender=author_db.gender,
        position=author_db.position,
        department_id=author_db.department_id
    )


class AuthorRepoImpl(IAuthorRepository):
    """Implementación del repositorio de autores."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, author: Author) -> Author:
        """Crea un nuevo autor."""
        author_db = AuthorModel(
            dni=author.dni.value,
            title=author.title,
            first_name=author.name,
            last_name=author.surname,
            birth_date=author.birth_date,
            gender=author.gender,
            position=author.position,
            department_id=author.department_id
        )
        self.session.add(author_db)
        self.session.commit()
        self.session.refresh(author_db)

        # Actualizar el objeto de dominio con el ID generado
        author.author_id = author_db.author_id
        return author

    def get_all(self) -> List[Author]:
        """Obtiene todos los autores."""
        authors = self.session.query(AuthorModel).all()
        return [_to_domain_entity(author_db) for author_db in authors]

    def get_by_id(self, author_id: int) -> Optional[Author]:
        """Obtiene un autor por su ID."""
        author_db = self.session.query(AuthorModel).filter(AuthorModel.author_id == author_id).first()
        if not author_db:
            return None
        return _to_domain_entity(author_db)

    def get_by_dni(self, dni: str) -> Optional[Author]:
        """Obtiene un autor por su DNI."""
        author_db = self.session.query(AuthorModel).filter(AuthorModel.dni == dni).first()
        if not author_db:
            return None
        return _to_domain_entity(author_db)

    def get_by_department_id(self, department_id: int) -> List[Author]:
        """Obtiene autores por ID de departamento."""
        authors = self.session.query(AuthorModel).filter(AuthorModel.department_id == department_id).all()
        return [_to_domain_entity(author_db) for author_db in authors]

    def update(self, author: Author) -> Author:
        """Actualiza un autor existente."""
        author_db = self.session.query(AuthorModel).filter(AuthorModel.author_id == author.author_id).first()
        if not author_db:
            raise ValueError("El autor no fue encontrado.")

        author_db.dni = author.dni.value
        author_db.title = author.title
        author_db.first_name = author.name
        author_db.last_name = author.surname
        author_db.birth_date = author.birth_date
        author_db.gender = author.gender
        author_db.position = author.position
        author_db.department_id = author.department_id

        self.session.commit()
        self.session.refresh(author_db)

        return author

    def delete(self, author_id: int) -> None:
        """Elimina un autor."""
        author_db = self.session.query(AuthorModel).filter(AuthorModel.author_id == author_id).first()
        if not author_db:
            raise ValueError("El autor no fue encontrado.")

        self.session.delete(author_db)
        self.session.commit()

    def search_by_name(self, search_term: str) -> List[Author]:
        """Busca autores por nombre completo (nombres y apellidos)."""
        # Buscar por nombres, apellidos o nombre completo
        search_pattern = f"%{search_term.strip()}%"
        authors = self.session.query(AuthorModel).filter(
            (AuthorModel.first_name.ilike(search_pattern)) |
            (AuthorModel.last_name.ilike(search_pattern)) |
            ((AuthorModel.first_name + ' ' + AuthorModel.last_name).ilike(search_pattern)) |
            ((AuthorModel.last_name + ' ' + AuthorModel.first_name).ilike(search_pattern))
        ).all()
        return [_to_domain_entity(author_db) for author_db in authors]
