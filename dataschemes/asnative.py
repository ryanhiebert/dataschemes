from typing import Set, TypeVar


class PrimitiveMismatchError(TypeError):
    """Type does not match what would have been serialized."""


class UnknownPrimitiveError(TypeError):
    """Primitive type cannot be converted to this native type."""


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
    if issubclass(cls, str):
        if types is None:
            return str(value)
        elif str in types:
            if isinstance(value, str):
                return value
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        else:
            raise UnknownPrimitiveError(
                "Primitive type cannot be converted to this native type."
            )

    elif issubclass(cls, int):
        if types is None:
            return int(value)
        elif int in types:
            if isinstance(value, int):
                return value
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        elif float in types:
            if isinstance(value, float):
                return int(value)
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        elif str in types:
            if isinstance(value, str):
                return int(value)
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        else:
            raise UnknownPrimitiveError(
                "Primitive type cannot be converted to this native type."
            )

    elif issubclass(cls, float):
        if types is None:
            return float(value)
        elif float in types:
            if isinstance(value, float):
                return value
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        elif str in types:
            if isinstance(value, str):
                return float(value)
            else:
                raise PrimitiveMismatchError(
                    "Type does not match what would have been serialized."
                )
        else:
            raise UnknownPrimitiveError(
                "Primitive type cannot be converted to this native type."
            )

    else:
        raise NativeTypeError(
            "Type is unable to be constructed from a serialized value."
        )
