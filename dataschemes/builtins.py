from abc import ABC, abstractmethod
from typing import Tuple, Callable, Dict, ClassVar, TypeVar, Type
from dataclasses import dataclass
from .converter import Converter


class UnserializableValueError(ValueError):
    """The primitive types are not able to serialize this value."""


class PrimitiveMismatchError(TypeError):
    """Type does not match what would have been serialized."""


class UnknownPrimitiveError(TypeError):
    """Primitive type cannot be converted to this native type."""


T = TypeVar("T")


@dataclass
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

    def asnative(self, cls: Type[T], value: object) -> T:
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
