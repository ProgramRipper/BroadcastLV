from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

from ..util import pascal_to_snake, pascal_to_upper_snake

if TYPE_CHECKING:
    from .danmu_msg import DanmuMsg
    from .guard_buy import GuardBuy
    from .interact_word import InteractWord
    from .like_info_v3_update import LikeInfoV3Update
    from .live import Live
    from .send_gift import SendGift
    from .watched_change import WatchedChange

__all__ = [
    "COMMAND_MAP",
    "DanmuMsg",
    "GuardBuy",
    "InteractWord",
    "LikeInfoV3Update",
    "Live",
    "SendGift",
    "WatchedChange",
]


COMMAND_MAP: dict[str, type[Command]] = {}
from ..event import Command

for cmd in __all__[1:]:
    COMMAND_MAP.setdefault(pascal_to_upper_snake(cmd), Command)


def __getattr__(name: str) -> Any:
    if name in __all__[1:]:
        globals()[name] = getattr(
            import_module(f".{pascal_to_snake(name)}", __package__), name
        )
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return __all__
