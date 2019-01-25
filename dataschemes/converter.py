from abc import ABC, abstractmethod
from typing import Set, TypeVar, Union, Tuple, Callable, Dict


def converters(method):
    return {
        type_: getattr(Converter(), method)
        for type_, Converter in {
            bool: BoolConverter,
            str: StrConverter,
            int: IntConverter,
            float: FloatConverter,
        }.items()
    }


class UnserializableValueError(ValueError):
    """The primitive types are not able to serialize this value."""


class PrimitiveMismatchError(TypeError):
    """Type does not match what would have been serialized."""


class UnknownPrimitiveError(TypeError):
    """Primitive type cannot be converted to this native type."""


class Converter(ABC):
    @abstractmethod
    def asprimitive(self, value: object, types: Set[type] = None) -> object:
        raise NotImplementedError

    @abstractmethod
    def asnative(self, value: object, types: Set[type] = None) -> object:
        raise NotImplementedError


class AtomConverter(Converter):
    """A non-collection converter."""

    type: type
    options: Dict[type, Tuple[Callable[[object], object], Callable[[object], object]]]

    def preferred(self):
        return next(iter(self.options.items()))

    def asprimitive(self, value: object, types: Set[type] = None) -> object:
        _, (converter, _) = self.preferred()
        if types is None:
            return converter(value)

        for type_, (converter, _) in self.options.items():
            if type_ in types:
                return converter(value)

        raise UnserializableValueError(
            f"Could not convert '{self.type}' to any of these types: {types}"
        )

    def asnative(self, value: object, types: Set[type] = None) -> object:
        _, (_, converter) = self.preferred()
        if types is None:
            return converter(value)

        for type_, (_, converter) in self.options.items():
            if type_ in types:
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


class IntConverter(AtomConverter):
    """Convert the int built-in type."""

    type = int
    options = {int: (int, int), float: (float, int), str: (str, int)}


class FloatConverter(AtomConverter):
    """Convert the float built-in type."""

    type = float
    options = {float: (float, float), str: (str, float)}


class BoolConverter(AtomConverter):
    """Convert the bool built-in type."""

    type = bool
    options = {bool: (bool, bool), int: (int, bool)}
