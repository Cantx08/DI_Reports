"""Excepciones personalizadas para el dominio de la aplicación."""


class DomainException(Exception):
    """Base para todas las excepciones del dominio."""
    pass


class EmptyFieldException(DomainException):
    """Excepción lanzada cuando un campo obligatorio está vacío."""

    def __init__(self, field: str):
        super().__init__(f"El campo '{field}' no puede estar vacío.")
        self.field = field
