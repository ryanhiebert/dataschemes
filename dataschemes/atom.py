from abc import ABC, abstractmethod
from typing import Tuple, Callable, Dict, ClassVar
from .converter import (
    Converter,
    UnserializableValueError,
    PrimitiveMismatchError,
    UnknownPrimitiveError,
)


class AtomConverter(Converter):
    """A non-collection converter."""

    type: ClassVar[type]
    options: ClassVar[
        Dict[type, Tuple[Callable[[object], object], Callable[[object], object]]]
    ]

    def preferred(self):
        return next(iter(self.options.items()))

    def asprimitive(self, value: object) -> object:
        _, (converter, _) = self.preferred()
        if self.types is None:
            return converter(value)

        for type_, (converter, _) in self.options.items():
            if type_ in self.types:
                return converter(value)

        raise UnserializableValueError(
            f"Could not convert '{self.type}' to any of these types: {self.types}"
        )

    def asnative(self, value: object) -> object:
        _, (_, converter) = self.preferred()
        if self.types is None:
            return converter(value)

        for type_, (_, converter) in self.options.items():
            if type_ in self.types:
                if isinstance(value, type_):
                    return converter(value)
                raise PrimitiveMismatchError(
                    f"'{self.type}' would have been converted to '{type_}', "
                    f"but got a '{type(value)}' instead."
                )

        raise UnknownPrimitiveError(
            f"No converter found to convert '{type(value)}' to '{self.type}'."
        )


class StrConverter(AtomConverter):
    """Convert the str built-in type."""

    type = str
    options = {str: (str, str)}


class BoolConverter(AtomConverter):
    """Convert the bool built-in type."""

    type = bool
    options = {bool: (bool, bool), int: (int, bool)}


class IntConverter(AtomConverter):
    """Convert the int built-in type."""

    type = int
    options = {int: (int, int), float: (float, int), str: (str, int)}


class FloatConverter(AtomConverter):
    """Convert the float built-in type."""

    type = float
    options = {float: (float, float), str: (str, float)}
