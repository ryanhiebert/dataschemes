from typing import Set, TypeVar, Optional, Type
from .default import DefaultConverter


T = TypeVar("T")


def asnative(cls: Type[T], value: object, types: Optional[Set[type]] = None) -> T:
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
    return DefaultConverter(types=types).asnative(cls, value)
