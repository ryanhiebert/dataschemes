from abc import ABC, abstractmethod
from typing import Set, TypeVar, Optional, Union, Tuple, Callable, Dict, ClassVar
from dataclasses import dataclass


class UnserializableValueError(ValueError):
    """The primitive types are not able to serialize this value."""


class PrimitiveMismatchError(TypeError):
    """Type does not match what would have been serialized."""


class UnknownPrimitiveError(TypeError):
    """Primitive type cannot be converted to this native type."""


@dataclass
class Converter(ABC):
    types: Optional[Set[type]]

    @abstractmethod
    def asprimitive(self, value: object) -> object:
        raise NotImplementedError

    @abstractmethod
    def asnative(self, value: object) -> object:
        raise NotImplementedError


def converters(
    method: str, converters: Dict[type, Converter], types: Optional[Set[type]]
) -> Callable[[object], object]:
    assert method in ["asprimitive", "asnative"]
    return {
        type_: getattr(Converter(types), method)
        for type_, Converter in converters.items()
    }
