from typing import Literal

import msgspec

from ..event import Command
from ..util import add_from_bytes

__all__ = [
    "WatchedChange",
]


class Data(msgspec.Struct, kw_only=True, gc=False):
    num: int
    """看过人数"""
    text_small: str
    """人数文本表达"""
    text_large: str
    """看过人数文本表达"""


@add_from_bytes
class WatchedChange(Command, kw_only=True, gc=False):
    """看过人数变化"""

    cmd: Literal["WATCHED_CHANGE"] = "WATCHED_CHANGE"
    data: Data
    """看过人数变化数据"""
