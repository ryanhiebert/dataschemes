from typing import Optional, Set
from .converter import converters
from .default import DEFAULT_CONVERTERS


class UnrecognizedTypeError(TypeError):
    """The type of the value is unable to be serialized."""


def asprimitive(value: object, types: Optional[Set[type]] = None) -> object:
    """Convert a dataclass to primitive serializable types.

    Attempt to convert the given dataclass object into a primitive
    datastructure made up of only the specified types. Because
    different formats are able to serialize different sets of types,
    the set of types the format is able to serialize is taken as
    an optional argument. If the types are not specified, then it
    will make it whatever the type prefers.
    """
    for type_, converter in converters(
        "asprimitive", DEFAULT_CONVERTERS, types
    ).items():
        if isinstance(value, type_):
            return converter(value)
    raise UnrecognizedTypeError("Type cannot be converted to a primitive.")
