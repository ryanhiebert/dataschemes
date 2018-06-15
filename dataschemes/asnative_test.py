from .converter import PrimitiveMismatchError, UnknownPrimitiveError
from .asnative import asnative, NativeTypeError

import pytest


def test_str():
    """``str`` comes from ``str``."""
    assert asnative(str, "cow") == "cow"
    assert isinstance(asnative(str, "cow"), str)
    assert asnative(str, 42) == "42"
    assert asnative(str, "cow", {str}) == "cow"
    assert isinstance(asnative(str, "cow", {str}), str)
    with pytest.raises(PrimitiveMismatchError):
        asnative(str, 42, {str, int})
    with pytest.raises(UnknownPrimitiveError):
        asnative(str, "cow", {int})


def test_int():
    """``int`` comes from ``int``, ``float``, or ``str``."""
    assert asnative(int, 42) == 42
    assert isinstance(asnative(int, 42), int)
    assert asnative(int, 42, {int, float, str}) == 42
    assert isinstance(asnative(int, 42, {int, float, str}), int)
    with pytest.raises(PrimitiveMismatchError):
        asnative(int, 42.0, {int, float, str})
    assert asnative(int, 42.0, {float, str}) == 42
    assert isinstance(asnative(int, 42.0, {float, str}), int)
    with pytest.raises(PrimitiveMismatchError):
        asnative(int, "42", {float, str})
    assert asnative(int, "42", {str}) == 42
    assert isinstance(asnative(int, "42", {str}), int)
    with pytest.raises(PrimitiveMismatchError):
        asnative(int, {}, {str})
    with pytest.raises(UnknownPrimitiveError):
        asnative(int, "42", {dict})


def test_float():
    """``float`` comes from ``float`` or ``str``."""
    assert asnative(float, 42.0) == 42.0
    assert isinstance(asnative(float, 42.0), float)
    assert asnative(float, 42.0, {float, str}) == 42.0
    assert isinstance(asnative(float, 42.0, {float, str}), float)
    with pytest.raises(PrimitiveMismatchError):
        asnative(float, "42", {float, str})
    assert asnative(float, "42", {str}) == 42.0
    assert isinstance(asnative(float, "42", {str}), float)
    with pytest.raises(PrimitiveMismatchError):
        asnative(float, 42, {str})
    with pytest.raises(UnknownPrimitiveError):
        asnative(float, 42.0, {dict})


def test_unknown():
    """Unknown types cannot be constructed."""
    with pytest.raises(NativeTypeError):
        asnative(type(...), 42, {str})
