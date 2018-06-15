from typing import Set
from .converter import converters


class UnrecognizedTypeError(TypeError):
    """The type of the value is unable to be serialized."""


def asprimitive(value: object, types: Set[type] = None) -> object:
    """Convert a dataclass to primitive serializable types.

    Attempt to convert the given dataclass object into a primitive
    datastructure made up of only the specified types. Because
    different formats are able to serialize different sets of types,
    the set of types the format is able to serialize is taken as
    an optional argument. If the types are not specified, then it
    will make it whatever the type prefers.
    """
    for type_, converter in converters(asprimitive=True).items():
        if isinstance(value, type_):
            # In order to allow for single argument converters, only call
            # the converter with types if asprimitive was called with types.
            if types is None:
                return converter(value)
            else:
                return converter(value, types)

    raise UnrecognizedTypeError("Type cannot be converted to a primitive.")
