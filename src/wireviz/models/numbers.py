from math import modf
from typing import Any, Union

from pydantic import BaseModel, validator


class NumberAndUnit(BaseModel):
    number: float
    unit: Union[str, None] = None

    def __init__(self, number, unit=None, **data):
        super().__init__(number=number, unit=unit, **data)

    @classmethod
    def to_number_and_unit(
        cls,
        inp: Any,
        default_unit: Union[str, None] = None,
        default_value: Union[float, None] = None,
    ):
        if inp is None:
            if default_value is not None:
                return cls(number=default_value, unit=default_unit)
            return None
        elif isinstance(inp, NumberAndUnit):
            return inp
        elif isinstance(inp, float) or isinstance(inp, int):
            return cls(number=float(inp), unit=default_unit)
        elif isinstance(inp, str):
            if " " in inp:
                number, unit = inp.split(" ", 1)
            else:
                number, unit = inp, default_unit
            try:
                number = float(number)
            except ValueError:
                raise Exception(
                    f"{inp} is not a valid number and unit.\n"
                    "It must be a number, or a number and unit separated by a space."
                )
            else:
                return cls(number=number, unit=unit)

    def chose_unit(self, other):
        if self.unit is None:
            return other.unit

        if other.unit is not None and self.unit != other.unit:
            raise ValueError(f"Cannot add {self} and {other}, units not matching")
        return self.unit

    @property
    def number_str(self):
        return f"{self.number:.2f}" if modf(self.number)[0] else f"{int(self.number)}"

    @property
    def unit_str(self):
        return "" if self.unit is None else self.unit

    def __str__(self):
        return " ".join((self.number_str, self.unit_str)).strip()

    def __eq__(self, other):
        return self.number == other.number and self.unit == other.unit

    class Config:
        arbitrary_types_allowed = True
        allow_mutation = True
        allow_population_by_field_name = True

    def __add__(self, other):
        other = NumberAndUnit.to_number_and_unit(other, self.unit, 0)

        return NumberAndUnit(
            number=float(self.number) + float(other.number),
            unit=self.chose_unit(other),
        )

    def __mul__(self, other):
        other = NumberAndUnit.to_number_and_unit(other, self.unit, 1)

        return NumberAndUnit(
            number=float(self.number) * float(other.number),
            unit=self.chose_unit(other),
        )
