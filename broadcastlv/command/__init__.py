from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

from ..util import pascal_to_snake

if TYPE_CHECKING:
    from ..event import Command
    from .danmu_msg import DanmuMsg

__all__ = [
    "COMMAND_MAP",
    "DanmuMsg",
]


COMMAND_MAP: dict[str, type[Command]] = {}


def __getattr__(name: str) -> Any:
    if name in __all__:
        globals()[name] = getattr(
            import_module(f".{pascal_to_snake(name)}", __package__), name
        )
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return __all__
