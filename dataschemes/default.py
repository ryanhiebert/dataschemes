from typing import Optional, Set, Dict, Type, TypeVar, ClassVar
from dataclasses import dataclass
from .converter import Converter
from .builtins import StrConverter, IntConverter, FloatConverter, BoolConverter


class UnrecognizedTypeError(TypeError):
    """The type of the value is unable to be serialized."""


class NativeTypeError(TypeError):
    """Type is unable to be constructed from a serialized value."""


T = TypeVar("T")


@dataclass
class DefaultConverter(Converter):
    converters: ClassVar[Dict[type, Type[Converter]]] = {
        str: StrConverter,
        bool: BoolConverter,
        int: IntConverter,
        float: FloatConverter,
    }

    def asprimitive(self, value: object) -> object:
        for type_, converter in self.converters.items():
            if isinstance(value, type_):
                return converter(types=self.types).asprimitive(value)
        raise UnrecognizedTypeError("Type cannot be converted into a primitive.")

    def asnative(self, cls: Type[T], value: object) -> T:
        for type_, converter in self.converters.items():
            if issubclass(cls, type_):
                return converter(types=self.types).asnative(cls, value)
        raise NativeTypeError("Type cannot be constructed from a primitive value.")
