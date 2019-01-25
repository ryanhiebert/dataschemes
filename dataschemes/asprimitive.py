from typing import Optional, Set
from .default import DefaultConverter


def asprimitive(value: object, types: Optional[Set[type]] = None) -> object:
    """Convert a dataclass to primitive serializable types.

    Attempt to convert the given dataclass object into a primitive
    datastructure made up of only the specified types. Because
    different formats are able to serialize different sets of types,
    the set of types the format is able to serialize is taken as
    an optional argument. If the types are not specified, then it
    will make it whatever the type prefers.
    """
    return DefaultConverter(types=types).asprimitive(value)
