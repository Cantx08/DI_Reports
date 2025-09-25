""" DTOS para Cuenta Scopus. """
from typing import Optional
from pydantic import BaseModel, Field


class ScopusAccountCreateDTO(BaseModel):
    """DTO para crear una cuenta Scopus."""
    username: str = Field(..., description="Nombre de usuario en Scopus")
    affiliation: str = Field(..., description="Afiliación institucional")
    author_id: int = Field(..., description="ID del autor")


class ScopusAccountUpdateDTO(BaseModel):
    """DTO para actualizar una cuenta Scopus."""
    username: Optional[str] = Field(None, description="Nombre de usuario en Scopus")
    affiliation: Optional[str] = Field(None, description="Afiliación institucional")
    author_id: Optional[int] = Field(None, description="ID del autor")


class ScopusAccountResponseDTO(BaseModel):
    """DTO para la respuesta de cuenta Scopus."""
    scopus_id: int
    username: str
    affiliation: str
    author_id: int

    class Config:
        from_attributes = True