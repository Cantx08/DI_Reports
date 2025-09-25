from .base import Base
from sqlalchemy import Column, Integer, String


class DepartmentModel(Base):
    """Modelo para la tabla de departamentos."""
    __tablename__ = "departments"

    dep_id = Column(Integer, primary_key=True, autoincrement=True)
    dep_code = Column(String(10), unique=True, nullable=False)
    dep_name = Column(String(100), nullable=False)
    fac_name = Column(String(100), nullable=False)
