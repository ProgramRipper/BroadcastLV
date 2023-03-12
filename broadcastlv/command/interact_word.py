from collections.abc import Sequence
from typing import Literal

import msgspec

from ..event import Command
from ..util import add_from_bytes


class Contribution(msgspec.Struct, kw_only=True, gc=False):
    grade: Literal[0, 1, 2, 3]
    """高能用户榜排名，1~3 时有效"""


class FansMedal(msgspec.Struct, kw_only=True, gc=False):
    medal_level: int = 1
    """勋章等级"""
    medal_name: str = "--"
    """勋章名称"""
    anchor_roomid: int = 0
    """勋章拥有者房间号"""
    medal_color: int
    """勋章颜色"""
    special: Literal["", "union"] = ""
    icon_id: int
    medal_color_border: int = 0
    """勋章边框色"""
    medal_color_start: int = 0
    """勋章渐变色起始色"""
    medal_color_end: int = 0
    """勋章渐变色结束色"""
    guard_level: Literal[0, 1, 2, 3] = 0
    """同 SendGift.data.guard_level"""
    is_lighted: Literal[0, 1] = 0
    """是否点亮勋章"""
    target_id: int = 0
    """勋章拥有者 uid"""
    score: int


class Data(msgspec.Struct, kw_only=True, gc=False):
    uid: int
    """发送者 uid"""
    identities: Sequence[int] = ()
    """
    身份列表，1：普通 (Normal)，2：超管 (Manager)，3：粉丝 (Fans)，
    4：老爷 (Vip)，5：年费老爷 (SVip)，6：舰长 (GuardJian)，
    7：提督 (GuardTi)，8：总督 (GuardZong)
    """
    uname: str = "--"
    """发送者用户名"""
    uname_color: str = ""
    """发送者用户名颜色，格式为 #AARRGGBB"""
    msg_type: Literal[1, 2, 3, 4, 5, 6]
    """
    消息类型，1：进场 (Entry)，2：关注 (Attention)，3：分享 (Share)，
    4：：特别关注 (SpecialAttention)，5：互粉 (MutualAttention)，6：未知 (Link)
    """
    fans_medal: FansMedal
    """粉丝勋章信息"""
    timestamp: int
    """发送时间，单位：秒"""
    dmscore: int
    "sendgift.dmscore"
    contribution: Contribution | None
    """高能用户榜贡献"""
    tail_icon: int
    """尾标，102：人气（来自人气榜）"""
    core_user_type: int
    is_spread: int
    privilege_type: int
    roomid: int
    """房间号"""
    score: int
    spread_desc: str
    spread_info: str
    trigger_time: int
    """触发时间，单位：纳秒"""


@add_from_bytes
class InteractWord(Command, kw_only=True, gc=False):
    cmd: Literal["INTERACT_WORD"] = "INTERACT_WORD"
    data: Data
