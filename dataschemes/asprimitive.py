from typing import Set
from abc import ABCMeta, abstractmethod


class UnserializableValueError(ValueError):
    """The primitive types are not able to serialize this value."""


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
    if isinstance(value, str):
        if types is None or str in types:
            return value
        else:
            raise UnserializableValueError("Could not convert str to a primitive.")

    elif isinstance(value, int):
        if types is None or int in types:
            return value
        elif float in types:
            return float(value)
        elif str in types:
            return str(value)
        else:
            raise UnserializableValueError("Could not convert int to a primitive.")

    elif isinstance(value, float):
        if types is None or float in types:
            return value
        elif str in types:
            return str(value)
        else:
            raise UnserializableValueError("Could not convert float to a primitive.")

    else:
        raise UnrecognizedTypeError("Type cannot be converted to a primitive.")
