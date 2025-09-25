"""
Modelo SQLAlchemy para la entidad Author.
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .base import Base
from ...domain.entities.author import Gender


class AuthorModel(Base):
    """Modelo para la tabla de autores."""
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(10), unique=True, nullable=False)
    title = Column(String(50), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    position = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.dep_id'), nullable=False)

    # Relaciones
    department = relationship("DepartmentModel", back_populates="authors")
    scopus_accounts = relationship("ScopusAccountModel", back_populates="author", cascade="all, delete-orphan")