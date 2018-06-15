from typing import Set, TypeVar
from .converter import converters


class NativeTypeError(TypeError):
    """Type is unable to be constructed from a serialized value."""


T = TypeVar("T")


def asnative(cls: T, value: object, types: Set[type] = None) -> T:
    """Convert a primitive serializable class to a native type.

    The types given are to allow the native converter to notice if
    a serialized value is a different type than it would have given
    if it had serialized it. This could likely indicate an issue
    with the data structure.

    For example, if the data structure has an ``id`` property that
    is an ``int``, it would prefer to be formatted as a primitive of
    ``int``. If instead it got a ``str`` as the primitive type, it
    may indicate that the data strcture itself should have the ``id``
    as a ``str``, even if it would convert correctly, because ``int``
    may not be sufficient to interpret all possible values.
    """
    for type_, converter in converters(asprimitive=False).items():
        if issubclass(cls, type_):
            # In order to allow for single argument converters, only call
            # the converter with types if asnative was called with types.
            if types is None:
                return converter(value)
            else:
                return converter(value, types)

    raise NativeTypeError("Type is unable to be constructed from a serialized value.")
