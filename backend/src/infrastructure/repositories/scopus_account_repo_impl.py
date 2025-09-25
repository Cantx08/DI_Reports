""" Implementación del repositorio para la entidad ScopusAccount. """
from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.entities.scopus_account import ScopusAccount
from ...domain.repositories.scopus_account_repository import IScopusAccountRepository
from ..models.scopus_account import ScopusAccountModel


def _to_domain_entity(account_db: ScopusAccountModel) -> ScopusAccount:
    """Convierte un modelo de base de datos a entidad de dominio."""
    return ScopusAccount(
        scopus_id=account_db.scopus_id,
        username=account_db.username,
        affiliation=account_db.affiliation,
        author_id=account_db.author_id
    )


class ScopusAccountRepoImpl(IScopusAccountRepository):
    """Implementación del repositorio de cuentas Scopus."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """Crea una nueva cuenta Scopus."""
        scopus_db = ScopusAccountModel(
            username=scopus_account.username,
            affiliation=scopus_account.affiliation,
            author_id=scopus_account.author_id
        )
        self.session.add(scopus_db)
        self.session.commit()
        self.session.refresh(scopus_db)

        # Actualizar el objeto de dominio con el ID generado
        scopus_account.scopus_id = scopus_db.scopus_id
        return scopus_account

    def get_all(self) -> List[ScopusAccount]:
        """Obtiene todas las cuentas Scopus."""
        accounts = self.session.query(ScopusAccountModel).all()
        return [_to_domain_entity(account_db) for account_db in accounts]

    def get_by_id(self, scopus_id: int) -> Optional[ScopusAccount]:
        """Obtiene una cuenta Scopus por su ID."""
        account_db = self.session.query(ScopusAccountModel).filter(ScopusAccountModel.scopus_id == scopus_id).first()
        if not account_db:
            return None
        return _to_domain_entity(account_db)

    def get_by_author_id(self, author_id: int) -> List[ScopusAccount]:
        """Obtiene cuentas Scopus por ID de autor."""
        accounts = self.session.query(ScopusAccountModel).filter(ScopusAccountModel.author_id == author_id).all()
        return [_to_domain_entity(account_db) for account_db in accounts]

    def get_by_username(self, username: str) -> Optional[ScopusAccount]:
        """Obtiene una cuenta Scopus por nombre de usuario."""
        account_db = self.session.query(ScopusAccountModel).filter(ScopusAccountModel.username == username).first()
        if not account_db:
            return None
        return _to_domain_entity(account_db)

    def update(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """Actualiza una cuenta Scopus existente."""
        account_db = self.session.query(ScopusAccountModel).filter(
            ScopusAccountModel.scopus_id == scopus_account.scopus_id).first()
        if not account_db:
            raise ValueError("La cuenta Scopus no fue encontrada.")

        account_db.username = scopus_account.username
        account_db.affiliation = scopus_account.affiliation
        account_db.author_id = scopus_account.author_id

        self.session.commit()
        self.session.refresh(account_db)

        return scopus_account

    def delete(self, scopus_id: int) -> None:
        """Elimina una cuenta Scopus."""
        account_db = self.session.query(ScopusAccountModel).filter(ScopusAccountModel.scopus_id == scopus_id).first()
        if not account_db:
            raise ValueError("La cuenta Scopus no fue encontrada.")

        self.session.delete(account_db)
        self.session.commit()
