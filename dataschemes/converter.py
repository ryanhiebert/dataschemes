from abc import ABCMeta, abstractmethod
from typing import Set, TypeVar, Union


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


class StrConverter(Converter):
    """Convert the str built-in type."""

    def asprimitive(self, value: str, types: Set[type] = None) -> str:
        if types is None or str in types:
            return value
        else:
            raise UnserializableValueError(f"Could not convert str to a primitive.")

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


class IntConverter(Converter):
    """Convert the int built-in type."""

    def asprimitive(
        self, value: int, types: Set[type] = None
    ) -> Union[int, float, str]:
        if types is None or int in types:
            return value
        elif float in types:
            return float(value)
        elif str in types:
            return str(value)
        else:
            raise UnserializableValueError("Could not convert int to a primitive.")

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


class FloatConverter(Converter):
    """Convert the float built-in type."""

    def asprimitive(self, value: float, types: Set[type] = None) -> Union[float, str]:
        if types is None or float in types:
            return value
        elif str in types:
            return str(value)
        else:
            raise UnserializableValueError("Could not convert int to a primitive.")

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
