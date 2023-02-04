from __future__ import annotations

import re
from typing import TYPE_CHECKING, TypeVar

import msgspec

__all__ = [
    "add_from_bytes",
    "pascal_to_snake",
    "pascal_to_upper_snake",
]


if TYPE_CHECKING:
    from .event import EventStruct

    _T = TypeVar("_T", bound=type[EventStruct])


def add_from_bytes(cls: _T) -> _T:
    cls.from_bytes = staticmethod(msgspec.json.Decoder(cls).decode)
    return cls


def pascal_to_upper_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()


def pascal_to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
