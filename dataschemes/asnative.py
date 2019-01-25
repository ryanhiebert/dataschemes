from typing import Set, TypeVar, Optional
from .converter import converters
from .default import DEFAULT_CONVERTERS


class NativeTypeError(TypeError):
    """Type is unable to be constructed from a serialized value."""


T = TypeVar("T")


def asnative(cls: T, value: object, types: Optional[Set[type]] = None) -> T:
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
    for type_, converter in converters("asnative", DEFAULT_CONVERTERS, types).items():
        if issubclass(cls, type_):
            return converter(value)
    raise NativeTypeError("Type is unable to be constructed from a serialized value.")
