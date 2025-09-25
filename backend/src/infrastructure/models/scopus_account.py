"""
Modelo SQLAlchemy para la entidad ScopusAccount.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class ScopusAccountModel(Base):
    """Modelo para la tabla de cuentas Scopus."""
    __tablename__ = "scopus_accounts"

    scopus_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    affiliation = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=False)

    # Relaciones
    author = relationship("AuthorModel", back_populates="scopus_accounts")