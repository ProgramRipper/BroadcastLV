from typing import Literal

import msgspec

from ..command import Command
from ..util import add_from_bytes

__all__ = [
    "GuardBuy",
]


class Data(msgspec.Struct, kw_only=True, gc=False):
    uid: int
    """发送者 uid"""
    username: str
    """发送者用户名"""
    guard_level: Literal[1, 2, 3]
    """大航海等级，1：总督，2：提督，3：舰长"""
    num: int
    """礼物数量"""
    price: int
    """礼物价格"""
    gift_id: int
    """礼物 id"""
    gift_name: str
    """礼物名称"""
    start_time: int
    """大航海生效时间"""
    end_time: int


@add_from_bytes
class GuardBuy(Command, kw_only=True, gc=False):
    """大航海购买通知"""

    cmd: str
    data: Data
    """大航海购买数据"""
