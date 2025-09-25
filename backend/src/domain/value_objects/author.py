""" Value Objects relacionados con el dominio de Autor. """
from dataclasses import dataclass
from ..exceptions.domain_exceptions import EmptyFieldException


@dataclass(frozen=True)
class DNI:
    """ Value Object que representa un DNI. """
    value: str

    def __post_init__(self):
        if self.value is None or not self.value.strip():
            raise EmptyFieldException("DNI")
        if not self.validate_dni():
            raise ValueError("DNI incorrecto.")

    def validate_dni(self) -> bool:
        valid_dni = False
        if self.value.isdigit() and len(self.value) == 10:
            state_digit = int(self.value[0:2])
            if 1 <= state_digit <= 24:
                coefficients = [2, 1, 2, 1, 2, 1, 2, 1, 2]
                total = 0
                for i in range(9):
                    digit = int(self.value[i]) * coefficients[i]
                    if digit >= 10:
                        digit -= 9
                    total += digit
                check_digit = (10 - (total % 10)) % 10
                if check_digit == int(self.value[9]):
                    valid_dni = True
        return valid_dni
