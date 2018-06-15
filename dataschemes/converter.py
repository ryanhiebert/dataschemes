from abc import ABCMeta, abstractmethod
from typing import Set, TypeVar, Union, Tuple, Callable, Dict


def converters(method):
    return {
        type_: getattr(Converter(), method)
        for type_, Converter in {
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


class Converter(metaclass=ABCMeta):
    @abstractmethod
    def asprimitive(self, value: object, types: Set[type] = None) -> object:
        raise NotImplementedError

    @abstractmethod
    def asnative(self, value: object, types: Set[type] = None) -> object:
        raise NotImplementedError


class AtomConverter(Converter):
    """The common elements between atom converters."""

    type: type
    options: Dict[type, Tuple[Callable[[object], object], Callable[[object], object]]]

    def asprimitive(self, value: object, types: Set[type] = None) -> object:
        preferred = next(iter(self.options.items()))
        _, (converter, _) = preferred
        if types is None:
            return converter(value)

        for type_, (converter, _) in self.options.items():
            if type_ in types:
                return converter(value)

        raise UnserializableValueError(f"Could not convert {self.type} to a primitive.")


class StrConverter(AtomConverter):
    """Convert the str built-in type."""

    type: str
    options = {str: (str, str)}

    def asnative(self, value: object, types: Set[type] = None) -> str:
        if types is None:
            return str(value)
        elif str in types:
            if isinstance(value, str):
                return value
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        else:
            raise UnknownPrimitiveError(
                "Primitive type cannot be converted to this native type."
            )


class IntConverter(AtomConverter):
    """Convert the int built-in type."""

    type: int
    options = {int: (int, int), float: (float, int), str: (str, int)}

    def asnative(self, value: object, types: Set[type] = None) -> int:
        if types is None:
            return int(value)
        elif int in types:
            if isinstance(value, int):
                return value
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        elif float in types:
            if isinstance(value, float):
                return int(value)
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        elif str in types:
            if isinstance(value, str):
                return int(value)
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        else:
            raise UnknownPrimitiveError(
                "Primitive type cannot be converted to this native type."
            )


class FloatConverter(AtomConverter):
    """Convert the float built-in type."""

    type: float
    options: {float: (float, float), str: (str, float)}

    def asnative(self, value: object, types: Set[type] = None) -> float:
        if types is None:
            return float(value)
        elif float in types:
            if isinstance(value, float):
                return value
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        elif str in types:
            if isinstance(value, str):
                return float(value)
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        else:
            raise UnknownPrimitiveError(
                "Primitive type cannot be converted to this native type."
            )
