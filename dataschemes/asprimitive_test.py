from .converter import UnserializableValueError
from .asprimitive import asprimitive, UnrecognizedTypeError

import pytest


def test_str():
    """``str`` goes to ``str``, and nothing else."""
    assert asprimitive("cow") == "cow"
    assert isinstance(asprimitive("cow"), str)
    assert asprimitive("cow", {str}) == "cow"
    assert isinstance(asprimitive("cow", {str}), str)
    with pytest.raises(UnserializableValueError):
        asprimitive("cow", {int})


def test_int():
    """``int`` goes to ``int``, ``float``, or ``str``."""
    assert asprimitive(42) == 42
    assert isinstance(asprimitive(42), int)
    assert asprimitive(42, {int, float, str}) == 42
    assert isinstance(asprimitive(42, {int, float, str}), int)
    assert asprimitive(42, {float, str}) == 42.0
    assert isinstance(asprimitive(42, {float, str}), float)
    assert asprimitive(42, {str}) == "42"
    assert isinstance(asprimitive(42, {str}), str)
    with pytest.raises(UnserializableValueError):
        asprimitive(42, {dict})


def test_float():
    """``float`` goes to ``float`` or ``str``."""
    assert asprimitive(42.0) == 42.0
    assert isinstance(asprimitive(42.0), float)
    assert asprimitive(42.0, {float, str}) == 42.0
    assert isinstance(asprimitive(42.0, {float, str}), float)
    assert asprimitive(42.0, {str}) == "42.0"
    assert isinstance(asprimitive(42.0, {str}), str)
    with pytest.raises(UnserializableValueError):
        asprimitive(42.0, {dict})


def test_unknown():
    """Unknown types cannot be constructed."""
    with pytest.raises(UnrecognizedTypeError):
        asprimitive(..., {str})
