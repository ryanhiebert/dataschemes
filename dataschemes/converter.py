from typing import Set, TypeVar, Optional
from dataclasses import dataclass


T = TypeVar("T")


@dataclass
class Converter:
    types: Optional[Set[type]] = None

    def asprimitive(self, value: object) -> object:
        raise NotImplementedError

    def asnative(self, cls: T, value: object) -> T:
        raise NotImplementedError
