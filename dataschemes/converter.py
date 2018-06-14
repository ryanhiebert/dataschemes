from abc import ABCMeta, abstractmethod
from typing import Set, TypeVar, Union


def converters(*, asprimitive):
    return {
        type_: Converter(asprimitive=asprimitive)
        for type_, Converter in {
            str: StrConverter,
            int: IntConverter,
            float: FloatConverter,
        }.items()
    }


class UnserializableValueError(ValueError):
    """The primitive types are not able to serialize this value."""


T = TypeVar("T")


class Converter(metaclass=ABCMeta):
    def __init__(self, *, asprimitive):
        self.asprimitive = asprimitive

    def __call__(self, *args, **kwargs):
        method = self.__asprimitive__ if self.asprimitive else self.__asnative__
        return method(*args, **kwargs)

    @abstractmethod
    def __asprimitive__(self, value: object, types: Set[type] = None) -> object:
        raise NotImplementedError

    @abstractmethod
    def __asnative__(self, cls: T, value: object, types: Set[type] = None) -> T:
        raise NotImplementedError


class StrConverter(Converter):
    """Convert the str built-in type."""

    def __asprimitive__(self, value: str, types: Set[type] = None) -> str:
        if types is None or str in types:
            return value
        else:
            raise UnserializableValueError(f"Could not convert str to a primitive.")

    def __asnative__(self, cls, value, types):
        raise NotImplementedError


class IntConverter(Converter):
    """Convert the int built-in type."""

    def __asprimitive__(
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

    def __asnative__(self, cls, value, types):
        raise NotImplementedError


class FloatConverter(Converter):
    """Convert the float built-in type."""

    def __asprimitive__(
        self, value: float, types: Set[type] = None
    ) -> Union[float, str]:
        if types is None or float in types:
            return value
        elif str in types:
            return str(value)
        else:
            raise UnserializableValueError("Could not convert int to a primitive.")

    def __asnative__(self, cls, value, types):
        raise NotImplementedError
